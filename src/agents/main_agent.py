"""
Main Agent - Master Orchestrator für Test App Entwicklung
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
import time

class MainAgent(BaseAgent):
    def __init__(self):
        super().__init__("main", "Master Orchestrator")
        self.project_phases = [
            "init",
            "sveltekit_setup", 
            "leaflet_integration",
            "github_setup",
            "final_integration"
        ]
        self.current_phase = 0
        self.agent_responses = {}
        
    def setup(self):
        """Setup Main Agent handlers"""
        self.register_handler("phase_complete", self.handle_phase_complete)
        self.register_handler("agent_ready", self.handle_agent_ready)
        self.register_handler("status_request", self.handle_status_request)
        
        print("🎭 Main Agent (Master Orchestrator) ready!")
        print("🎯 Type 'start' to begin Test App development")
        
        # Start interactive mode
        self.interactive_mode()
        
    def interactive_mode(self):
        """Interactive command mode"""
        while True:
            try:
                command = input("\n🎭 Main Agent> ").strip().lower()
                
                if command == "start":
                    self.start_test_app_development()
                elif command == "status":
                    self.check_all_agent_status()
                elif command == "next":
                    self.next_phase()
                elif command == "help":
                    self.show_help()
                elif command in ["quit", "exit"]:
                    break
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n👋 Main Agent shutting down...")
                break
                
    def show_help(self):
        """Show available commands"""
        print("\n🎯 Available Commands:")
        print("  start  - Start Test App development")
        print("  status - Check all agent status")
        print("  next   - Proceed to next phase")
        print("  help   - Show this help")
        print("  quit   - Exit agent")
        
    def start_test_app_development(self):
        """Start coordinated test app development"""
        print("\n🚀 Starting Test App Development...")
        print("📋 Project: Simple Leaflet Map + GitHub Integration")
        print("🎨 Theme: Southwest Desert with Apple Liquid Glass")
        print("🤖 Agents: UI + Leaflet + GitHub")
        
        # Phase 1: Initialize all agents
        self.current_phase = 0
        self.coordinate_phase(self.project_phases[self.current_phase])
        
    def coordinate_phase(self, phase_name: str):
        """Coordinate current development phase"""
        print(f"\n📍 Phase {self.current_phase + 1}: {phase_name}")
        
        if phase_name == "init":
            print("🔄 Initializing all agents...")
            self.send_message("ui", "initialize", {"phase": "init", "role": "SvelteKit + Southwest Theme"})
            self.send_message("leaflet", "initialize", {"phase": "init", "role": "Map Integration"})
            self.send_message("github", "initialize", {"phase": "init", "role": "GitHub MCP Integration"})
            
        elif phase_name == "sveltekit_setup":
            print("🎨 UI Agent: SvelteKit + Southwest Theme setup...")
            self.send_message("ui", "setup_sveltekit", {
                "project_path": "./test-app",
                "theme": "southwest",
                "features": ["tailwind", "typescript", "responsive"]
            })
            
        elif phase_name == "leaflet_integration":
            print("🗺️ Leaflet Agent: Map component integration...")
            self.send_message("leaflet", "create_map_component", {
                "target_path": "./test-app/src/lib/components",
                "default_center": [-115.1398, 36.1699],  # Las Vegas
                "zoom": 8,
                "features": ["click_to_add_markers", "southwest_theme"]
            })
            
        elif phase_name == "github_setup":
            print("🐙 GitHub Agent: Repository and integration setup...")
            self.send_message("github", "setup_repository", {
                "repo_name": "agent-lab-test-app",
                "description": "Test app built with Warp 2.0 Multi-Agent system",
                "features": ["issues", "actions", "project_board"]
            })
            
        elif phase_name == "final_integration":
            print("🔗 Final integration and testing...")
            self.send_message("ui", "integrate_components", {"components": ["map", "github"]})
            
    def handle_phase_complete(self, payload):
        """Handle phase completion from agents"""
        agent = payload.get("agent")
        phase = payload.get("phase")
        
        print(f"✅ {agent} completed {phase}")
        
        self.agent_responses[f"{agent}_{phase}"] = payload
        
        # Check if all agents completed current phase
        if self.all_agents_ready_for_next_phase():
            self.next_phase()
            
    def all_agents_ready_for_next_phase(self):
        """Check if all agents are ready for next phase"""
        current_phase_name = self.project_phases[self.current_phase]
        
        if current_phase_name == "init":
            required_responses = ["ui_init", "leaflet_init", "github_init"]
        elif current_phase_name == "sveltekit_setup":
            required_responses = ["ui_sveltekit_setup"]
        elif current_phase_name == "leaflet_integration":
            required_responses = ["leaflet_map_component"]
        elif current_phase_name == "github_setup":
            required_responses = ["github_repository_setup"]
        else:
            return True
            
        return all(response in self.agent_responses for response in required_responses)
        
    def next_phase(self):
        """Proceed to next phase"""
        if self.current_phase < len(self.project_phases) - 1:
            self.current_phase += 1
            self.coordinate_phase(self.project_phases[self.current_phase])
        else:
            print("\n🎉 All phases completed!")
            print("✅ Test App development finished")
            self.show_final_summary()
            
    def show_final_summary(self):
        """Show final project summary"""
        print("\n📊 PROJECT SUMMARY:")
        print("🎨 UI Agent: SvelteKit app with Southwest theme")
        print("🗺️ Leaflet Agent: Interactive map with markers")
        print("🐙 GitHub Agent: Repository with issues and actions")
        print("🔗 Integration: All components working together")
        print("\n🚀 Test app ready at: ./test-app")
        
    def check_all_agent_status(self):
        """Check status of all agents"""
        print("\n📊 Checking agent status...")
        self.send_message("ui", "status_request", {})
        self.send_message("leaflet", "status_request", {})
        self.send_message("github", "status_request", {})
        
    def handle_agent_ready(self, payload):
        """Handle agent ready notification"""
        agent = payload.get("agent")
        print(f"✅ {agent} is ready")
        
    def handle_status_request(self, payload):
        """Handle status request"""
        return {
            "agent": self.agent_name,
            "status": "active",
            "current_phase": self.project_phases[self.current_phase] if self.current_phase < len(self.project_phases) else "completed",
            "phase_number": self.current_phase + 1,
            "total_phases": len(self.project_phases)
        }

if __name__ == "__main__":
    agent = MainAgent()
    agent.start()
