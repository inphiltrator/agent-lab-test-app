
"""
Base Agent Class für Redis + MCP Koordination
"""

import redis
import json
import time
import os
import threading
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import logging

class BaseAgent:
    def __init__(self, agent_name: str, agent_role: str):
        self.agent_name = agent_name
        self.agent_role = agent_role
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        
        # Redis Setup
        try:
            self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
            print(f"✅ {agent_name} connected to Redis")
        except Exception as e:
            print(f"❌ {agent_name} Redis connection failed: {e}")
            raise
        
        # Message handlers
        self.message_handlers: Dict[str, Callable] = {}
        self.is_running = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"Agent-{agent_name}")
        
    def register_handler(self, message_type: str, handler: Callable):
        """Register message handler for specific message type"""
        self.message_handlers[message_type] = handler
        
    def send_message(self, to_agent: str, message_type: str, payload: Dict[str, Any]):
        """Send message to another agent"""
        message = {
            "from": self.agent_name,
            "to": to_agent,
            "type": message_type,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload
        }
        
        try:
            channel = f'agent_{to_agent}'
            self.redis_client.publish(channel, json.dumps(message))
            self.update_status("active", f"Sent {message_type} to {to_agent}")
            self.logger.info(f"📤 → {to_agent}: {message_type}")
        except Exception as e:
            self.logger.error(f"❌ Message send failed: {e}")
    
    def update_status(self, status: str, task: Optional[str] = None):
        """Update agent status for MCP Bridge"""
        status_update = {
            "agent": self.agent_name,
            "status": status,
            "task": task,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            self.redis_client.publish('agent_status_update', json.dumps(status_update))
        except Exception as e:
            self.logger.error(f"❌ Status update failed: {e}")
    
    def listen_for_messages(self):
        """Listen for incoming messages"""
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(f'agent_{self.agent_name}')
            
            self.logger.info(f"👂 {self.agent_name} listening for messages...")
            self.update_status("ready", "Waiting for tasks")
            
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        data = json.loads(message['data'])
                        message_type = data.get('type')
                        payload = data.get('payload', {})
                        from_agent = data.get('from')
                        
                        self.logger.info(f"📥 ← {from_agent}: {message_type}")
                        
                        if message_type in self.message_handlers:
                            self.update_status("working", f"Processing {message_type}")
                            result = self.message_handlers[message_type](payload)
                            
                            # Send response if handler returns something
                            if result:
                                self.send_message(from_agent, f"{message_type}_response", result)
                        else:
                            self.logger.warning(f"No handler for message type: {message_type}")
                            
                    except json.JSONDecodeError:
                        self.logger.warning("Invalid JSON message received")
                    except Exception as e:
                        self.logger.error(f"Message processing error: {e}")
                        self.update_status("error", str(e))
                        
        except KeyboardInterrupt:
            self.logger.info(f"🛑 {self.agent_name} stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Listen error: {e}")
        finally:
            self.update_status("offline", "Agent stopped")
    
    def start(self):
        """Start the agent"""
        self.is_running = True
        self.update_status("starting", "Agent initialization")
        self.setup()
        self.listen_for_messages()
    
    def setup(self):
        """Override in subclass for agent-specific setup"""
        pass
    
    def stop(self):
        """Stop the agent"""
        self.is_running = False
        self.update_status("stopping", "Agent shutdown")
