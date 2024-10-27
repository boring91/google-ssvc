const plugin = require('tailwindcss/plugin');
const button = require('./tailwindcss/button');

/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{html,ts}'],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: 'rgb(var(--primary-500) / <alpha-value>)',
                    50: 'rgb(var(--primary-50) / <alpha-value>)',
                    100: 'rgb(var(--primary-100) / <alpha-value>)',
                    200: 'rgb(var(--primary-200) / <alpha-value>)',
                    300: 'rgb(var(--primary-300) / <alpha-value>)',
                    400: 'rgb(var(--primary-400) / <alpha-value>)',
                    500: 'rgb(var(--primary-500) / <alpha-value>)',
                    600: 'rgb(var(--primary-600) / <alpha-value>)',
                    700: 'rgb(var(--primary-700) / <alpha-value>)',
                    800: 'rgb(var(--primary-800) / <alpha-value>)',
                    900: 'rgb(var(--primary-900) / <alpha-value>)',
                    950: 'rgb(var(--primary-950) / <alpha-value>)',
                },
                secondary: {
                    DEFAULT: 'rgb(var(--secondary-500) / <alpha-value>)',
                    50: 'rgb(var(--secondary-50) / <alpha-value>)',
                    100: 'rgb(var(--secondary-100) / <alpha-value>)',
                    200: 'rgb(var(--secondary-200) / <alpha-value>)',
                    300: 'rgb(var(--secondary-300) / <alpha-value>)',
                    400: 'rgb(var(--secondary-400) / <alpha-value>)',
                    500: 'rgb(var(--secondary-500) / <alpha-value>)',
                    600: 'rgb(var(--secondary-600) / <alpha-value>)',
                    700: 'rgb(var(--secondary-700) / <alpha-value>)',
                    800: 'rgb(var(--secondary-800) / <alpha-value>)',
                    900: 'rgb(var(--secondary-900) / <alpha-value>)',
                    950: 'rgb(var(--secondary-950) / <alpha-value>)',
                },
            },
        },
    },
    plugins: [plugin(button)],
};
