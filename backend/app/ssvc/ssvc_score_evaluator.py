from dataclasses import dataclass
from typing import Literal, Optional

import pandas as pd

from app.ssvc.evaluation_aggregators.automatability_evaluation_aggregator import AutomatabilityEvaluationAggregator
from app.ssvc.evaluation_aggregators.exploitation_evaluation_aggregator import ExploitationEvaluationAggregator
from app.ssvc.evaluation_aggregators.exposure_evaluation_aggregator import ExposureEvaluationAggregator
from app.ssvc.evaluation_aggregators.mission_impact_evaluation_aggregator import MissionImpactEvaluationAggregator
from app.ssvc.evaluation_aggregators.mission_prevalence_evaluation_aggregator import MissionPrevalenceEvaluationAggregator
from app.ssvc.evaluation_aggregators.public_wellbeing_evaluation_aggregator import PublicWellbeingEvaluationAggregator
from app.ssvc.evaluation_aggregators.technical_impact_evaluation_aggregator import TechnicalImpactEvaluationAggregator
from app.ssvc.evaluation_aggregators.value_density_evaluation_aggregator import ValueDensityEvaluationAggregator
from app.ssvc.evaluation_units.evaluation_unit import EvaluationResult


@dataclass
class SsvcEvaluationResult:
    action: Literal['track', 'track*', 'attend', 'act']
    automatability: EvaluationResult
    exploitation: EvaluationResult
    exposure: EvaluationResult
    mission_impact: EvaluationResult
    mission_prevalence: EvaluationResult
    public_wellbeing: EvaluationResult
    technical_impact: EvaluationResult
    value_density: EvaluationResult


class SsvcScoreEvaluator:
    def __init__(self, llm: Literal['gemini', 'openai'] = 'gemini'):
        # self._automatability = AutomatabilityEvaluationAggregator(llm)
        # self._exploitation = ExploitationEvaluationAggregator(llm)
        # self._exposure = ExposureEvaluationAggregator(llm)
        # self._mission_impact = MissionImpactEvaluationAggregator(llm)
        # self._mission_prevalence = MissionPrevalenceEvaluationAggregator(llm)
        # self._public_wellbeing = PublicWellbeingEvaluationAggregator(llm)
        # self._technical_impact = TechnicalImpactEvaluationAggregator(llm)
        # self._value_density = ValueDensityEvaluationAggregator(llm)

        self._aggregators = {
            'automatability': AutomatabilityEvaluationAggregator(llm),
            'exploitation': ExploitationEvaluationAggregator(llm),
            'exposure': ExposureEvaluationAggregator(llm),
            'mission_impact': MissionImpactEvaluationAggregator(llm),
            'mission_prevalence': MissionPrevalenceEvaluationAggregator(llm),
            'public_wellbeing': PublicWellbeingEvaluationAggregator(llm),
            'technical_impact': TechnicalImpactEvaluationAggregator(llm),
            'value_density': ValueDensityEvaluationAggregator(llm)
        }

        self._mission_prevalence_wellbeing_df = pd.DataFrame({
            'minimal': {'minimal': 'low', 'support': 'medium', 'essential': 'high'},
            'material': {'minimal': 'medium', 'support': 'medium', 'essential': 'high'},
            'irreversible': {'minimal': 'high', 'support': 'high', 'essential': 'high'}
        })

        self._tree_df = pd.DataFrame({
            'exploitation': ['none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none', 'none',
                             'none',
                             'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc', 'poc',
                             'active',
                             'active', 'active', 'active', 'active', 'active', 'active', 'active', 'active', 'active',
                             'active',
                             'active'],
            'automatability': ['no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes',
                               'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes',
                               'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes', 'yes', 'yes'],
            'technical_impact': ['partial', 'partial', 'partial', 'total', 'total', 'total', 'partial', 'partial',
                                 'partial',
                                 'total', 'total', 'total', 'partial', 'partial', 'partial', 'total', 'total', 'total',
                                 'partial',
                                 'partial', 'partial', 'total', 'total', 'total', 'partial', 'partial', 'partial',
                                 'total',
                                 'total',
                                 'total', 'partial', 'partial', 'partial', 'total', 'total', 'total'],
            'mission_and_wellbeing': ['low', 'medium', 'high', 'low', 'medium', 'high', 'low', 'medium', 'high', 'low',
                                      'medium', 'high',
                                      'low', 'medium', 'high', 'low', 'medium', 'high', 'low', 'medium', 'high', 'low',
                                      'medium', 'high',
                                      'low', 'medium', 'high', 'low', 'medium', 'high', 'low', 'medium', 'high', 'low',
                                      'medium', 'high'],
            'decision': ['track', 'track', 'track', 'track', 'track', 'track*', 'track', 'track', 'attend', 'track',
                         'track',
                         'attend',
                         'track', 'track', 'track*', 'track', 'track*', 'attend', 'track', 'track', 'attend', 'track',
                         'track*',
                         'attend',
                         'track', 'track', 'attend', 'track', 'attend', 'act', 'attend', 'attend', 'act', 'attend',
                         'act',
                         'act']
        })

    def evaluate(self, cve_id: str) -> Optional[SsvcEvaluationResult]:
        # TODO: for this to work, we need to make data sources singleton and thread safe.
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     results = dict(executor.map(lambda x: (x[0], x[1].aggregate(cve_id)), self._aggregators.items()))

        results = dict(map(lambda x: (x[0], x[1].aggregate(cve_id)), self._aggregators.items()))

        print(results)
        if results is None or any(r is None for r in results):
            return None

        mission_prevalence_wellbeing = self._mission_prevalence_wellbeing_df.loc[
            results['mission_prevalence'].assessment, results['public_wellbeing'].assessment]

        print('mnm', results['exploitation'].assessment)
        print('mnm', results['automatability'].assessment)
        print('mnm', results['technical_impact'].assessment)

        action = self._tree_df[
            (self._tree_df['exploitation'] == results['exploitation'].assessment) &
            (self._tree_df['automatability'] == results['automatability'].assessment) &
            (self._tree_df['technical_impact'] == results['technical_impact'].assessment) &
            (self._tree_df['mission_and_wellbeing'] == mission_prevalence_wellbeing)].values[0][-1]

        return SsvcEvaluationResult(
            action,
            results['automatability'],
            results['exploitation'],
            results['exposure'],
            results['mission_impact'],
            results['mission_prevalence'],
            results['public_wellbeing'],
            results['technical_impact'],
            results['value_density']
        )
