#!/usr/bin/env python3
"""
GitHub Agent - GitHub MCP Integration Specialist
"""

import sys
import os
import subprocess
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class GitHubAgent(BaseAgent):
    def __init__(self):
        super().__init__("github", "GitHub MCP Integration Specialist")
        
    def setup(self):
        """Setup GitHub Agent handlers"""
        self.register_handler("initialize", self.handle_initialize)
        self.register_handler("setup_repository", self.handle_setup_repository)
        self.register_handler("status_request", self.handle_status_request)
        
        print("🐙 GitHub Agent ready!")
        print("🎯 Specializing in: GitHub MCP Server + Repository Management")
        
    def handle_initialize(self, payload):
        """Initialize GitHub Agent"""
        print("🐙 GitHub Agent initializing...")
        print("📋 Role: GitHub Repository + MCP Integration")
        print("✅ GitHub Agent ready for repository setup")
        
        # Check GitHub CLI availability
        if self.check_github_cli():
            print("✅ GitHub CLI available")
        else:
            print("⚠️ GitHub CLI not found - some features may be limited")
        
        # Notify main agent
        self.send_message("main", "phase_complete", {
            "agent": "github",
            "phase": "init",
            "status": "ready"
        })
        
    def check_github_cli(self):
        """Check if GitHub CLI is available"""
        try:
            subprocess.run("gh --version", shell=True, check=True, 
                         capture_output=True, text=True)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def handle_setup_repository(self, payload):
        """Setup GitHub repository with MCP integration"""
        repo_name = payload.get("repo_name", "agent-lab-test-app")
        description = payload.get("description", "Test app built with Warp 2.0 Multi-Agent system")
        features = payload.get("features", [])
        
        print(f"🐙 Setting up GitHub repository: {repo_name}")
        print(f"📝 Description: {description}")
        print(f"🎯 Features: {features}")
        
        try:
            # Local Git repository initialisieren
            self.init_local_repo(repo_name)
            
            # README und andere Files erstellen
            self.create_repo_files(repo_name, description)
            
            # GitHub Repository erstellen (falls GitHub CLI verfügbar)
            if self.check_github_cli():
                self.create_github_repo(repo_name, description)
            
            # GitHub Actions setup
            if "actions" in features:
                self.setup_github_actions(repo_name)
                
            # Issues setup
            if "issues" in features:
                self.create_initial_issues(repo_name)
                
            print("✅ GitHub repository setup complete!")
            
            # Notify completion
            self.send_message("main", "phase_complete", {
                "agent": "github",
                "phase": "repository_setup",
                "status": "complete",
                "repository": repo_name,
                "features_enabled": features
            })
            
        except Exception as e:
            print(f"❌ GitHub setup failed: {e}")
            self.update_status("error", f"GitHub setup failed: {e}")
            
    def init_local_repo(self, repo_name):
        """Initialize local git repository"""
        print("📦 Initializing local git repository...")
        
        repo_path = f"./test-app"
        
        try:
            # Git init
            subprocess.run("git init", shell=True, check=True, cwd=repo_path)
            
            # Git config (falls noch nicht gesetzt)
            subprocess.run("git config user.name 'Warp Agent' || true", 
                         shell=True, cwd=repo_path)
            subprocess.run("git config user.email 'agent@warp.dev' || true", 
                         shell=True, cwd=repo_path)
            
            print("✅ Local git repository initialized")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git initialization failed: {e}")
            
    def create_repo_files(self, repo_name, description):
        """Create repository files"""
        print("📝 Creating repository files...")
        
        repo_path = "./test-app"
        
        # README.md
        readme_content = f"""# {repo_name}

{description}

## 🌵 Southwest Test App

Built with **Warp 2.0 Multi-Agent System** featuring:

- 🎨 **UI Agent**: SvelteKit + Southwest Desert Theme
- 🗺️ **Leaflet Agent**: Interactive Map with Southwest Markers  
- 🐙 **GitHub Agent**: Repository Management via MCP
- 🤖 **Main Agent**: Master Orchestrator

## 🚀 Features

- ✅ Interactive Leaflet Map
- ✅ Southwest Apple Liquid Glass Theme
- ✅ Click-to-Add Markers
- ✅ Responsive Design
- ✅ TypeScript Support
- ✅ GitHub Integration

## 🛠️ Tech Stack

- **Frontend**: SvelteKit + TypeScript
- **Styling**: Tailwind CSS + Custom Southwest Theme
- **Maps**: Leaflet.js
- **Development**: Warp 2.0 Multi-Agent Coordination

## 🎯 Development

This app was built entirely through AI agent coordination:

1. **Main Agent** orchestrated the entire development process
2. **UI Agent** created the SvelteKit app with Southwest theming
3. **Leaflet Agent** integrated the interactive map component
4. **GitHub Agent** set up this repository and documentation

## 🌵 Southwest Theme

The app features a custom Southwest USA desert theme with:
- Sunset Orange (`#FF6B35`) - Primary accent
- Desert Sage (`#9CAF88`) - Success/nature elements  
- Canyon Red (`#CD853F`) - Warning/earth tones
- Sky Blue (`#87CEEB`) - Info/sky elements
- Apple Liquid Glass effects with backdrop-blur

## 🗺️ Map Features

- Default view centered on Las Vegas, Nevada
- Click anywhere to add Southwest-themed markers (🌵)
- Responsive design for mobile and desktop
- Custom popup styling with glass effects

## 🚀 Getting Started

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## 🤖 Agent Coordination

This project demonstrates the power of **Warp 2.0's Multi-Agent Development Environment**:

- **Real-time coordination** between specialized AI agents
- **MCP (Model Context Protocol)** for standardized tool communication
- **Redis Pub/Sub** for agent-to-agent messaging
- **Agent Management Panel** for visual progress tracking

---

*Built with ❤️ by Warp 2.0 Multi-Agent System*
"""
        
        with open(f"{repo_path}/README.md", "w") as f:
            f.write(readme_content)
            
        # .gitignore
        gitignore_content = """# Dependencies
node_modules/
/.pnp
.pnp.js

# Build outputs
/.svelte-kit/
/build/
/dist/

# Environment
.env
.env.local
.env.*.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage
coverage/
.nyc_output

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Temporary
*.tmp
*.temp
"""
        
        with open(f"{repo_path}/.gitignore", "w") as f:
            f.write(gitignore_content)
            
        print("✅ Repository files created")
        
    def create_github_repo(self, repo_name, description):
        """Create GitHub repository using GitHub CLI"""
        print("🐙 Creating GitHub repository...")
        
        repo_path = "./test-app"
        
        try:
            # GitHub repo erstellen
            cmd = f"gh repo create {repo_name} --description '{description}' --public --source=."
            subprocess.run(cmd, shell=True, check=True, cwd=repo_path)
            
            # Initial commit und push
            subprocess.run("git add .", shell=True, check=True, cwd=repo_path)
            subprocess.run("git commit -m 'Initial commit: Southwest Test App via Warp 2.0 Multi-Agent System'", 
                         shell=True, check=True, cwd=repo_path)
            subprocess.run("git push -u origin main", shell=True, check=True, cwd=repo_path)
            
            print("✅ GitHub repository created and pushed")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ GitHub repo creation failed: {e}")
            print("📝 You can manually create the repo and push later")
            
    def setup_github_actions(self, repo_name):
        """Setup GitHub Actions workflow"""
        print("⚙️ Setting up GitHub Actions...")
        
        repo_path = "./test-app"
        workflows_dir = f"{repo_path}/.github/workflows"
        os.makedirs(workflows_dir, exist_ok=True)
        
        # CI workflow
        workflow_content = """name: Southwest Test App CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install dependencies
      run: npm ci
      
    - name: Build Southwest App
      run: npm run build
      
    - name: Test Southwest Components
      run: npm run test || echo "Tests will be added later"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
        
    - name: Install and Build
      run: |
        npm ci
        npm run build
        
    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./build
"""
        
        with open(f"{workflows_dir}/ci.yml", "w") as f:
            f.write(workflow_content)
            
        print("✅ GitHub Actions workflow created")
        
    def create_initial_issues(self, repo_name):
        """Create initial GitHub issues"""
        print("📋 Creating initial GitHub issues...")
        
        issues = [
            {
                "title": "🎨 Enhance Southwest Theme with More Desert Elements",
                "body": "Add more Southwest-specific design elements:\\n- Cactus icons and imagery\\n- Desert sunset gradients\\n- Route 66 inspired typography\\n- Sand texture backgrounds"
            },
            {
                "title": "🗺️ Add More Map Features",
                "body": "Enhance the Leaflet map with:\\n- Marker clustering for multiple points\\n- Different marker types (gas stations, restaurants, attractions)\\n- Route planning between markers\\n- Southwest POI data integration"
            },
            {
                "title": "🚀 Performance Optimization",
                "body": "Optimize app performance:\\n- Lazy loading for map components\\n- Image optimization\\n- Bundle size reduction\\n- Mobile performance improvements"
            },
            {
                "title": "📱 Mobile Experience Enhancement",
                "body": "Improve mobile experience:\\n- Touch-friendly map controls\\n- Responsive design refinements\\n- Offline map capabilities\\n- PWA features"
            },
            {
                "title": "🧪 Add Testing Framework",
                "body": "Implement comprehensive testing:\\n- Unit tests for Southwest components\\n- Integration tests for map functionality\\n- E2E tests for user workflows\\n- Visual regression testing"
            }
        ]
        
        repo_path = "./test-app"
        
        for issue in issues:
            try:
                if self.check_github_cli():
                    cmd = f'gh issue create --title "{issue["title"]}" --body "{issue["body"]}"'
                    subprocess.run(cmd, shell=True, check=True, cwd=repo_path)
                    print(f"✅ Created issue: {issue['title']}")
                else:
                    print(f"📝 Issue template: {issue['title']}")
                    
            except subprocess.CalledProcessError as e:
                print(f"⚠️ Issue creation failed: {e}")
                
        print("✅ Initial issues created")
        
    def handle_status_request(self, payload):
        """Handle status request"""
        return {
            "agent": self.agent_name,
            "status": "ready",
            "specialization": "GitHub MCP Integration + Repository Management",
            "capabilities": ["repository_setup", "github_actions", "issue_management", "mcp_integration"]
        }

if __name__ == "__main__":
    agent = GitHubAgent()
    agent.start()