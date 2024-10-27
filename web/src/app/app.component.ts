import {
    ChangeDetectionStrategy,
    Component,
    model,
    signal,
} from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ApiError, SsvcEvaluationResult } from './types';
import { AppService } from './services/app.service';
import { FormsModule } from '@angular/forms';
import { JsonPipe, NgClass } from '@angular/common';
import { catchError, finalize, throwError } from 'rxjs';
import { ErrorMessageComponent, ResultCardComponent } from './components';
import { assessmentStyles } from './constants';
import { staggeredFadeIn } from './animations';

@Component({
    selector: 'app-root',
    standalone: true,
    templateUrl: './app.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    animations: [staggeredFadeIn],
    imports: [
        RouterOutlet,
        FormsModule,
        JsonPipe,
        NgClass,
        ResultCardComponent,
        ErrorMessageComponent,
    ],
    styles: [
        `
            @keyframes blink {
                0%,
                100% {
                    border-color: transparent;
                }
                50% {
                    border-color: rgb(96, 165, 250);
                }
            }
        `,
    ],
})
export class AppComponent {
    protected cveId = model<string>();
    protected readonly isSubmitting = signal<boolean>(false);
    protected readonly result = signal<SsvcEvaluationResult | undefined>(
        undefined,
    );
    protected readonly error = signal<ApiError | undefined>(undefined);

    protected readonly assessmentStyles = assessmentStyles;

    public constructor(private readonly appService: AppService) {}

    protected submit(): void {
        if (!this.cveId() || this.isSubmitting()) return;

        this.isSubmitting.set(true);
        this.error.set(undefined);
        this.result.set(undefined);

        this.appService
            .query(this.cveId()!)
            .pipe(
                catchError(err => {
                    let error: ApiError;

                    if (err.status === 404) {
                        error = {
                            status: 404,
                            message: `No data found for CVE ID: ${this.cveId()}`,
                            details: err.error?.message,
                        };
                    } else if (err.status === 429) {
                        error = {
                            status: 429,
                            message:
                                'Too many requests. Please try again later.',
                            details: err.error?.message,
                        };
                    } else {
                        error = {
                            status: err.status || 500,
                            message:
                                'An unexpected error occurred while evaluating the CVE.',
                            details: err.error?.message || err.message,
                        };
                    }

                    this.error.set(error);
                    return throwError(() => error);
                }),
                finalize(() => this.isSubmitting.set(false)),
            )
            .subscribe(result => this.result.set(result));
    }

    protected updateCveId(value: string): void {
        this.cveId.set(value);
        if (this.error()) {
            this.error.set(undefined);
        }
    }
}
