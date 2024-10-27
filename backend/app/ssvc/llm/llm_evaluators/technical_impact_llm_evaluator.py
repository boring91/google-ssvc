from app.ssvc.llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class TechnicalImpactLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'technical_impact'

    def _get_question(self) -> str:
        return "What is the Technical Impact of exploiting the given CVE?"

    def _get_description(self) -> str:
        return """Your assessment should be either "partial" or "total". When evaluating technical impact, the 
        definition of "scope" is particularly important which includes:
            - How the boundaries of the affected system are set.
            - Whose security policy is relevant.
            - How far forward in time or causal steps one reasons about effects and harms.
        
        If an answer to one of the following questions is yes, then your assessment should be "total":
            - Can the attacker install and run arbitrary software?
            - Can the attacker trigger all the actions that the vulnerable component can perform?
            - Does the attacker get an account with full privileges to the vulnerable component (administrator or root
             user accounts, for example)?
        """
