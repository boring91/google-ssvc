from dataclasses import asdict
from typing import Optional


def dataclass_to_camelcase_dict(obj: Optional[any]) -> Optional[dict]:
    """
    Convert a dataclass object to a dictionary with camelCase keys.
    Handles nested dictionaries by recursively converting their keys as well.

    Args:
        obj: A dataclass instance or None. If None, returns None.

    Returns:
        Optional[dict]: A dictionary with all keys converted to camelCase,
                       or None if the input is None.

    Examples:
        >>> @dataclass
        >>> class User:
        >>>     first_name: str
        >>>     last_name: str
        >>>
        >>> user = User(first_name="John", last_name="Doe")
        >>> dataclass_to_camelcase_dict(user)
        >>> {'firstName': 'John', 'lastName': 'Doe'}
    """
    if obj is None:
        return obj

    def snake_to_camel(snake_str: str) -> str:
        """
        Convert a snake_case string to camelCase.

        Args:
            snake_str: A string in snake_case format

        Returns:
            str: The input string converted to camelCase

        Examples:
            >>> snake_to_camel("first_name")
            >>> "firstName"
        """
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def convert_keys_to_camel_case(snake_dict: dict) -> dict:
        """
        Recursively convert all dictionary keys from snake_case to camelCase.

        Args:
            snake_dict: A dictionary with snake_case keys

        Returns:
            dict: A new dictionary with all keys converted to camelCase,
                 including keys in nested dictionaries

        Examples:
            >>> convert_keys_to_camel_case({"first_name": "John", "address_info": {"postal_code": "12345"}})
            >>> {"firstName": "John", "addressInfo": {"postalCode": "12345"}}
        """
        camel_dict = {}
        for key, value in snake_dict.items():
            camel_key = snake_to_camel(key)
            if isinstance(value, dict):
                value = convert_keys_to_camel_case(value)
            camel_dict[camel_key] = value
        return camel_dict

    return convert_keys_to_camel_case(asdict(obj))
