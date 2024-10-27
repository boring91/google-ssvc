from dataclasses import dataclass
from typing import Literal, Optional

import pandas as pd

from evaluation_aggregators.automatability_evaluation_aggregator import AutomatabilityEvaluationAggregator
from evaluation_aggregators.exploitation_evaluation_aggregator import ExploitationEvaluationAggregator
from evaluation_aggregators.exposure_evaluation_aggregator import ExposureEvaluationAggregator
from evaluation_aggregators.mission_impact_evaluation_aggregator import MissionImpactEvaluationAggregator
from evaluation_aggregators.mission_prevalence_evaluation_aggregator import MissionPrevalenceEvaluationAggregator
from evaluation_aggregators.public_wellbeing_evaluation_aggregator import PublicWellbeingEvaluationAggregator
from evaluation_aggregators.technical_impact_evaluation_aggregator import TechnicalImpactEvaluationAggregator
from evaluation_aggregators.value_density_evaluation_aggregator import ValueDensityEvaluationAggregator
from evaluation_units.evaluation_unit import EvaluationResult


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
        self._automatability = AutomatabilityEvaluationAggregator(llm)
        self._exploitation = ExploitationEvaluationAggregator(llm)
        self._exposure = ExposureEvaluationAggregator(llm)
        self._mission_impact = MissionImpactEvaluationAggregator(llm)
        self._mission_prevalence = MissionPrevalenceEvaluationAggregator(llm)
        self._public_wellbeing = PublicWellbeingEvaluationAggregator(llm)
        self._technical_impact = TechnicalImpactEvaluationAggregator(llm)
        self._value_density = ValueDensityEvaluationAggregator(llm)

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
        exploitation = self._exploitation.aggregate(cve_id)
        automatability = self._automatability.aggregate(cve_id)
        technical_impact = self._technical_impact.aggregate(cve_id)

        mission_prevalence = self._mission_prevalence.aggregate(cve_id)
        public_wellbeing = self._public_wellbeing.aggregate(cve_id)

        exposure = self._exposure.aggregate(cve_id)
        mission_impact = self._mission_impact.aggregate(cve_id)
        value_density = self._value_density.aggregate(cve_id)

        if (exploitation is None or automatability is None or technical_impact is None or mission_prevalence is None or
                public_wellbeing is None):
            return None

        mission_prevalence_wellbeing = self._mission_prevalence_wellbeing_df.loc[
            mission_prevalence.assessment, public_wellbeing.assessment]

        action = self._tree_df[
            (self._tree_df['exploitation'] == exploitation.assessment) &
            (self._tree_df['automatability'] == automatability.assessment) &
            (self._tree_df['technical_impact'] == technical_impact.assessment) &
            (self._tree_df['mission_and_wellbeing'] == mission_prevalence_wellbeing)].values[0][-1]

        return SsvcEvaluationResult(
            action,
            automatability,
            exploitation,
            exposure,
            mission_impact,
            mission_prevalence,
            public_wellbeing,
            technical_impact,
            value_density
        )
