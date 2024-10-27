from app.ssvc.llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class MissionImpactLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'mission_impact'

    def _get_question(self) -> str:
        return "What is the CVE's Impact on Mission essential functions of the organization?"

    def _get_description(self) -> str:
        return """Your answer should be either "degraded", "mef_support_crippled", "mef_failure", or "mission_failure". 
        Consider the following during your 
        evaluation.
        - A mission essential function (MEF) is a function “directly related to accomplishing the organization’s 
        mission as set forth in its statutory or executive charter”. 
        - Mission Essential Functions are in effect critical activities within an organization that are used to 
        identify key assets, supporting tasks, and resources that an organization requires to remain operational in 
        a crisis's situation, and so must be included in its planning process. 
        - During an event, key resources may be limited, and personnel may be unavailable, so organizations must 
        consider these factors and validate assumptions when identifying, validating, and prioritizing MEFs.
        - When reviewing the list of organizational functions, an organization must first identify whether a function 
        is essential or non-essential. 
        - As mission essential functions are most clearly defined for government agencies, stakeholders in other 
        sectors may be familiar with different terms of art from continuity planning. For example, infrastructure 
        providers in the US may better align with National Critical Functions. Private sector businesses may better 
        align with operational and financial impacts in a business continuity plan.
        
        Also consider this:
        - The factors that influence the mission impact level are diverse.
        - At a minimum, understanding mission impact should include gathering information about the critical paths 
        that involve vulnerable components, viability of contingency measures, and resiliency of the systems that 
        support the mission. There are various sources of guidance on how to gather this information; see for example 
        the FEMA guidance in Continuity Directive 2 1 or OCTAVE FORTE 3. 
        - As a heuristic, Utility might constrain Mission Impact if both are not used in the same decision tree. For 
        example, if the Utility is super effective, then Mission Impact is at least MEF support crippled.
        """
