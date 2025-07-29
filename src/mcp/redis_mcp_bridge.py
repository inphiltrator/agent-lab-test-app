#!/usr/bin/env python3
"""
Redis-MCP Bridge for Warp 2.0
Connects Redis Pub/Sub with an MCP memory server and exposes a minimal
MCP-compatible JSON-RPC 2.0 interface (`stdin`/`stdout`).

Supported MCP methods:
- initialize
- list_tools (returns empty list – no tools exposed)
- shutdown

Anything else returns JSON-RPC error –32601 (method not found).

The bridge keeps listening on Redis `agent_status_update` channel and
updates a JSON memory file so that Warp’s memory MCP server can serve it.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Optional

import redis
import logging

############################
# Logging setup            #
############################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("redis-mcp-bridge")

############################
# Bridge core              #
############################


class RedisMCPBridge:
    """Holds Redis connection and updates the JSON memory file."""

    def __init__(self) -> None:
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        self.agent_lab_path = os.getenv(
            "AGENT_LAB_PATH", os.path.expanduser("~/development/agent-lab")
        )
        self.memory_file = os.path.join(self.agent_lab_path, "warp-agent-memory.json")

        # Redis connection -------------------------------------------------
        try:
            self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("✅ Connected to Redis %s", self.redis_url)
        except Exception as exc:  # pragma: no cover
            logger.error("❌ Redis connection failed: %s", exc)
            sys.exit(1)

        self._init_memory_file()

    # ------------------------------------------------------------------
    # Memory helpers
    # ------------------------------------------------------------------
    def _init_memory_file(self) -> None:
        if os.path.exists(self.memory_file):
            logger.info("📝 Memory file exists: %s", self.memory_file)
            return

        initial_memory: Dict[str, Any] = {
            "agents": {},
            "coordination": {
                "active_phase": "init",
                "total_agents": 0,
                "active_agents": 0,
            },
            "created_at": datetime.utcnow().isoformat(),
        }
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(initial_memory, f, indent=2)
        logger.info("✅ Memory file initialised: %s", self.memory_file)

    def _load_memory(self) -> Dict[str, Any]:
        with open(self.memory_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_memory(self, data: Dict[str, Any]) -> None:
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # Public API used by listener
    # ------------------------------------------------------------------
    def update_agent_status(self, agent: str, status: str, task: Optional[str] = None) -> None:
        mem = self._load_memory()
        agents = mem.setdefault("agents", {})
        agent_entry = agents.setdefault(agent, {"status": "unknown", "tasks": []})
        agent_entry["status"] = status
        agent_entry["last_update"] = datetime.utcnow().isoformat()
        if task:
            agent_entry["tasks"].append({"task": task, "timestamp": datetime.utcnow().isoformat()})
            agent_entry["tasks"] = agent_entry["tasks"][-10:]
        mem["coordination"]["active_agents"] = sum(
            1 for a in agents.values() if a.get("status") in {"active", "working", "ready"}
        )
        self._save_memory(mem)
        logger.info("📊 %s → %s %s", agent, status, f"({task})" if task else "")

    # ------------------------------------------------------------------
    # Redis listener (blocking)
    # ------------------------------------------------------------------
    def listen_for_agent_updates(self) -> None:
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe("agent_status_update")
        logger.info("👂 Listening on Redis channel agent_status_update …")
        for message in pubsub.listen():
            if message.get("type") != "message":
                continue
            try:
                data = json.loads(message["data"])  # type: ignore[arg-type]
                self.update_agent_status(
                    data.get("agent", "unknown"), data.get("status", "unknown"), data.get("task")
                )
            except Exception as exc:  # pragma: no cover
                logger.warning("Invalid status update: %s", exc)

############################
# Minimal MCP JSON-RPC     #
############################


class MCPJsonRpcServer:
    """Very small JSON-RPC 2.0 loop that fulfils MCP handshake."""

    def __init__(self, bridge: RedisMCPBridge) -> None:
        self.bridge = bridge
        self.loop = asyncio.get_event_loop()
        self._running = True
        # run blocking redis listener in executor
        # Schedule the blocking Redis listener in a background thread
        self.loop.run_in_executor(None, self.bridge.listen_for_agent_updates)

    # ------------------------------------------------------------------
    # JSON-RPC helpers
    # ------------------------------------------------------------------
    def _reply(self, _id: Any, result: Any = None, *, error: Optional[Dict[str, Any]] = None) -> None:
        response = {"jsonrpc": "2.0", "id": _id}
        if error is not None:
            response["error"] = error
        else:
            response["result"] = result
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

    # ------------------------------------------------------------------
    # Supported methods
    # ------------------------------------------------------------------
    def _method_initialize(self, _id: Any, _params: Dict[str, Any]):
        self._reply(
            _id,
            {
                "serverInfo": {"name": "redis-mcp-bridge", "version": "0.1.0"},
                "protocolVersion": "2024-11-05",
                "capabilities": {},
            },
        )

    def _method_list_tools(self, _id: Any, _params: Dict[str, Any]):
        self._reply(_id, [])

    def _method_shutdown(self, _id: Any, _params: Dict[str, Any]):
        self._running = False
        self._reply(_id, True)

    # ------------------------------------------------------------------
    async def serve(self) -> None:  # noqa: C901  (simple enough)
        while self._running:
            line = await self.loop.run_in_executor(None, sys.stdin.readline)
            if line == "":
                # EOF
                break
            try:
                request = json.loads(line.strip())
                _id = request.get("id")
                method = request.get("method")
                params = request.get("params", {}) or {}
                if method == "initialize":
                    self._method_initialize(_id, params)
                elif method == "list_tools":
                    self._method_list_tools(_id, params)
                elif method == "shutdown":
                    self._method_shutdown(_id, params)
                else:
                    self._reply(
                        _id,
                        error={"code": -32601, "message": f"Method {method} not found"},
                    )
            except Exception as exc:  # pragma: no cover
                self._reply(None, error={"code": -32603, "message": str(exc)})

############################
# Entry-point              #
############################


def main() -> None:  # pragma: no cover
    bridge = RedisMCPBridge()
    logger.info("🌉 Redis-MCP Bridge running (JSON-RPC mode)")
    server = MCPJsonRpcServer(bridge)
    try:
        server.loop.run_until_complete(server.serve())
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("👋 Redis-MCP Bridge stopped")


if __name__ == "__main__":
    main()