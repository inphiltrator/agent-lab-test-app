/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        // Southwest Desert Theme
        'sunset-orange': '#FF6B35',
        'desert-sage': '#9CAF88',
        'canyon-red': '#B85450',
        'mesa-tan': '#E8C5A0',
        'sage-green': '#7A9B76',
        'desert-sky': '#87CEEB',
        'cactus': '#2F5233',
        'sandstone': '#D2B48C',
        'adobe': '#C19A6B'
      },
      fontFamily: {
        'sans': ['SF Pro Display', 'system-ui', 'sans-serif'],
        'mono': ['SF Mono', 'Monaco', 'Inconsolata', 'monospace']
      },
      backdropBlur: {
        'xs': '2px',
        'glass': '20px'
      },
      backgroundColor: {
        'glass': 'rgba(255, 255, 255, 0.1)',
        'glass-dark': 'rgba(0, 0, 0, 0.1)'
      },
      borderColor: {
        'glass': 'rgba(255, 255, 255, 0.2)'
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'float': 'float 6s ease-in-out infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        }
      }
    },
  },
  plugins: [],
}
