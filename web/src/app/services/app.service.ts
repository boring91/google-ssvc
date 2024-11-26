import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map, Observable } from 'rxjs';
import { SsvcEvaluationResult, Task } from '../types';
import { environment } from '../../environments/environment';

@Injectable()
export class AppService {
    public constructor(private readonly httpClient: HttpClient) {}

    public evaluate(cveId: string): Observable<SsvcEvaluationResult> {
        return this.httpClient.get<SsvcEvaluationResult>(
            `${environment.apiUrl}/ssvc/evaluate/${cveId}`,
        );
    }

    public listTasks(): Observable<Task[]> {
        return this.httpClient.get<Task[]>(
            `${environment.apiUrl}/ssvc/bulk-evaluate`,
        );
    }

    public getTask(taskId: string): Observable<Task> {
        return this.httpClient.get<Task>(
            `${environment.apiUrl}/ssvc/bulk-evaluate/${taskId}`,
        );
    }

    public startTask(file: File): Observable<string> {
        const formData = new FormData();
        formData.append('file', file);

        return this.httpClient
            .post<{ taskId: string }>(
                `${environment.apiUrl}/ssvc/bulk-evaluate`,
                formData,
                {
                    headers: {
                        // Don't set Content-Type header - browser will set it automatically with boundary
                        Accept: 'application/json',
                    },
                },
            )
            .pipe(map(data => data.taskId));
    }
}
