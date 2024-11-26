import {
    ChangeDetectionStrategy,
    Component,
    model,
    signal,
} from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { JsonPipe, NgClass } from '@angular/common';
import { catchError, finalize, throwError } from 'rxjs';
import {
    DecisionPointResultCardComponent,
    ErrorMessageComponent,
    SsvcResultGridComponent,
} from '../../components';
import { ApiError, SsvcEvaluationResult } from '../../types';
import { assessmentStyles } from '../../constants';
import { AppService } from '../../services/app.service';

type InputMethod = 'single' | 'bulk';

@Component({
    selector: 'app-home-page',
    standalone: true,
    templateUrl: './home-page.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
    imports: [
        RouterOutlet,
        FormsModule,
        JsonPipe,
        NgClass,
        DecisionPointResultCardComponent,
        ErrorMessageComponent,
        SsvcResultGridComponent,
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
export class HomePageComponent {
    protected cveId = model<string>();
    protected readonly isSubmitting = signal<boolean>(false);
    protected readonly result = signal<SsvcEvaluationResult | undefined>(
        undefined,
    );
    protected readonly error = signal<ApiError | undefined>(undefined);
    protected readonly inputMethod = signal<InputMethod>('single');
    protected readonly isDragging = signal<boolean>(false);
    protected readonly selectedFile = signal<File | undefined>(undefined);

    protected readonly assessmentStyles = assessmentStyles;

    public constructor(
        private readonly appService: AppService,
        private readonly router: Router,
    ) {}

    protected submit(): void {
        if (this.isSubmitting()) return;

        if (this.inputMethod() === 'single' && !this.cveId()) return;
        if (this.inputMethod() === 'bulk' && !this.selectedFile()) return;

        this.isSubmitting.set(true);
        this.error.set(undefined);
        this.result.set(undefined);

        if (this.inputMethod() === 'single') {
            this.submitSingle();
        } else {
            this.submitBulk();
        }
    }

    protected updateCveId(value: string): void {
        this.cveId.set(value);
        if (this.error()) {
            this.error.set(undefined);
        }
    }

    protected setInputMethod(method: InputMethod): void {
        this.inputMethod.set(method);
        this.error.set(undefined);
        this.result.set(undefined);
        this.cveId.set('');
        this.selectedFile.set(undefined);
    }

    protected handleFileSelect(event: Event): void {
        const input = event.target as HTMLInputElement;
        const file = input.files?.[0];
        this.setSelectedFile(file);
    }

    protected handleDragOver(event: DragEvent): void {
        event.preventDefault();
        event.stopPropagation();
        this.isDragging.set(true);
    }

    protected handleDragLeave(event: DragEvent): void {
        event.preventDefault();
        event.stopPropagation();
        this.isDragging.set(false);
    }

    protected handleDrop(event: DragEvent): void {
        event.preventDefault();
        event.stopPropagation();
        this.isDragging.set(false);

        const file = event.dataTransfer?.files[0];
        this.setSelectedFile(file);
    }

    protected clearFile(event: MouseEvent): void {
        event.preventDefault();
        event.stopPropagation();
        this.selectedFile.set(undefined);
    }

    private submitSingle(): void {
        this.appService
            .evaluate(this.cveId()!)
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
                            details: err.error?.detail || err.detail,
                        };
                    }

                    this.error.set(error);
                    return throwError(() => error);
                }),
                finalize(() => this.isSubmitting.set(false)),
            )
            .subscribe(result => this.result.set(result));
    }

    private submitBulk(): void {
        const file = this.selectedFile();
        if (!file) return;

        const reader = new FileReader();
        reader.onload = e => {
            const text = e.target?.result as string;
            const cveIds = this.parseCsvContent(text);

            // TODO: Implement bulk processing logic
            // For now, just process the first CVE as an example
            this.appService.startTask(file).subscribe(async taskId => {
                await this.router.navigate(['', 'tasks', taskId]);
            });
        };
        reader.onerror = e => {
            this.error.set({
                status: 400,
                message: 'Failed to read the CSV file',
                details: e.target?.error?.message,
            });
            this.isSubmitting.set(false);
        };
        reader.readAsText(file);
    }

    private parseCsvContent(content: string): string[] {
        return content
            .split('\n')
            .map(line => line.trim())
            .filter(
                line =>
                    line.length > 0 && line.toUpperCase().startsWith('CVE-'),
            );
    }

    private setSelectedFile(file: File | undefined): void {
        if (file && file.type === 'text/csv') {
            this.selectedFile.set(file);
            this.error.set(undefined);
        } else {
            this.error.set({
                status: 400,
                message: 'Invalid file type',
                details: 'Please upload a CSV file',
            });
        }
    }
}
