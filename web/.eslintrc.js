module.exports = {
    root: true,
    env: {
        es6: true,
    },
    plugins: ['prettier', 'import', '@typescript-eslint'],
    overrides: [
        {
            files: ['*.ts'],
            parserOptions: {
                tsconfigRootDir: __dirname,
                project: ['./tsconfig.json'],
            },
            extends: [
                'plugin:@angular-eslint/recommended',
                'plugin:@angular-eslint/template/process-inline-templates',
            ],
            rules: {
                '@angular-eslint/directive-selector': [
                    'error',
                    {
                        'type': 'attribute',
                        'prefix': 'app',
                        'style': 'camelCase',
                    },
                ],
                '@angular-eslint/component-selector': [
                    'error',
                    {
                        'type': 'element',
                        'prefix': 'app',
                        'style': 'kebab-case',
                    },
                ],
                '@typescript-eslint/explicit-member-accessibility': ['error'],
                '@typescript-eslint/naming-convention': [
                    'error',
                    {
                        'selector': 'default',
                        'format': ['strictCamelCase'],
                        'leadingUnderscore': 'forbid',
                        'trailingUnderscore': 'forbid',
                    },
                    {
                        'selector': 'parameter',
                        'format': ['strictCamelCase'],
                        'leadingUnderscore': 'allow',
                        'trailingUnderscore': 'allow',
                    },
                    {
                        'selector': 'variable',
                        'format': ['StrictPascalCase'],
                        'types': ['boolean'],
                        'prefix': ['is', 'should', 'has', 'can', 'did', 'will'],
                    },
                    {
                        'selector': 'typeLike',
                        'format': ['StrictPascalCase'],
                    },
                ],
                '@typescript-eslint/no-unused-vars': ['error'],
                '@typescript-eslint/no-empty-function': ['error'],
                '@typescript-eslint/explicit-function-return-type': [
                    'error',
                    {
                        'allowExpressions': true,
                    },
                ],
                '@typescript-eslint/member-ordering': ['error'],
                'space-in-parens': ['error'],
                'no-irregular-whitespace': ['error'],
                'prettier/prettier': ['error'],
                // "newline-per-chained-call": ["error"],
                'import/no-duplicates': 'error',
            },
        },
        {
            files: ['ar.ts', 'en.ts'],
            parserOptions: {
                tsconfigRootDir: __dirname,
                project: ['./tsconfig.json'],
            },
            extends: [
                'plugin:@angular-eslint/recommended',
                'plugin:@angular-eslint/template/process-inline-templates',
            ],
            rules: {
                '@typescript-eslint/naming-convention': [
                    'error',
                    {
                        'selector': 'variable',
                        'format': ['snake_case'],
                    },
                ],
            },
        },
        {
            files: ['*.html'],
            extends: ['plugin:@angular-eslint/template/recommended'],
            rules: {},
        },
    ],
};
