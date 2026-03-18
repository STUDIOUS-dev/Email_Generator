/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // ── solid-pink palette ─────────────────────────────────────────────
        // Usage guide:
        //   pink-100  (#f8ebeb) → app backgrounds, large surfaces, cards
        //   pink-400  (#d79599) → borders, hover states, secondary elements
        //   pink-700  (#913f4d) → primary buttons, active states, highlights
        //   pink-950  (#3a171f) → headings, body text, high-contrast elements
        pink: {
          100: '#f8ebeb',
          400: '#d79599',
          700: '#913f4d',
          950: '#3a171f',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.5s ease-out',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      boxShadow: {
        'card': '0 2px 12px rgba(58, 23, 31, 0.08)',
        'card-hover': '0 8px 32px rgba(58, 23, 31, 0.16)',
        'btn': '0 2px 8px rgba(145, 63, 77, 0.35)',
        'btn-hover': '0 4px 16px rgba(145, 63, 77, 0.5)',
      },
    },
  },
  plugins: [],
}
