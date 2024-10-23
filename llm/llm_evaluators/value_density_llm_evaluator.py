from llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class ValueDensityLlmEvaluator(BaseLlmEvaluator):
    def _get_question(self) -> str:
        return "What is the Value Density of the given CVE? In other words, the concentration of value in the target?"

    def _get_description(self) -> str:
        return """Your assessment should be either "diffuse" or "concentrated". Your assessment methodology should 
        follow these rules:
            - You should assess a CVE with "diffuse" if:
                * The system that contains the vulnerable component has limited resources. That is, the resources that 
                the adversary will gain control over with a single exploitation event are relatively small. Examples of 
                systems with diffuse value are email accounts, most consumer online banking accounts, common cell 
                phones, and most personal computing resources owned and maintained by users.
                
            - You should assess a CVE with "concentrated" if:
                * The system that contains the vulnerable component is rich in resources. Heuristically, such systems 
                are often the direct responsibility of “system operators” rather than users. Examples of concentrated 
                value are database systems, Kerberos servers, web servers hosting login pages, and cloud service 
                providers. However, usefulness and uniqueness of the resources on the vulnerable system also inform 
                value density. For example, encrypted mobile messaging platforms may have concentrated value, not 
                because each phone’s messaging history has a particularly large amount of data, but because it is 
                uniquely valuable to law enforcement."""
