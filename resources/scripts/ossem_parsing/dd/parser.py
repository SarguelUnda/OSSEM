"""
Module that provides functions useful for:
- creating a 'flat' for parsing data dictionaries, and generating a flat collection of them
- standardizing events using the generated flat data dicitionaries collections
"""

import os
import yaml
import sys

DEFAULT_IGNORED_FILE_OR_DIR = ['ressources', ".git"]

def get_data_dictionaries(path: str, ignored_file_or_dir=DEFAULT_IGNORED_FILE_OR_DIR):
    """
    Recursive function that returns the parsed data dictionaries within a directory

    **Parameters**:

    - **path**: path of the directory that contains all of the data dictionaries
    - **ignored_directories**: directories to ignore when parsing the data dictionaries in `path`
    """
    result = {}

    for file_or_dir in os.listdir(path):

        if file_or_dir in ignored_file_or_dir:
            continue

        file_or_dir_path = os.path.join(path, file_or_dir)

        # Directory - Recurse
        if os.path.isdir(file_or_dir_path):
            print(f"visiting {file_or_dir_path}", file=sys.stderr)
            result.update(get_data_dictionaries(file_or_dir_path, ignored_file_or_dir))

        # File - Parse, and add to data_dictionary
        else:
            with open(file_or_dir_path, "rb") as data_dictionary_file:
                file_name_dot_split = file_or_dir_path.split('.')

                if file_name_dot_split[-1] not in ['yml', "yaml"]:
                    continue

                data_dictionary_key = "".join(file_name_dot_split[:-1])
                data_dictionary_value = yaml.safe_load(data_dictionary_file)

                result[data_dictionary_key] = data_dictionary_value

    return result
