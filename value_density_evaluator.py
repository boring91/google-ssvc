from base_evaluator import BaseEvaluator


class ValueDensityEvaluator(BaseEvaluator):
    def _get_prompt(self, cve_id: str, cve_data: str) -> str:
        return f"""I am going to give you an ID of a specific ID and some data related to that CVE in a json format. The json
        object has at its roots properties that represent different data sources, each property of these is assigned
        to another json object that represent the information about the given CVE from that data source. Your role is
        to use the provided information from these data sources and answer the following question:
        
        "What is the Value Density of the given CVE? In other words, the concentration of value in the target?
        
        Your answer should be either "diffuse" or "concentrated". Your assessment methodology should follow
        these rules:
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
                uniquely valuable to law enforcement.
                
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
