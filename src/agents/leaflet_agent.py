"""
Leaflet Agent - Map Integration Specialist
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class LeafletAgent(BaseAgent):
    def __init__(self):
        super().__init__("leaflet", "Map Integration Specialist")
        
    def setup(self):
        """Setup Leaflet Agent handlers"""
        self.register_handler("initialize", self.handle_initialize)
        self.register_handler("create_map_component", self.handle_create_map_component)
        self.register_handler("status_request", self.handle_status_request)
        
        print("🗺️ Leaflet Agent ready!")
        print("🎯 Specializing in: Leaflet.js + SvelteKit + Southwest Map Features")
        
    def handle_initialize(self, payload):
        """Initialize Leaflet Agent"""
        print("🗺️ Leaflet Agent initializing...")
        print("📋 Role: Interactive Map Integration with Southwest Markers")
        print("✅ Leaflet Agent ready for map component creation")
        
        # Notify main agent
        self.send_message("main", "phase_complete", {
            "agent": "leaflet",
            "phase": "init",
            "status": "ready"
        })
        
    def handle_create_map_component(self, payload):
        """Create Leaflet map component for SvelteKit"""
        target_path = payload.get("target_path", "./test-app/src/lib/components")
        default_center = payload.get("default_center", [-115.1398, 36.1699])  # Las Vegas
        zoom = payload.get("zoom", 8)
        features = payload.get("features", [])
        
        print(f"🗺️ Creating map component at: {target_path}")
        print(f"📍 Default center: {default_center}")
        print(f"🔍 Zoom level: {zoom}")
        print(f"✨ Features: {features}")
        
        try:
            # Components directory erstellen
            os.makedirs(target_path, exist_ok=True)
            
            # Map Component erstellen
            self.create_leaflet_component(target_path, default_center, zoom, features)
            
            # Package.json updaten für Leaflet
            self.setup_leaflet_dependencies(target_path)
            
            # Map in main page integrieren
            self.integrate_map_component(target_path)
            
            print("✅ Leaflet map component created successfully!")
            
            # Notify completion
            self.send_message("main", "phase_complete", {
                "agent": "leaflet",
                "phase": "map_component",
                "status": "complete",
                "component_path": f"{target_path}/MapContainer.svelte"
            })
            
        except Exception as e:
            print(f"❌ Map component creation failed: {e}")
            self.update_status("error", f"Map component creation failed: {e}")
            
    def create_leaflet_component(self, target_path, center, zoom, features):
        """Create Leaflet SvelteKit component"""
        print("📦 Creating Leaflet component...")
        
        map_component = f'''<script lang="ts">
  import {{ onMount, onDestroy }} from 'svelte';
  import type {{ Map, Marker }} from 'leaflet';

  export let center: [number, number] = [{center[0]}, {center[1]}];
  export let zoom: number = {zoom};
  export let height: string = '400px';

  let mapContainer: HTMLDivElement;
  let map: Map;
  let markers: Marker[] = [];

  onMount(async () => {{
    // Dynamically import Leaflet for SSR compatibility
    const L = await import('leaflet');
    
    // Import Leaflet CSS
    await import('leaflet/dist/leaflet.css');
    
    // Initialize map
    map = L.default.map(mapContainer).setView(center, zoom);
    
    // Add Southwest-themed tile layer
    L.default.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
      attribution: '© OpenStreetMap contributors'
    }}).addTo(map);
    
    // Custom Southwest marker icon
    const southwestIcon = L.default.divIcon({{
      className: 'southwest-marker',
      html: '<div class="marker-pin">🌵</div>',
      iconSize: [30, 30],
      iconAnchor: [15, 30]
    }});
    
    // Add click handler for adding markers
    map.on('click', (e) => {{
      const marker = L.default.marker([e.latlng.lat, e.latlng.lng], {{
        icon: southwestIcon
      }}).addTo(map);
      
      marker.bindPopup(`
        <div class="glass p-3 rounded-lg">
          <h3 class="font-bold text-southwest-sunset">Southwest Marker</h3>
          <p class="text-sm">Lat: ${{e.latlng.lat.toFixed(4)}}</p>
          <p class="text-sm">Lng: ${{e.latlng.lng.toFixed(4)}}</p>
        </div>
      `);
      
      markers.push(marker);
    }});
    
    // Add initial marker at center
    const initialMarker = L.default.marker(center, {{
      icon: southwestIcon
    }}).addTo(map);
    
    initialMarker.bindPopup(`
      <div class="glass p-3 rounded-lg">
        <h3 class="font-bold text-southwest-sunset">🎯 Southwest Center</h3>
        <p class="text-sm">Click anywhere to add markers!</p>
      </div>
    `);
    
    markers.push(initialMarker);
    
    console.log('🗺️ Southwest Leaflet map initialized');
  }});

  onDestroy(() => {{
    if (map) {{
      map.remove();
    }}
  }});
</script>

<div 
  bind:this={{mapContainer}} 
  class="leaflet-map glass-elevated rounded-xl overflow-hidden shadow-lg"
  style="height: {{height}}; width: 100%;"
></div>

<style>
  :global(.southwest-marker) {{
    background: transparent;
    border: none;
  }}
  
  :global(.marker-pin) {{
    font-size: 24px;
    text-align: center;
    background: rgba(255, 107, 53, 0.9);
    color: white;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    width: 30px;
    height: 30px;
    line-height: 30px;
    border: 2px solid rgba(255, 255, 255, 0.5);
  }}
  
  :global(.leaflet-popup-content-wrapper) {{
    backdrop-filter: blur(8px);
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
  }}
</style>
'''
        
        # Component file schreiben
        with open(f"{target_path}/MapContainer.svelte", "w") as f:
            f.write(map_component)
            
        print("✅ MapContainer.svelte created")
        
    def setup_leaflet_dependencies(self, target_path):
        """Setup Leaflet dependencies"""
        print("📦 Setting up Leaflet dependencies...")
        
        # Gehe zum Projektroot
        project_root = target_path.replace("/src/lib/components", "")
        
        try:
            import subprocess
            
            # Leaflet installieren
            subprocess.run("npm install leaflet", shell=True, check=True, cwd=project_root)
            subprocess.run("npm install -D @types/leaflet", shell=True, check=True, cwd=project_root)
            
            print("✅ Leaflet dependencies installed")
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Leaflet dependencies installation failed: {e}")
            
    def integrate_map_component(self, target_path):
        """Integrate map component into main page"""
        print("🔗 Integrating map component...")
        
        project_root = target_path.replace("/src/lib/components", "")
        page_path = f"{project_root}/src/routes/+page.svelte"
        
        # Updated page with map integration
        updated_page = '''<script>
  import MapContainer from '$lib/components/MapContainer.svelte';
  import '../southwest.css';
</script>

<main class="min-h-screen p-4">
  <div class="glass-card p-8 max-w-6xl mx-auto">
    <h1 class="text-4xl font-bold text-white mb-6">
      🌵 Southwest Test App
    </h1>
    <p class="text-white/80 mb-8">
      Built with Warp 2.0 Multi-Agent System
    </p>
    
    <div class="grid gap-6">
      <!-- Interactive Southwest Map -->
      <div class="glass-card p-6">
        <h2 class="text-2xl font-semibold text-white mb-4">
          🗺️ Interactive Southwest Map
        </h2>
        <p class="text-white/70 mb-4">
          Click anywhere on the map to add Southwest-themed markers!
        </p>
        <MapContainer height="500px" />
      </div>
      
      <!-- GitHub integration placeholder -->
      <div class="glass-card p-6">
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
'''
        
        with open(page_path, "w") as f:
            f.write(updated_page)
            
        print("✅ Map component integrated into main page")
        
    def handle_status_request(self, payload):
        """Handle status request"""
        return {
            "agent": self.agent_name,
            "status": "ready", 
            "specialization": "Leaflet.js + SvelteKit + Southwest Mapping",
            "capabilities": ["leaflet_integration", "southwest_markers", "click_to_add", "responsive_maps"]
        }

if __name__ == "__main__":
    agent = LeafletAgent()
    agent.start()
