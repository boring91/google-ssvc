import { SsvcTaskResult } from './ssvc-task-result.type';

export type Task = {
    id: string;
    createdTime: Date;
    modifiedTime: Date;
    status: 'queued' | 'running' | 'succeeded' | 'failed';
    data: string[];
    results: SsvcTaskResult[];
};
