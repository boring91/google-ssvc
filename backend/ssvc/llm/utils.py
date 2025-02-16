import json
import re
from typing import Optional


def parse_llm_response(llm_response: str, ensure_assessment: bool = True) -> Optional[dict]:
    # noinspection PyBroadException
    try:
        cleaned = llm_response.replace('\n', '').replace('\t', '')
        pattern = r'(?:```json)?(\{.+?\})(?:```)?'
        match = re.search(pattern, cleaned)

        if match:
            captured_group = match.group(1)
            result: dict = json.loads(captured_group)

            if not ensure_assessment:
                return result

            if 'assessment' in result:
                return result

            return None

        else:
            return None

    except:
        return None
