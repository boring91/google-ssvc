export type EvaluationResult<T> = {
    assessment: T;
    confidence: number;
    justification: string;
    links?: string[];
};
