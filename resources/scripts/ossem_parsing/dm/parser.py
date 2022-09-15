"""
Module with functions to handle the common data model
"""

import os
import yaml

DEFAULT_IGNORED_FILE_OR_DIR = ['_all_ossem_relationships.yml']

def get_detection_model(path: str, ignored_file_or_dir=DEFAULT_IGNORED_FILE_OR_DIR) -> dict[str, dict]:
    """
    Function that returns a flat dictionary with the relationship definitions

    **Parameters**:

    - **path**: path to the directory containing the relationship files
    """

    result = {}

    for file_or_dir in os.listdir(path):

        if file_or_dir in ignored_file_or_dir:
            continue

        file_or_dir_path = os.path.join(path, file_or_dir)
        # print(f"parsing {file_or_dir_path}")

        if os.path.isfile(file_or_dir_path):
            with open(file_or_dir_path, "rb") as detection_model_file:
                file_or_dir_dot_split = file_or_dir.split('.')

                if file_or_dir_dot_split[-1] not in ['yml', "yaml"]:
                    continue

                detection_model_value = yaml.safe_load(detection_model_file)
                detection_model_key = detection_model_value["name"]
                result[detection_model_key] = detection_model_value

    return result