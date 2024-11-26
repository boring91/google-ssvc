from dataclasses import asdict
from typing import Optional, Any, Union, Dict, List


def dataclass_to_camelcase_dict(obj: Optional[Union[Any, Dict, List]]) -> Optional[Union[Dict, List]]:
    """
    Convert a dataclass object, dictionary, list of dataclasses, or list of dictionaries
    to a dictionary/list with camelCase keys. Handles nested structures by recursively
    converting their contents.

    Args:
        obj: A dataclass instance, dictionary, list of dataclasses, list of dictionaries,
             or None. If None, returns None.

    Returns:
        Optional[Union[Dict, List]]: A dictionary/list with all keys converted to camelCase,
                                   or None if the input is None.

    Examples:
        >>> @dataclass
        >>> class Address:
        >>>     postal_code: str
        >>>
        >>> @dataclass
        >>> class User:
        >>>     first_name: str
        >>>     addresses: list[Address]
        >>>
        >>> # Example with dataclass
        >>> user = User(first_name="John", addresses=[Address(postal_code="12345")])
        >>> dataclass_to_camelcase_dict(user)
        >>> {'firstName': 'John', 'addresses': [{'postalCode': '12345'}]}
        >>>
        >>> # Example with list of dataclasses
        >>> addresses = [Address(postal_code="12345"), Address(postal_code="67890")]
        >>> dataclass_to_camelcase_dict(addresses)
        >>> [{'postalCode': '12345'}, {'postalCode': '67890'}]
        >>>
        >>> # Example with dictionary
        >>> data = {"first_name": "John", "postal_code": "12345"}
        >>> dataclass_to_camelcase_dict(data)
        >>> {'firstName': 'John', 'postalCode': '12345'}
        >>>
        >>> # Example with list of dictionaries
        >>> data_list = [{"postal_code": "12345"}, {"postal_code": "67890"}]
        >>> dataclass_to_camelcase_dict(data_list)
        >>> [{'postalCode': '12345'}, {'postalCode': '67890'}]
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

    def convert_keys_to_camel_case(data: Any) -> Any:
        """
        Recursively convert all dictionary keys from snake_case to camelCase,
        including those in nested dictionaries and arrays.

        Args:
            data: Any data structure that might contain dictionaries or lists

        Returns:
            Any: The input data structure with all dictionary keys converted to camelCase
        """
        if isinstance(data, dict):
            return {
                snake_to_camel(key): convert_keys_to_camel_case(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [convert_keys_to_camel_case(item) for item in data]
        return data

    def try_convert_to_dict(item: Any) -> Any:
        """
        Try to convert an item to a dictionary if it's a dataclass,
        otherwise return the item unchanged.

        Args:
            item: Any item that might be a dataclass

        Returns:
            Any: The converted dictionary if item was a dataclass, or the original item
        """
        try:
            return asdict(item)
        except (TypeError, AttributeError):
            return item

    # If input is a list, try to convert each item to dict first
    if isinstance(obj, list):
        converted_list = [try_convert_to_dict(item) for item in obj]
        return convert_keys_to_camel_case(converted_list)

    # If input is already a dict, convert it directly
    if isinstance(obj, dict):
        return convert_keys_to_camel_case(obj)

    # Try to convert as a single dataclass
    try:
        return convert_keys_to_camel_case(asdict(obj))
    except (TypeError, AttributeError):
        raise ValueError(
            "Input must be a dataclass instance, dictionary, list of dataclasses, "
            "list of dictionaries, or None"
        )
