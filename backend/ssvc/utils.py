import json
from typing import Optional, TypeVar, Type

from dacite import from_dict

T = TypeVar('T')


def from_json(json_string: str, data_class: Type[T]) -> T:
    try:
        data = json.loads(json_string)
        return from_dict(data_class=data_class, data=data)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {e}")


def extract_cvss_from_nist(data: dict) -> Optional[str]:
    """
    Given the data return from the nist api, this method
    traverses the returned json and extracts the newest cvss
    string; e.g., if there are cvss4.0 and cvss3.1, the method
    would return the cvss4.0 string.
    """
    if data is None or 'metrics' not in data:
        return None

    metrics = data['metrics']

    versions = ['cvssMetricV40', 'cvssMetricV31', 'cvssMetricV30', 'cvssMetricV2']

    for version in versions:
        if version not in metrics or type(metrics[version]) != list or len(metrics[version]) == 0:
            continue

        for item in metrics[version]:
            if 'cvssData' in item and 'vectorString' in item['cvssData']:
                return item['cvssData']['vectorString']

    return None


def standardize_cvss(cvss: str) -> list[str]:
    """
    This method normalizes some of the fields found in the
    cvss string. Different versions may have different field
    names that represent the same data. For example the Integrity
    impact in v3.0 has the field name `I`, whereas in v4.0, it has
    the field name `VI`. The method would map it to `VI` regardless
    of the version.
    """
    cvss = dict(map(lambda x: x.split(':'), cvss.split('/')))

    replacements = [('C', 'VC'), ('I', 'VI'), ('A', 'VA')]
    for r in replacements:
        if r[0] in cvss and r[1] not in cvss:
            cvss[r[1]] = cvss.pop(r[0])

    return list(map(lambda x: f'{x[0]}:{x[1]}', cvss.items()))
