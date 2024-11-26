import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
    selector: 'app-logo',
    templateUrl: 'logo.component.html',
    standalone: true,
    changeDetection: ChangeDetectionStrategy.OnPush,
    styles: `
        :host {
            display: block;
        }
    `,
})
export class LogoComponent {}
