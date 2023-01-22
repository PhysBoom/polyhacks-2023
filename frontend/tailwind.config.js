/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#000000",
        secondary: "#D9D9D9",
        tertiary: "#FFFFFF",
      },
      fontSize: {
        "h1": ["60px", "1"],
        "body": "25px",
        "small": "20px"
      }
    },
  },
  plugins: [],
}