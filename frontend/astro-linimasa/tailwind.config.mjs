/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#0a0a08',
        ink: '#f3ead9',
        muted: '#8a7e6b',
        line: 'rgba(243,234,217,.12)',
        'evt-suksesi': '#e8a040',
        'evt-perjanjian': '#6bab90',
        'evt-konflik': '#c05a3c',
        'evt-diplomasi': '#7b8ec2',
        'evt-administratif': '#a086c0',
        'voc-copper': '#c4884d',
        'aceh-teal': '#4a8c7e',
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans: ['"IBM Plex Sans"', 'system-ui', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'Menlo', 'monospace'],
      },
    },
  },
  plugins: [],
};
