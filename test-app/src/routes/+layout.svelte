<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';

	let mounted = false;

	onMount(() => {
		mounted = true;
	});
</script>

<svelte:head>
	<title>Southwest Desert Theme</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-mesa-tan/20 via-desert-sky/20 to-sage-green/20">
	<!-- Glass Navigation -->
	<nav class="glass-nav sticky top-0 z-50 px-6 py-4">
		<div class="max-w-7xl mx-auto flex items-center justify-between">
			<div class="flex items-center space-x-2">
				<div class="w-8 h-8 bg-gradient-desert rounded-lg flex items-center justify-center">
					<span class="text-white font-bold text-sm">🌵</span>
				</div>
				<h1 class="text-xl font-bold text-gradient-sunset">Desert App</h1>
			</div>
			
			<div class="hidden md:flex items-center space-x-6">
				<a href="/" class="text-gray-700 hover:text-sunset-orange transition-colors duration-300">Home</a>
				<a href="/map" class="text-gray-700 hover:text-sunset-orange transition-colors duration-300">Map</a>
				<a href="/about" class="text-gray-700 hover:text-sunset-orange transition-colors duration-300">About</a>
			</div>
			
			<!-- Mobile Menu Button -->
			<button class="md:hidden btn-glass">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
				</svg>
			</button>
		</div>
	</nav>

	<!-- Main Content -->
	<main class="{mounted ? 'animate-fade-in' : 'opacity-0'}">
		<slot />
	</main>

	<!-- Footer -->
	<footer class="mt-20 glass-nav border-t border-glass/50">
		<div class="max-w-7xl mx-auto px-6 py-8">
			<div class="text-center text-gray-600">
				<p class="text-sm">© 2024 Desert App - Built with SvelteKit & Southwest Theme</p>
				<div class="mt-4 flex justify-center space-x-4">
					<span class="text-2xl animate-float">🌵</span>
					<span class="text-2xl animate-float" style="animation-delay: 1s;">🏜️</span>
					<span class="text-2xl animate-float" style="animation-delay: 2s;">🌄</span>
				</div>
			</div>
		</div>
	</footer>
</div>

<style>
	/* Additional component-specific styles */
	:global(html) {
		scroll-behavior: smooth;
	}
</style>
