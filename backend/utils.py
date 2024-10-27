from dataclasses import asdict


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
