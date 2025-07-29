<script lang="ts">
	import { onMount } from 'svelte';

	let mounted = false;
	let heroRef: HTMLElement;

	onMount(() => {
		mounted = true;
		
		// Parallax effect for hero section
		const handleScroll = () => {
			if (heroRef) {
				const scrolled = window.pageYOffset;
				const parallax = scrolled * 0.5;
				heroRef.style.transform = `translateY(${parallax}px)`;
			}
		};

		window.addEventListener('scroll', handleScroll);
		return () => window.removeEventListener('scroll', handleScroll);
	});
</script>

<svelte:head>
	<title>Southwest Desert Theme - Home</title>
	<meta name="description" content="Experience the beauty of the Southwest Desert with our Apple Liquid Glass design" />
</svelte:head>

<!-- Hero Section -->
<section class="relative min-h-screen flex items-center justify-center overflow-hidden">
	<!-- Background Pattern -->
	<div bind:this={heroRef} class="absolute inset-0 opacity-10">
		<div class="absolute top-20 left-20 text-6xl animate-float">🌵</div>
		<div class="absolute top-40 right-32 text-4xl animate-float" style="animation-delay: 1s;">🏜️</div>
		<div class="absolute bottom-32 left-1/4 text-5xl animate-float" style="animation-delay: 2s;">🌄</div>
		<div class="absolute top-1/3 right-20 text-3xl animate-float" style="animation-delay: 3s;">🦎</div>
	</div>

	<div class="relative z-10 text-center px-6 max-w-4xl mx-auto">
		<div class="{mounted ? 'animate-slide-up' : 'opacity-0 translate-y-8'}">
			<h1 class="text-5xl md:text-7xl font-bold mb-6">
				<span class="text-gradient-sunset">Southwest</span>
				<br>
				<span class="text-gradient-sage">Desert Theme</span>
			</h1>
			
			<p class="text-lg md:text-xl text-gray-700 mb-8 max-w-2xl mx-auto">
				Experience the warmth and beauty of the American Southwest with our stunning Apple Liquid Glass design system.
			</p>
			
			<div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
				<button class="btn-primary">
					Explore Features
				</button>
				<button class="btn-secondary">
					View Documentation
				</button>
			</div>
		</div>
	</div>
</section>

<!-- Features Section -->
<section class="py-20 px-6">
	<div class="max-w-7xl mx-auto">
		<div class="text-center mb-16">
			<h2 class="text-4xl font-bold text-gradient-sunset mb-4">Desert-Inspired Features</h2>
			<p class="text-lg text-gray-600 max-w-2xl mx-auto">
				Discover the power of Southwest aesthetics combined with modern web technology.
			</p>
		</div>
		
		<div class="grid md:grid-cols-3 gap-8">
			<!-- Feature Card 1 -->
			<div class="glass-card p-8 text-center card-float">
				<div class="w-16 h-16 bg-gradient-desert rounded-2xl flex items-center justify-center mx-auto mb-6">
					<span class="text-3xl">🌅</span>
				</div>
				<h3 class="text-xl font-bold text-gray-800 mb-3">Sunset Colors</h3>
				<p class="text-gray-600">
					Warm, vibrant colors inspired by desert sunsets and canyon walls.
				</p>
			</div>
			
			<!-- Feature Card 2 -->
			<div class="glass-card p-8 text-center card-float" style="animation-delay: 0.2s;">
				<div class="w-16 h-16 bg-gradient-sage rounded-2xl flex items-center justify-center mx-auto mb-6">
					<span class="text-3xl">💎</span>
				</div>
				<h3 class="text-xl font-bold text-gray-800 mb-3">Liquid Glass</h3>
				<p class="text-gray-600">
					Apple-inspired glass morphism with backdrop blur effects.
				</p>
			</div>
			
			<!-- Feature Card 3 -->
			<div class="glass-card p-8 text-center card-float" style="animation-delay: 0.4s;">
				<div class="w-16 h-16 bg-gradient-sky rounded-2xl flex items-center justify-center mx-auto mb-6">
					<span class="text-3xl">📱</span>
				</div>
				<h3 class="text-xl font-bold text-gray-800 mb-3">Mobile First</h3>
				<p class="text-gray-600">
					Responsive design that works beautifully on all devices.
				</p>
			</div>
		</div>
	</div>
</section>

<!-- Map Preview Section -->
<section class="py-20 px-6 bg-gradient-to-r from-mesa-tan/10 to-desert-sage/10">
	<div class="max-w-4xl mx-auto text-center">
		<h2 class="text-4xl font-bold text-gradient-sunset mb-6">Ready for Map Integration</h2>
		<p class="text-lg text-gray-600 mb-8">
			This theme is designed to beautifully showcase interactive maps and location-based content.
		</p>
		
		<!-- Map Placeholder -->
		<div class="glass-card p-8 mb-8">
			<div class="bg-gradient-to-br from-desert-sky/20 to-sage-green/20 rounded-xl h-64 flex items-center justify-center">
				<div class="text-center">
					<div class="text-6xl mb-4">🗺️</div>
					<p class="text-gray-600 font-medium">Interactive Map Component</p>
					<p class="text-sm text-gray-500 mt-2">Ready for integration</p>
				</div>
			</div>
		</div>
		
		<button class="btn-primary">
			Explore Map Features
		</button>
	</div>
</section>

<!-- Theme Showcase -->
<section class="py-20 px-6">
	<div class="max-w-6xl mx-auto">
		<div class="text-center mb-16">
			<h2 class="text-4xl font-bold text-gradient-sage mb-4">Color Palette</h2>
			<p class="text-lg text-gray-600">
				Inspired by the natural beauty of the American Southwest.
			</p>
		</div>
		
		<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
			<div class="glass-card p-6 text-center">
				<div class="w-full h-20 bg-sunset-orange rounded-lg mb-4"></div>
				<h4 class="font-semibold text-gray-800">Sunset Orange</h4>
				<p class="text-sm text-gray-500">#FF6B35</p>
			</div>
			
			<div class="glass-card p-6 text-center">
				<div class="w-full h-20 bg-desert-sage rounded-lg mb-4"></div>
				<h4 class="font-semibold text-gray-800">Desert Sage</h4>
				<p class="text-sm text-gray-500">#9CAF88</p>
			</div>
			
			<div class="glass-card p-6 text-center">
				<div class="w-full h-20 bg-canyon-red rounded-lg mb-4"></div>
				<h4 class="font-semibold text-gray-800">Canyon Red</h4>
				<p class="text-sm text-gray-500">#B85450</p>
			</div>
			
			<div class="glass-card p-6 text-center">
				<div class="w-full h-20 bg-mesa-tan rounded-lg mb-4"></div>
				<h4 class="font-semibold text-gray-800">Mesa Tan</h4>
				<p class="text-sm text-gray-500">#E8C5A0</p>
			</div>
		</div>
	</div>
</section>

<style>
	/* Component-specific animations */
	@keyframes float {
		0%, 100% { transform: translateY(0px); }
		50% { transform: translateY(-20px); }
	}
</style>
