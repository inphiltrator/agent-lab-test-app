

"""
UI Agent - SvelteKit + Southwest Theme Specialist
"""

import sys
import os
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class UIAgent(BaseAgent):
    def __init__(self):
        super().__init__("ui", "SvelteKit + Southwest Theme Specialist")
        
    def setup(self):
        """Setup UI Agent handlers"""
        self.register_handler("initialize", self.handle_initialize)
        self.register_handler("setup_sveltekit", self.handle_setup_sveltekit)
        self.register_handler("integrate_components", self.handle_integrate_components)
        self.register_handler("status_request", self.handle_status_request)
        
        print("🎨 UI Agent ready!")
        print("🎯 Specializing in: SvelteKit + Southwest Theme + Responsive Design")
        
    def handle_initialize(self, payload):
        """Initialize UI Agent"""
        print("🎨 UI Agent initializing...")
        print("📋 Role: SvelteKit + Southwest Theme Development")
        print("✅ UI Agent ready for SvelteKit setup")
        
        # Notify main agent
        self.send_message("main", "phase_complete", {
            "agent": "ui",
            "phase": "init",
            "status": "ready"
        })
        
    def handle_setup_sveltekit(self, payload):
        """Setup SvelteKit project with Southwest theme"""
        project_path = payload.get("project_path", "./test-app")
        theme = payload.get("theme", "southwest")
        
        print(f"🚀 Setting up SvelteKit project at: {project_path}")
        print(f"🎨 Theme: {theme}")
        
        try:
            # SvelteKit project erstellen
            self.create_sveltekit_project(project_path)
            
            # Southwest theme implementieren
            self.setup_southwest_theme(project_path)
            
            # Tailwind CSS setup
            self.setup_tailwind(project_path)
            
            print("✅ SvelteKit + Southwest theme setup complete!")
            
            # Notify completion
            self.send_message("main", "phase_complete", {
                "agent": "ui",
                "phase": "sveltekit_setup",
                "status": "complete",
                "project_path": project_path
            })
            
        except Exception as e:
            print(f"❌ SvelteKit setup failed: {e}")
            self.update_status("error", f"SvelteKit setup failed: {e}")
            
    def create_sveltekit_project(self, project_path):
        """Create new SvelteKit project"""
        print("📦 Creating SvelteKit project...")
        
        # SvelteKit mit TypeScript erstellen
        cmd = f"npm create svelte@latest {project_path} -- --template skeleton --types typescript --no-prettier --no-eslint --no-playwright --no-vitest"
        
        try:
            subprocess.run(cmd, shell=True, check=True, cwd="./")
            print("✅ SvelteKit project created")
            
            # Dependencies installieren
            subprocess.run("npm install", shell=True, check=True, cwd=project_path)
            print("✅ Dependencies installed")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"SvelteKit creation failed: {e}")
            
    def setup_southwest_theme(self, project_path):
        """Setup Southwest theme colors and styles"""
        print("🌵 Setting up Southwest theme...")
        
        # Southwest CSS erstellen
        southwest_css = """
/* Southwest Desert Theme */
:root {
  /* Southwest Color Palette */
  --southwest-sunset: #FF6B35;
  --southwest-desert: #D2691E;
  --southwest-sage: #9CAF88;
  --southwest-canyon: #CD853F;
  --southwest-sky: #87CEEB;
  
  /* Glass Effects */
  --glass-primary: rgba(255, 255, 255, 0.1);
  --glass-elevated: rgba(255, 255, 255, 0.15);
  --glass-subtle: rgba(255, 255, 255, 0.05);
  
  /* Text Colors */
  --text-primary: #1D1D1F;
  --text-secondary: #86868B;
  --text-accent: #FF6B35;
}

body {
  background: linear-gradient(135deg, var(--southwest-sunset) 0%, var(--southwest-desert) 50%, var(--southwest-canyon) 100%);
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Glass Components */
.glass-card {
  backdrop-filter: blur(12px);
  background: var(--glass-primary);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.glass-button {
  backdrop-filter: blur(8px);
  background: var(--glass-elevated);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 12px;
  color: white;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.glass-button:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}
"""
        
        # CSS Datei schreiben
        css_path = f"{project_path}/src"
        os.makedirs(css_path, exist_ok=True)
        
        with open(f"{css_path}/southwest.css", "w") as f:
            f.write(southwest_css)
            
        # App.svelte updaten
        app_svelte = """<script>
  import './southwest.css';
</script>

<main class="min-h-screen p-4">
  <div class="glass-card p-8 max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-white mb-6">
      🌵 Southwest Test App
    </h1>
    <p class="text-white/80 mb-8">
      Built with Warp 2.0 Multi-Agent System
    </p>
    
    <div class="grid gap-6">
      <!-- Map container will be added by Leaflet Agent -->
      <div id="map-container" class="glass-card p-4 h-96">
        <p class="text-white/60 text-center pt-20">
          🗺️ Map will be loaded by Leaflet Agent...
        </p>
      </div>
      
      <!-- GitHub integration will be added -->
      <div class="glass-card p-4">
        <h2 class="text-xl font-semibold text-white mb-4">
          🐙 GitHub Integration
        </h2>
        <p class="text-white/60">
          GitHub features will be added by GitHub Agent...
        </p>
      </div>
    </div>
  </div>
</main>

<style>
  main {
    padding: 1rem;
  }
</style>
"""
        
        with open(f"{project_path}/src/app.html", "w") as f:
            f.write("""<!doctype html>
<html lang="en">
	<head>
		<meta charset="utf-8" />
		<link rel="icon" href="%sveltekit.assets%/favicon.png" />
		<meta name="viewport" content="width=device-width, initial-scale=1" />
		%sveltekit.head%
	</head>
	<body data-sveltekit-preload-data="hover" class="bg-gradient-to-br from-orange-500 via-red-500 to-yellow-500">
		<div style="display: contents">%sveltekit.body%</div>
	</body>
</html>
""")
        
        with open(f"{project_path}/src/routes/+page.svelte", "w") as f:
            f.write(app_svelte)
            
        print("✅ Southwest theme setup complete")
        
    def setup_tailwind(self, project_path):
        """Setup Tailwind CSS"""
        print("🎨 Setting up Tailwind CSS...")
        
        try:
            # Tailwind installieren
            subprocess.run("npm install -D tailwindcss postcss autoprefixer @tailwindcss/typography", 
                         shell=True, check=True, cwd=project_path)
            
            # Tailwind init
            subprocess.run("npx tailwindcss init -p", shell=True, check=True, cwd=project_path)
            
            # Tailwind config
            tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'southwest': {
          'sunset': '#FF6B35',
          'desert': '#D2691E', 
          'sage': '#9CAF88',
          'canyon': '#CD853F',
          'sky': '#87CEEB'
        }
      },
      backdropBlur: {
        xs: '2px'
      }
    },
  },
  plugins: [],
}
"""
            
            with open(f"{project_path}/tailwind.config.js", "w") as f:
                f.write(tailwind_config)
                
            # CSS directives hinzufügen
            app_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gradient-to-br from-southwest-sunset via-southwest-desert to-southwest-canyon;
  }
}

@layer components {
  .glass {
    @apply backdrop-blur-md bg-white/10 border border-white/20 rounded-xl shadow-lg;
  }
  
  .glass-elevated {
    @apply backdrop-blur-lg bg-white/15 border-white/30 rounded-2xl shadow-xl;
  }
}
"""
            
            with open(f"{project_path}/src/app.css", "w") as f:
                f.write(app_css)
                
            print("✅ Tailwind CSS setup complete")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Tailwind setup failed: {e}")
            
    def handle_integrate_components(self, payload):
        """Integrate components from other agents"""
        components = payload.get("components", [])
        
        print(f"🔗 Integrating components: {components}")
        
        # Integration logic wird hier implementiert
        # wenn Components von anderen Agents verfügbar sind
        
        self.send_message("main", "phase_complete", {
            "agent": "ui",
            "phase": "final_integration",
            "status": "complete",
            "integrated_components": components
        })
        
    def handle_status_request(self, payload):
        """Handle status request"""
        return {
            "agent": self.agent_name,
            "status": "ready",
            "specialization": "SvelteKit + Southwest Theme + Responsive Design",
            "capabilities": ["sveltekit_setup", "southwest_theme", "tailwind_css", "component_integration"]
        }

if __name__ == "__main__":
    agent = UIAgent()
    agent.start()
