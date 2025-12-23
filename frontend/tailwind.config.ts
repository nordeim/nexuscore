import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // Singapore branding colors
        singapore: {
          red: '#eb582d',
          blue: '#1e3a8a',
        },
        // Primary color scale (Singapore red)
        primary: {
          50: '#fef3f0',
          100: '#fde5de',
          200: '#fbc8bc',
          300: '#f8a18f',
          400: '#f47252',
          500: '#eb582d',
          600: '#d94420',
          700: '#b5351a',
          800: '#932d1a',
          900: '#78291b',
        },
        // Secondary color scale (Singapore blue)
        secondary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e3a8a',
          900: '#1e3a5f',
        },
        // Glass morphism colors
        glass: {
          light: 'rgba(255, 255, 255, 0.7)',
          DEFAULT: 'rgba(255, 255, 255, 0.5)',
          dark: 'rgba(0, 0, 0, 0.5)',
        },
        // Dark mode colors
        dark: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backdropBlur: {
        xs: '2px',
      },
      animation: {
        'gradient': 'gradient 3s ease infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        gradient: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(235, 88, 45, 0.3)' },
          '100%': { boxShadow: '0 0 40px rgba(235, 88, 45, 0.6)' },
        },
      },
    },
  },
  plugins: [],
};
export default config;
