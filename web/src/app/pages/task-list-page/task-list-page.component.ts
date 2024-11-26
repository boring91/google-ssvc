import { ChangeDetectionStrategy, Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { Task } from '../../types';
import { AppService } from '../../services/app.service';
import { TimeAgoPipe } from '../../pipes/time-ago.pipe';

@Component({
    selector: 'app-task-list-page',
    templateUrl: 'task-list-page.component.html',
    standalone: true,
    changeDetection: ChangeDetectionStrategy.OnPush,
    imports: [CommonModule, RouterLink, TimeAgoPipe],
})
export class TaskListPageComponent {
    protected readonly tasks = signal<Task[] | undefined>(undefined);

    public constructor(appService: AppService) {
        appService.listTasks().subscribe(items => this.tasks.set(items));
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
}
