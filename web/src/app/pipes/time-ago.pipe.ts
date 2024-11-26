import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'timeAgo',
    standalone: true,
})
export class TimeAgoPipe implements PipeTransform {
    public transform(value: string | Date): string {
        const date = value instanceof Date ? value : new Date(value);
        const now = new Date();
        const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

        const intervals = {
            year: 31536000,
            month: 2592000,
            week: 604800,
            day: 86400,
            hour: 3600,
            minute: 60,
            second: 1,
        } as const;

        for (const [unit, secondsInUnit] of Object.entries(intervals)) {
            const interval = Math.floor(seconds / secondsInUnit);

            if (interval >= 1) {
                return interval === 1
                    ? `1 ${unit} ago`
                    : `${interval} ${unit}s ago`;
            }
        }

        return 'just now';
    }
}
