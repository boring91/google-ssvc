import { Component, input, signal } from '@angular/core';

@Component({
    selector: 'app-error-message',
    standalone: true,
    templateUrl: 'error-message.component.html',
})
export class ErrorMessageComponent {
    public title = input.required<string>();
    public message = input.required<string>();
    public details = input<string | undefined>();

    protected readonly showDetails = signal(false);

    protected toggleDetails(): void {
        this.showDetails.update(value => !value);
    }
}
