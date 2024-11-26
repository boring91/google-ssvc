import { SsvcEvaluationResult } from './ssvc-evaluation-result.type';

export type SsvcTaskResult = {
    createdTime: string;
    cveId: string;
    notes?: string;
    result?: SsvcEvaluationResult;
};
