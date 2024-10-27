from app.ssvc.llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class MissionPrevalenceLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'mission_prevalence'

    def _get_question(self) -> str:
        return """What is the Impact on Mission Essential Functions of Relevant Entities? I.e., whether the 
        vulnerability affects a critical component for business continuity or fulfilling essential missions such as
         protecting critical infrastructure?"""

    def _get_description(self) -> str:
        return """Your answer should be either "minimal", "support", or "essential". Consider the following during your 
        evaluation.
        - A mission essential function (MEF) is a function “directly related to accomplishing the organization’s 
        mission as set forth in its statutory or executive charter.”
        - Identifying MEFs is part of business continuity planning or crisis planning. In contrast to non-essential 
        functions, an organization “must perform a [MEF] during a disruption to normal operations.”
        - The mission is the reason an organization exists, and MEFs are how that mission is realized. Nonessential 
        functions support the smooth delivery or success of MEFs rather than directly supporting the mission.
        
        Also consider this:
        - Mission prevalence is more than simply counting devices or products present. 
        - If only a few devices are impacted, but they directly provide essential functions, then this criticality is 
        what is important.
        - Quantity may still be an important consideration. Sometimes being ubiquitous is enough to directly provide 
        essential functions. Examples for the right level of detail for a “mission” are “protect critical 
        infrastructure” or “perform health inspections.” 
        - This feature measures prevalence, not impact, so it does not need to account for any compensating controls or 
        the impact of the vulnerability on the component. (Technical impact and automatable already measure the 
        relevant features.)
        """
