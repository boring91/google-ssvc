import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SsvcEvaluationResult } from '../types';
import { environment } from '../environments/environment';

@Injectable()
export class AppService {
    public constructor(private readonly httpClient: HttpClient) {}

    public query(cveId: string): Observable<SsvcEvaluationResult> {
        return this.httpClient.get<SsvcEvaluationResult>(
            `${environment.apiUrl}/query/${cveId}`,
        );
    }
}
