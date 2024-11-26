import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { LogoComponent } from './components';

@Component({
    selector: 'app-root',
    standalone: true,
    templateUrl: './app.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    imports: [RouterOutlet, RouterLinkActive, RouterLink, LogoComponent],
})
export class AppComponent {}
