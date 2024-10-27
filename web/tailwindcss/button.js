module.exports = ({ addComponents }) => {
    const variants = [
        { name: 'primary', baseColor: 'primary' },
        { name: 'success', baseColor: 'green' },
        { name: 'info', baseColor: 'blue' },
        { name: 'warning', baseColor: 'yellow' },
        { name: 'danger', baseColor: 'red' },
        {
            name: 'white',
            fillColor: 'white',
            textColor: 'black',
            hoverColor: 'gray-400',
            disableColor: 'gray-200',
        },
        {
            name: 'black',
            fillColor: 'black',
            textColor: 'white',
            hoverColor: 'gray-900',
            disableColor: 'gray-400',
        },
    ];

    const base = {
        '.btn': {
            '@apply rounded-s-full rounded-e-full px-4 py-2 transition-colors inline-block no-underline hover:no-underline text-sm':
                {},
            '&.btn-sm': {
                '@apply px-3 py-2 text-xs': {},
            },
            '&.btn-lg': {
                '@apply text-base px-4 py-3': {},
            },
        },
    };

    const variantClasses = variants.map(x => {
        const name = x.name;
        const color = x.baseColor ? `${x.baseColor}-500` : x.fillColor;
        const textColor = x.baseColor ? 'white' : x.textColor;
        const hoverColor = x.baseColor ? `${x.baseColor}-700` : x.hoverColor;
        const disableColor = x.baseColor
            ? `${x.baseColor}-300`
            : x.disableColor;

        return {
            [`.btn-${name}`]: {
                [`@apply bg-${color} text-${textColor}`]: {},
                '&:hover:not(:disabled)': {
                    [`@apply bg-${hoverColor} text-${textColor}`]: '',
                },
                '&:disabled': {
                    [`@apply bg-${disableColor}`]: {},
                },
            },

            [`.btn-outline-${name}`]: {
                [`@apply border border-${color} text-${color}`]: {},
                '&:hover:not(:disabled)': {
                    [`@apply bg-${color} text-${textColor}`]: {},
                },
                '&:disabled': {
                    [`@apply border-${disableColor} text-${disableColor}`]: {},
                },
            },

            [`.btn-${name}, .btn-outline-${name}`]: {
                '&:focus, &:focus-within': {
                    [`@apply ring-4 ring-${color} ring-opacity-25 outline-none`]:
                        {},
                },
            },
        };
    });

    const all = Object.assign(...[base, ...variantClasses]);

    addComponents(all);
};
