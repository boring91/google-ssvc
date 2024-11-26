import {
    ChangeDetectionStrategy,
    Component,
    computed,
    DestroyRef,
    inject,
    signal,
} from '@angular/core';
import { SsvcTaskResult, Task } from '../../types';
import { AppService } from '../../services/app.service';
import { ActivatedRoute, Router } from '@angular/router';
import { SsvcResultGridComponent } from '../../components';
import { CommonModule } from '@angular/common';
import { interval, Subscription } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { assessmentStyles } from '../../constants';

type FilterType = 'all' | 'processed' | 'pending';

@Component({
    selector: 'app-task-detail-page',
    templateUrl: 'task-detail-page.component.html',
    standalone: true,
    changeDetection: ChangeDetectionStrategy.OnPush,
    imports: [CommonModule, SsvcResultGridComponent],
})
export class TaskDetailPageComponent {
    protected readonly task = signal<Task | undefined>(undefined);

    // Computed values for the template
    protected readonly progress = computed(() => {
        const task = this.task();
        if (!task?.data.length) return 0;
        return Math.round((task.results.length / task.data.length) * 100);
    });

    protected readonly isComplete = computed(
        () =>
            this.task()?.status === 'succeeded' ||
            this.task()?.status === 'failed',
    );

    protected readonly filteredCves = computed(() => {
        const task = this.task();
        if (!task) return [];

        switch (this.filterType()) {
            case 'processed':
                return task.data.filter(cveId => this.isProcessed(cveId));
            case 'pending':
                return task.data.filter(cveId => !this.isProcessed(cveId));
            default:
                return task.data;
        }
    });

    private readonly destroyRef = inject(DestroyRef);
    private pollingSubscription?: Subscription;
    private readonly POLLING_INTERVAL = 5000; // 5 seconds
    private readonly expandedCves = signal<Set<string>>(new Set());
    private readonly filterType = signal<FilterType>('all');

    public constructor(
        private readonly appService: AppService,
        private readonly activatedRoute: ActivatedRoute,
        private readonly router: Router,
    ) {
        this.load().then();
    }

    private async load(): Promise<void> {
        const taskId = this.activatedRoute.snapshot.paramMap.get('id');
        if (!taskId) {
            await this.router.navigate(['']);
            return;
        }

        // Initial load
        this.appService.getTask(taskId).subscribe(item => {
            this.task.set(item);
            this.setupPolling(taskId);
        });
    }

    private setupPolling(taskId: string): void {
        // Clear any existing polling
        this.pollingSubscription?.unsubscribe();

        // Start polling if task is not complete
        if (!this.isComplete()) {
            this.pollingSubscription = interval(this.POLLING_INTERVAL)
                .pipe(takeUntilDestroyed(this.destroyRef))
                .subscribe(() => {
                    this.appService.getTask(taskId).subscribe(item => {
                        this.task.set(item);
                        if (this.isComplete()) {
                            this.pollingSubscription?.unsubscribe();
                        }
                    });
                });
        }
    }

    protected getStatusClass(status: Task['status']): string {
        const classes = {
            queued: 'text-gray-400',
            running: 'text-blue-400',
            succeeded: 'text-green-400',
            failed: 'text-red-400',
        };
        return classes[status];
    }

    protected getActionClass(action: string): string {
        return assessmentStyles['action'][action];
    }

    protected isProcessed(cveId: string): boolean {
        return this.task()?.results.some(r => r.cveId === cveId) ?? false;
    }

    protected getResult(cveId: string): SsvcTaskResult | undefined {
        return this.task()?.results.find(r => r.cveId === cveId);
    }

    protected isExpanded(cveId: string): boolean {
        return this.expandedCves().has(cveId);
    }

    protected toggleExpanded(cveId: string): void {
        const expanded = this.expandedCves();
        const newExpanded = new Set(expanded);

        if (newExpanded.has(cveId)) {
            newExpanded.delete(cveId);
        } else {
            newExpanded.add(cveId);
        }

        this.expandedCves.set(newExpanded);
    }

    protected expandAll(): void {
        const allCves = new Set(this.filteredCves());
        this.expandedCves.set(allCves);
    }

    protected collapseAll(): void {
        this.expandedCves.set(new Set());
    }

    protected updateFilter(event: Event): void {
        const select = event.target as HTMLSelectElement;
        this.filterType.set(select.value as FilterType);
        this.expandedCves.set(new Set()); // Reset expanded state when filter changes
    }
}
