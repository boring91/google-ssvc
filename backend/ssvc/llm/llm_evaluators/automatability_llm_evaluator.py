from ssvc.llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class AutomatabilityLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'automatability'

    def _get_question(self) -> str:
        return "Is the CVE automateble?"

    def _get_description(self) -> str:
        return """Your answer should be either "yes" or "no". Your assessment methodology should follow
        these rules:
            - You should assess a CVE with "no" if all of the following applies:
                * The vulnerable component is not searchable or enumerable on the network.
                * Weaponization may require human direction for each target.
                * Delivery may require channels that widely deployed network security configurations block.
                * Exploitation is not reliable, due to exploit-prevention techniques (e.g., ASLR) enabled by default.
                
            - You should assess a CVE with "yes" if:
                * The vulnerability allows remote code execution or command injection."""
