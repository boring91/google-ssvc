from dataclasses import asdict
from typing import Optional


def extract_cvss_from_nist(data: dict) -> Optional[str]:
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
    cvss = dict(map(lambda x: x.split(':'), cvss.split('/')))

    replacements = [('C', 'VC'), ('I', 'VI'), ('A', 'VA')]
    for r in replacements:
        if r[0] in cvss and r[1] not in cvss:
            cvss[r[1]] = cvss.pop(r[0])

    return list(map(lambda x: f'{x[0]}:{x[1]}', cvss.items()))


def dataclass_to_camelcase_dict(obj: any) -> dict:
    def snake_to_camel(snake_str: str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def convert_keys_to_camel_case(snake_dict: dict):
        camel_dict = {}
        for key, value in snake_dict.items():
            camel_key = snake_to_camel(key)
            if isinstance(value, dict):
                value = convert_keys_to_camel_case(value)
            camel_dict[camel_key] = value
        return camel_dict

    return convert_keys_to_camel_case(asdict(obj))
