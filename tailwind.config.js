/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./src/templates/**/*.html",
    "./src/templates/**/*.{html,js}",
    "./src/templates/components/**/*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui"),
    require('@tailwindcss/typography'),
  ], 
  daisyui: {
    themes: ["light", "emerald"],
    base: true, // Applies background color and foreground color for root element
    styled: true, // Include daisyUI colors and design decisions
    utils: true, // Adds responsive and modifier utility classes
  },
}

