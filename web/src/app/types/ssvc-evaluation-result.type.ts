import { EvaluationResult } from './evaluation-result.type';

export type SsvcEvaluationResult = {
    action: 'track' | 'track*' | 'attend' | 'act';
    automatability: EvaluationResult<'yes' | 'no'>;
    exploitation: EvaluationResult<'none' | 'poc' | 'active'>;
    exposure: EvaluationResult<'small' | 'controlled' | 'open'>;
    missionImpact: EvaluationResult<
        'degraded' | 'mef_support_crippled' | 'mef_failure' | 'mission_failure'
    >;
    missionPrevalence: EvaluationResult<'minimal' | 'support' | 'essential'>;
    publicWellbeing: EvaluationResult<'minimal' | 'material' | 'irreversible'>;
    technicalImpact: EvaluationResult<'partial' | 'total'>;
    valueDensity: EvaluationResult<'centralized' | 'diffused'>;
};
