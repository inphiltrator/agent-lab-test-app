
#!/usr/bin/env python3
"""
Agent Coordinator - Warp Agent Management Helper
Koordiniert zwischen Redis und MCP für optimales Warp 2.0 Experience
"""

import redis
import json
import asyncio
import os
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.agent_config import config

class AgentCoordinator:
    """
    Central coordinator for multi-agent development
    Manages agent lifecycle, communication, and status reporting
    """
    
    def __init__(self):
        self.redis_url = config.redis_url
        self.agent_lab_path = config.agent_lab_path
        self.memory_file = f"{self.agent_lab_path}/warp-agent-memory.json"
        
        # Redis connection
        try:
            self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
            print(f"✅ Agent Coordinator connected to Redis: {self.redis_url}")
        except Exception as e:
            print(f"❌ Redis connection failed: {e}")
            raise
            
        # Agent tracking
        self.active_agents: Dict[str, Dict] = {}
        self.agent_heartbeats: Dict[str, datetime] = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("AgentCoordinator")
        
        # Initialize coordination
        self.init_coordination_system()
        
    def init_coordination_system(self):
        """Initialize the coordination system"""
        try:
            # Create memory file if it doesn't exist
            if not os.path.exists(self.memory_file):
                self.create_initial_memory()
                
            # Set up Redis channels for coordination
            self.setup_redis_channels()
            
            self.logger.info("🎭 Agent Coordinator initialized")
            
        except Exception as e:
            self.logger.error(f"❌ Coordination system init failed: {e}")
            raise
            
    def create_initial_memory(self):
        """Create initial memory structure for MCP"""
        initial_memory = {
            "coordination": {
                "status": "initialized",
                "active_agents": 0,
                "total_agents": len(config.agents),
                "current_phase": "init",
                "started_at": datetime.utcnow().isoformat()
            },
            "agents": {},
            "phases": {
                phase["name"]: {
                    "status": "pending",
                    "estimated_time": phase["estimated_time"],
                    "required_agents": phase["required_agents"]
                }
                for phase in config.phases
            },
            "project": {
                "name": config.project.project_name,
                "path": config.project.project_path,
                "tech_stack": ["SvelteKit", "Leaflet", "GitHub MCP", "Southwest Theme"]
            }
        }
        
        # Initialize agent entries
        for agent_name, agent_config in config.agents.items():
            initial_memory["agents"][agent_name] = {
                "status": "offline",
                "role": agent_config.role,
                "capabilities": agent_config.capabilities,
                "dependencies": agent_config.dependencies,
                "last_seen": None,
                "tasks": [],
                "errors": []
            }
            
        # Write to file
        with open(self.memory_file, 'w') as f:
            json.dump(initial_memory, f, indent=2)
            
        self.logger.info(f"📝 Initial memory created: {self.memory_file}")
        
    def setup_redis_channels(self):
        """Setup Redis pub/sub channels for coordination"""
        self.coordination_channels = [
            "agent_status_update",
            "agent_heartbeat", 
            "phase_transition",
            "coordination_command"
        ]
        
        for channel in self.coordination_channels:
            # Test channel connectivity
            try:
                self.redis_client.publish(channel, json.dumps({
                    "type": "coordinator_init",
                    "timestamp": datetime.utcnow().isoformat()
                }))
            except Exception as e:
                self.logger.warning(f"Channel setup warning for {channel}: {e}")
                
    def register_agent(self, agent_name: str, agent_info: Dict[str, Any]):
        """Register an agent with the coordinator"""
        try:
            # Update active agents tracking
            self.active_agents[agent_name] = {
                **agent_info,
                "registered_at": datetime.utcnow(),
                "status": "active"
            }
            
            # Update heartbeat
            self.agent_heartbeats[agent_name] = datetime.utcnow()
            
            # Update memory file
            self.update_agent_memory(agent_name, "active", "Agent registered and ready")
            
            # Publish registration event
            self.redis_client.publish("agent_status_update", json.dumps({
                "event": "agent_registered",
                "agent": agent_name,
                "timestamp": datetime.utcnow().isoformat()
            }))
            
            self.logger.info(f"✅ Agent registered: {agent_name}")
            
        except Exception as e:
            self.logger.error(f"❌ Agent registration failed for {agent_name}: {e}")
            
    def update_agent_status(self, agent_name: str, status: str, task: Optional[str] = None):
        """Update agent status in coordination system"""
        try:
            # Update heartbeat
            self.agent_heartbeats[agent_name] = datetime.utcnow()
            
            # Update active agents
            if agent_name in self.active_agents:
                self.active_agents[agent_name]["status"] = status
                if task:
                    self.active_agents[agent_name]["current_task"] = task
                    
            # Update memory
            self.update_agent_memory(agent_name, status, task)
            
            # Check for phase transitions
            self.check_phase_transition()
            
            self.logger.info(f"📊 {agent_name}: {status}" + (f" - {task}" if task else ""))
            
        except Exception as e:
            self.logger.error(f"❌ Status update failed for {agent_name}: {e}")
            
    def update_agent_memory(self, agent_name: str, status: str, task: Optional[str] = None):
        """Update agent status in MCP memory file"""
        try:
            # Load current memory
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                
            # Update agent entry
            if agent_name not in memory["agents"]:
                memory["agents"][agent_name] = {
                    "status": "unknown",
                    "tasks": [],
                    "errors": []
                }
                
            memory["agents"][agent_name]["status"] = status
            memory["agents"][agent_name]["last_seen"] = datetime.utcnow().isoformat()
            
            if task:
                memory["agents"][agent_name]["tasks"].append({
                    "task": task,
                    "timestamp": datetime.utcnow().isoformat()
                })
                # Keep only last 10 tasks
                memory["agents"][agent_name]["tasks"] = memory["agents"][agent_name]["tasks"][-10:]
                
            # Update coordination stats
            active_count = sum(1 for agent in memory["agents"].values() 
                             if agent["status"] in ["active", "working", "ready"])
            memory["coordination"]["active_agents"] = active_count
            memory["coordination"]["last_update"] = datetime.utcnow().isoformat()
            
            # Save updated memory
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"❌ Memory update failed for {agent_name}: {e}")
            
    def check_phase_transition(self):
        """Check if we can transition to next phase"""
        try:
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                
            current_phase = memory["coordination"]["current_phase"]
            phase_config = config.get_phase_config(current_phase)
            
            if not phase_config:
                return
                
            # Check if all required agents are ready for this phase
            required_agents = phase_config["required_agents"]
            ready_agents = [
                name for name, info in memory["agents"].items()
                if info["status"] in ["ready", "active"] and name in required_agents
            ]
            
            if len(ready_agents) == len(required_agents):
                self.logger.info(f"🎯 Phase {current_phase} ready - all agents available")
                
                # Publish phase ready event
                self.redis_client.publish("phase_transition", json.dumps({
                    "event": "phase_ready",
                    "phase": current_phase,
                    "ready_agents": ready_agents,
                    "timestamp": datetime.utcnow().isoformat()
                }))
                
        except Exception as e:
            self.logger.error(f"❌ Phase transition check failed: {e}")
            
    def monitor_agent_health(self):
        """Monitor agent health via heartbeats"""
        unhealthy_agents = []
        current_time = datetime.utcnow()
        
        for agent_name, last_heartbeat in self.agent_heartbeats.items():
            # Check if agent hasn't sent heartbeat in 2 minutes
            if current_time - last_heartbeat > timedelta(minutes=2):
                unhealthy_agents.append(agent_name)
                self.logger.warning(f"⚠️ Agent {agent_name} appears unhealthy (last seen: {last_heartbeat})")
                
        return unhealthy_agents
        
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination status"""
        try:
            with open(self.memory_file, 'r') as f:
                memory = json.load(f)
                
            unhealthy_agents = self.monitor_agent_health()
            
            return {
                "coordination": memory["coordination"],
                "active_agents": len(self.active_agents),
                "total_agents": len(config.agents),
                "unhealthy_agents": unhealthy_agents,
                "phases": memory["phases"],
                "last_update": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"❌ Status retrieval failed: {e}")
            return {"error": str(e)}
            
    def send_coordination_command(self, command: str, targets: List[str], payload: Dict[str, Any]):
        """Send coordination command to agents"""
        try:
            message = {
                "command": command,
                "targets": targets,
                "payload": payload,
                "timestamp": datetime.utcnow().isoformat(),
                "sender": "coordinator"
            }
            
            # Send to coordination command channel
            self.redis_client.publish("coordination_command", json.dumps(message))
            
            # Also send to individual agent channels
            for target in targets:
                if target in config.agents:
                    channel = f"agent_{target}"
                    self.redis_client.publish(channel, json.dumps({
                        "from": "coordinator",
                        "to": target,
                        "type": "coordination_command",
                        "payload": {
                            "command": command,
                            **payload
                        },
                        "timestamp": datetime.utcnow().isoformat()
                    }))
                    
            self.logger.info(f"📤 Coordination command sent: {command} → {targets}")
            
        except Exception as e:
            self.logger.error(f"❌ Command send failed: {e}")
            
    def start_monitoring(self):
        """Start monitoring loop"""
        self.logger.info("👁️ Starting agent monitoring...")
        
        try:
            while True:
                # Health check
                unhealthy = self.monitor_agent_health()
                if unhealthy:
                    self.logger.warning(f"⚠️ Unhealthy agents detected: {unhealthy}")
                    
                # Status summary every 30 seconds
                status = self.get_coordination_status()
                self.logger.info(f"📊 Coordination: {status['active_agents']}/{status['total_agents']} agents active")
                
                time.sleep(30)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Monitoring stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Monitoring error: {e}")

def main():
    """Main entry point for Agent Coordinator"""
    coordinator = AgentCoordinator()
    
    print("🎭 Agent Coordinator started")
    print(f"📍 Agent Lab Path: {coordinator.agent_lab_path}")
    print(f"💾 Memory File: {coordinator.memory_file}")
    print("🔄 Ready for agent coordination...")
    
    try:
        coordinator.start_monitoring()
    except KeyboardInterrupt:
        print("👋 Coordinator shutdown complete")

if __name__ == "__main__":
    main()