import json
from dataclasses import dataclass, asdict
from typing import Literal, Optional

import concurrent.futures
import pandas as pd

from database.db import Db
from ssvc.evaluation_aggregators.automatability_evaluation_aggregator import AutomatabilityEvaluationAggregator
from ssvc.evaluation_aggregators.exploitation_evaluation_aggregator import ExploitationEvaluationAggregator
from ssvc.evaluation_aggregators.exposure_evaluation_aggregator import ExposureEvaluationAggregator
from ssvc.evaluation_aggregators.mission_impact_evaluation_aggregator import MissionImpactEvaluationAggregator
from ssvc.evaluation_aggregators.mission_prevalence_evaluation_aggregator import MissionPrevalenceEvaluationAggregator
from ssvc.evaluation_aggregators.public_wellbeing_evaluation_aggregator import PublicWellbeingEvaluationAggregator
from ssvc.evaluation_aggregators.technical_impact_evaluation_aggregator import TechnicalImpactEvaluationAggregator
from ssvc.evaluation_aggregators.value_density_evaluation_aggregator import ValueDensityEvaluationAggregator
from ssvc.evaluation_units.evaluation_unit import EvaluationResult
from ssvc.utils import from_json


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

    def evaluate(self, cve_id: str, reevaluate: bool = False) -> Optional[SsvcEvaluationResult]:
        if not reevaluate:
            # Check the cache first
            with Db() as db:
                result = db.first('SELECT * FROM ssvc_results WHERE cve_id=%s', (cve_id,))
                if result is not None:
                    return from_json(result['result'], SsvcEvaluationResult)
        else:
            with Db() as db:
                db.execute('DELETE FROM ssvc_results WHERE cve_id=%s', (cve_id,))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = dict(
                executor.map(lambda x: (x[0], x[1].aggregate(cve_id, reevaluate)), self._aggregators.items()))

        if results is None or any(r is None for r in results.values()):
            print('One of them is none')
            return None

        print()

        mission_prevalence_wellbeing = self._mission_prevalence_wellbeing_df.loc[
            results['mission_prevalence'].assessment, results['public_wellbeing'].assessment]

        action = self._tree_df[
            (self._tree_df['exploitation'] == results['exploitation'].assessment) &
            (self._tree_df['automatability'] == results['automatability'].assessment) &
            (self._tree_df['technical_impact'] == results['technical_impact'].assessment) &
            (self._tree_df['mission_and_wellbeing'] == mission_prevalence_wellbeing)].values[0][-1]

        result = SsvcEvaluationResult(
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

        # Cache the result:
        with Db() as db:
            db.execute('INSERT INTO ssvc_results(cve_id, result) VALUES (%s, %s)',
                       (cve_id, json.dumps(asdict(result))))

        return result
