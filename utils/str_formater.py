import re


def convert_camel_to_snake(input_string: str) -> str:
    snake_case = re.sub('([a-z])([A-Z])', r'\1_\2', input_string).lower()
    return snake_case
