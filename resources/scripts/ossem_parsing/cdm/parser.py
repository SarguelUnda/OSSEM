"""
Module with functions to handle the common data model
"""

import os
import yaml


def add_reverse_extensions_common_data_model(common_data_model: dict) -> dict:
    """
    Produce a common data model with an added field of reversed_extensions

    **Parameters**:

    - **common_data_model**: a dict representing ossem_commmon_data_model
    """

    for entity_name, entity_schema in common_data_model.items():
        extensions = entity_schema.get("extends_entities", [])

        for extension_schema in [common_data_model[e] for e in extensions if e in common_data_model]:
            extension_schema.setdefault("reverse_extends_entities", []) \
                            .append(entity_name)

    return common_data_model


def get_common_data_model(path: str) -> dict[str, dict]:
    """
    Function that returns a flat dictionary with the entities definition

    **Parameters**:

    - **path**: parent directory of the entity files
    """

    result = {}

    for file_or_dir in os.listdir(path):

        file_or_dir_path = os.path.join(path, file_or_dir)
        # print(f"parsing {file_or_dir_path}")

        if os.path.isfile(file_or_dir_path):
            with open(file_or_dir_path, "rb") as common_data_model_file:
                file_or_dir_dot_split = file_or_dir.split('.')

                if file_or_dir_dot_split[-1] not in ['yml', "yaml"]:
                    continue

                common_data_model_value = yaml.safe_load(common_data_model_file)
                common_data_model_key = common_data_model_value["name"]
                result[common_data_model_key] = common_data_model_value

    return add_reverse_extensions_common_data_model(result)
