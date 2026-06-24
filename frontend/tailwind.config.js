/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#2563EB',
        secondary: '#7C3AED',
        accent: '#06B6D4',
        success: '#10B981',
        background: '#0F172A',
        surface: '#1E293B',
        'text-primary': '#F8FAFC',
        'text-secondary': '#CBD5E1',
        border: '#334155',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'hero-gradient': 'linear-gradient(135deg, #2563EB 0%, #7C3AED 50%, #06B6D4 100%)',
      },
    },
  },
  plugins: [],
};
