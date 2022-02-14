/**
 * Sources: https://react.i18next.com/latest/typescript
 */

import { resources } from './i18n';

// react-i18next versions higher than 11.11.0
declare module 'react-i18next' {
    interface CustomTypeOptions {
        resources: typeof resources['en'];
    }
}