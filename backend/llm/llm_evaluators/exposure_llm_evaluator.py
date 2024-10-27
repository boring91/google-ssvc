from llm.llm_evaluators.base_llm_evaluator import BaseLlmEvaluator


class ExposureLlmEvaluator(BaseLlmEvaluator):
    @staticmethod
    def name() -> str:
        return 'exposure'

    def _get_question(self) -> str:
        return "What is the accessible attack surface of the affected system or service? i.e., the Exposure of the CVE?"

    def _get_description(self) -> str:
        return """Your answer should be either "small", "controlled", or "open". Consider the following during your 
        evaluation.
        - Measuring the attack surface precisely is difficult, and it is not suggested to perfectly delineate between 
        small and controlled access.
        - Exposure should be judged against the system in its deployed context, which may differ from how it is 
        commonly expected to be deployed.
        - System Exposure is primarily used by Deployers, so the question is about whether some specific system is 
        in fact exposed, not a hypothetical or aggregate question about systems of that type. Therefore, it generally 
        has a concrete answer, even though it may vary from vulnerable component to vulnerable component, based on 
        their respective configurations.
        - System Exposure can be readily informed by network scanning techniques. Network policy or diagrams are also 
        useful information sources, especially for services intentionally open to the Internet such as public web 
        servers.
        
        Also consider this:
        Distinguishing between small and controlled is more nuanced. If open has been ruled out, some suggested 
        heuristics for differentiating the other two are as follows. 
        Apply these heuristics in order and stop when one of them applies. 
        - If the system's networking and communication interfaces have been physically removed or disabled, 
        choose small.
        - If Automatable is yes, then choose controlled. 
        - If the vulnerable component is on a network where other hosts can browse the web or receive email, choose 
        controlled.
        - If the vulnerable component is in a third-party library that is unreachable because the feature is unused in 
        the surrounding product, choose small.
        """
