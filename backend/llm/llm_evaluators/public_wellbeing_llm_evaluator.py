from llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class PublicWellbeingLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'public_wellbeing'

    def _get_question(self) -> str:
        return "What is the CVE's impact of affected system compromise on humans?"

    def _get_description(self) -> str:
        return """Your answer should be either "minimal", "material", or "irreversible". Consider the following during 
        your evaluation.
        
        Evaluation should be "irreversible" if any of the following is satisfied:
            - If there is a physical harm, then one or both of the following are true:
                - Multiple fatalities are likely.
                - The cyber-physical system, of which the vulnerable component is a part, is likely lost or destroyed.
            - If there is an environmental harm, then extreme or serious externalities (immediate public health 
            threat, environmental damage leading to small ecosystem collapse, etc.) are imposed o other parties.
            - If there is a financial harm, then social systems (elections, financial grid, etc.) supported by the 
            software are destabilized and potentially collapse.
        
        Evaluation should be 'material' if any of the following is satisfied:
            - If there is a physical harm, then the CVE:
                - Causes physical distress or injury to system users.
                - Introduces occupational safety hazards.
                - Reduces and/or results in failure of cyber-physical system safety margins.
            - If there is an environmental harm, major externalities (property damage, environmental damage, etc.) are 
            imposed on other parties.
            - If there is a financial harm, then financial losses likely lead to bankruptcy of multiple persons.
            - If there is a psychological harm, then Widespread emotional or psychological harm, sufficient to 
            necessitate counseling or therapy, impact populations of people.
            
        Evaluation should be 'minimal' if none of the above was satisified.
        """
