
# ===== src/config/agent_config.py =====
#!/usr/bin/env python3
"""
Agent Configuration für Warp 2.0 Multi-Agent System
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    name: str
    role: str
    redis_channel: str
    capabilities: List[str]
    dependencies: List[str]
    timeout: int = 30
    retry_attempts: int = 3

@dataclass
class ProjectConfig:
    """Overall project configuration"""
    project_name: str = "Southwest Test App"
    project_path: str = "./test-app"
    redis_url: str = "redis://localhost:6379"
    agent_lab_path: str = "/Users/default/development/agent-lab"
    
class AgentLabConfig:
    """Central configuration for Agent Lab"""
    
    def __init__(self):
        self.redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
        self.agent_lab_path = os.getenv('AGENT_LAB_PATH', '/Users/default/development/agent-lab')
        self.github_token = os.getenv('GITHUB_TOKEN', '')
        
        # Project settings
        self.project = ProjectConfig(
            project_name="Southwest Test App",
            project_path="./test-app",
            redis_url=self.redis_url,
            agent_lab_path=self.agent_lab_path
        )
        
        # Agent configurations
        self.agents = {
            "main": AgentConfig(
                name="main",
                role="Master Orchestrator",
                redis_channel="agent_main",
                capabilities=[
                    "project_coordination",
                    "phase_management", 
                    "agent_monitoring",
                    "task_distribution"
                ],
                dependencies=[],
                timeout=60
            ),
            
            "ui": AgentConfig(
                name="ui",
                role="SvelteKit + Southwest Theme Specialist",
                redis_channel="agent_ui",
                capabilities=[
                    "sveltekit_setup",
                    "southwest_theme",
                    "tailwind_css",
                    "component_integration",
                    "responsive_design"
                ],
                dependencies=["main"],
                timeout=120
            ),
            
            "leaflet": AgentConfig(
                name="leaflet",
                role="Map Integration Specialist", 
                redis_channel="agent_leaflet",
                capabilities=[
                    "leaflet_integration",
                    "southwest_markers",
                    "click_to_add",
                    "responsive_maps",
                    "ssr_safe_loading"
                ],
                dependencies=["main", "ui"],
                timeout=90
            ),
            
            "github": AgentConfig(
                name="github",
                role="GitHub MCP Integration Specialist",
                redis_channel="agent_github", 
                capabilities=[
                    "repository_setup",
                    "github_actions",
                    "issue_management",
                    "mcp_integration",
                    "ci_cd_pipeline"
                ],
                dependencies=["main"],
                timeout=180
            )
        }
        
        # Development phases
        self.phases = [
            {
                "name": "init",
                "description": "Initialize all agents",
                "required_agents": ["main", "ui", "leaflet", "github"],
                "estimated_time": "2-3 minutes"
            },
            {
                "name": "sveltekit_setup", 
                "description": "SvelteKit + Southwest theme setup",
                "required_agents": ["ui"],
                "estimated_time": "5-8 minutes"
            },
            {
                "name": "leaflet_integration",
                "description": "Map component integration",
                "required_agents": ["leaflet"],
                "estimated_time": "8-12 minutes"
            },
            {
                "name": "github_setup",
                "description": "Repository and CI/CD setup", 
                "required_agents": ["github"],
                "estimated_time": "10-15 minutes"
            },
            {
                "name": "final_integration",
                "description": "Final integration and testing",
                "required_agents": ["ui", "leaflet", "github"],
                "estimated_time": "5-10 minutes"
            }
        ]
        
        # Southwest theme configuration
        self.southwest_theme = {
            "colors": {
                "sunset": "#FF6B35",
                "desert": "#D2691E", 
                "sage": "#9CAF88",
                "canyon": "#CD853F",
                "sky": "#87CEEB"
            },
            "glass_effects": {
                "primary": "rgba(255, 255, 255, 0.1)",
                "elevated": "rgba(255, 255, 255, 0.15)",
                "subtle": "rgba(255, 255, 255, 0.05)"
            },
            "map_defaults": {
                "center": [-115.1398, 36.1699],  # Las Vegas
                "zoom": 8,
                "marker_icon": "🌵"
            }
        }
        
        # MCP Server configurations  
        self.mcp_servers = {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", self.agent_lab_path],
                "start_on_launch": True
            },
            "github": {
                "command": "docker",
                "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": self.github_token
                },
                "start_on_launch": True
            },
            "memory": {
                "command": "npx", 
                "args": ["-y", "@modelcontextprotocol/server-memory"],
                "env": {
                    "MEMORY_FILE_PATH": f"{self.agent_lab_path}/warp-agent-memory.json"
                },
                "start_on_launch": True
            }
        }
        
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get configuration for specific agent"""
        return self.agents.get(agent_name)
        
    def get_phase_config(self, phase_name: str) -> Dict[str, Any]:
        """Get configuration for specific phase"""
        for phase in self.phases:
            if phase["name"] == phase_name:
                return phase
        return None
        
    def validate_dependencies(self, agent_name: str, active_agents: List[str]) -> bool:
        """Check if agent dependencies are satisfied"""
        agent_config = self.get_agent_config(agent_name)
        if not agent_config:
            return False
            
        for dependency in agent_config.dependencies:
            if dependency not in active_agents:
                return False
        return True
        
    def get_mcp_config_json(self) -> str:
        """Generate MCP configuration JSON for Warp"""
        config = {
            "mcpServers": self.mcp_servers
        }
        import json
        return json.dumps(config, indent=2)

# Global config instance
config = AgentLabConfig()