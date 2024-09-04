from base_evaluator import BaseEvaluator


class AutomatabilityEvaluator(BaseEvaluator):
    def _get_prompt(self, cve_id: str, cve_data: str) -> str:
        return f"""I am going to give you an ID of a specific ID and some data related to that CVE in a json format. The json
        object has at its roots properties that represent different data sources, each property of these is assigned
        to another json object that represent the information about the given CVE from that data source. Your role is
        to use the provided information from these data sources and answer the following question: 
        "Is the CVE automateble?". Your answer should be either "yes" or "no". Your assessment methodology should follow
        these rules:
            - You should assess a CVE with "no" if all of the following applies:
                * The vulnerable component is not searchable or enumerable on the network.
                * Weaponization may require human direction for each target.
                * Delivery may require channels that widely deployed network security configurations block.
                * Exploitation is not reliable, due to exploit-prevention techniques (e.g., ASLR) enabled by default.
                
            - You should assess a CVE with "yes" if:
                *  The vulnerability allows remote code execution or command injection.
        
        You answer should be formatted as a json object with two properties: 1) "cve_id" which contains the id of the 
        cve in question, 2) "assessment" which can take one of the three previous values, 3) "justification": explaining 
        how you reached to the answer you provided in the "assessment" property (the description should not refer to the 
        json data but rather talks about the information that led you to this conclusion, aka, avoid saying the json 
        data shows etc. Also avoid giving generic descriptions like: "multiple sources have reported etc." but rather 
        provide concrete descriptions: e.g., name the sources, name the versions or software, provide links if 
        available, etc.), and 4) "confidence": ranges between 0 and 1, which indicates how confident you are in your 
        assessment, 1 being very confident.

        You should only respond with the json object nothing more.

        Here are the two pieces of information:

        CVE ID: {cve_id}
        JSON data: {cve_data}
        """
