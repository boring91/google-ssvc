import {
    animate,
    query,
    stagger,
    style,
    transition,
    trigger,
} from '@angular/animations';

export const staggeredFadeIn = trigger('staggeredFadeIn', [
    transition(':enter', [
        query('.card-item', [
            style({ opacity: 0, transform: 'translateY(20px)' }),
            stagger('50ms', [
                animate(
                    '300ms ease-out',
                    style({ opacity: 1, transform: 'translateY(0)' }),
                ),
            ]),
        ]),
    ]),
]);
