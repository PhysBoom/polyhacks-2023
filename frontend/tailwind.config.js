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
        quaternary: "#142E36",
      },
      fontSize: {
        "h1": ["60px", "1"],
        "h2": "30px",
        "body": "25px",
        "small": "15px"
      }
    },
  },
  plugins: [],
}