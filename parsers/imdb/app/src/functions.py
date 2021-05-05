import json
from pathlib import Path


def read_html_file(path_to_file: Path) -> str:
    data: str = ''
    with open(path_to_file, 'r') as file:
        data = file.read()
    return data


def write_json_file(data: dict, path_to_file: Path) -> None:
    with open(path_to_file, 'w') as file:
        json.dump(data, file)
