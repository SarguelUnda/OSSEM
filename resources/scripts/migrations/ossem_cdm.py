import os
from ruamel.yaml import YAML
from multiprocessing import Pool
from functools import partial
import sys
import re

yaml = YAML(typ='rt')
yaml.width = float("inf")
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.allow_unicode = True


DEFAULT_IGNORED_FILE_OR_DIR = ['ressources', ".git"]


def standard_name_from_camel_to_snake(cdm_entity):
    def to_snake_case(camel_str):
        # Insert a space before each uppercase letter, before doing the split
        # then join with an '_'
        return 'TBD' if camel_str == 'TBD' else '_'.join(re.sub(r"([A-Z])", r" \1", camel_str).lower().split())

    if cdm_entity and "attributes" in cdm_entity:
        for attribute in cdm_entity['attributes']:
            if "name" in attribute:
                attribute['name'] = to_snake_case(attribute['name'])
    return cdm_entity


def standard_name_from_snake_to_camel(cdm_entity):
    def to_camel_case(snake_str):
        return ''.join([c[0].upper() + c[1:]if len(c) > 0 else '' for c in snake_str.split('_')])

    if cdm_entity:
        if "name" in cdm_entity:
          cdm_entity['name'] = to_camel_case(cdm_entity['name'])
        if "prefix" in cdm_entity:
            cdm_entity["prefix"] = list(map(to_camel_case, cdm_entity["prefix"]))
        if "extends_entities" in cdm_entity:
            cdm_entity["extends_entities"] = list(map(to_camel_case, cdm_entity["extends_entities"]))
        if "attributes" in cdm_entity:
            for attribute in cdm_entity['attributes']:
                if "name" in attribute and attribute != "TBD":
                    attribute['name'] = to_camel_case(attribute['name'])
        return cdm_entity


POSSIBLE_MIGRATIONS = {
    'm4': standard_name_from_camel_to_snake,
    'm5': standard_name_from_snake_to_camel,
}

def crawl_cdm(path: str) -> dict[str, dict]:
    """
    Function that returns a flat dictionary with the entities definition

    **Parameters**:

    - **path**: parent directory of the entity files
    """

    to_process = []

    for file_or_dir in os.listdir(path):

        file_or_dir_path = os.path.join(path, file_or_dir)
        # print(f"parsing {file_or_dir_path}")

        if os.path.isfile(file_or_dir_path):
            with open(file_or_dir_path, "rb") as common_data_model_file:
                file_or_dir_dot_split = file_or_dir.split('.')

                # only check fo yaml file defining entities
                if file_or_dir_dot_split[-1] not in ['yml', "yaml"]:
                    continue

                to_process.append(file_or_dir_path)
                
    return to_process



def apply_migrations(file_or_dir_path, migrations):
    with open(file_or_dir_path, "r", encoding="utf-8") as data_dictionary_file:
        file_name_dot_split = file_or_dir_path.split('.')

        if file_name_dot_split[-1] not in ['yml', "yaml"]:
            return

        data_dictionary = yaml.load(data_dictionary_file)
        for f in migrations:
            data_dictionary = POSSIBLE_MIGRATIONS[f](data_dictionary)

    with open(file_or_dir_path, "w", encoding="utf-8", newline='\n') as data_dictionary_file:
        yaml.dump(data_dictionary, data_dictionary_file)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Apply migration to ossem CDM')
    parser.add_argument('migrations', metavar='migrations',
                        type=str, nargs='+', help='an integer for the accumulator')

    args = parser.parse_args()
    to_process = crawl_cdm("OSSEM-CDM\\schemas\\entities")
    print(to_process)

    with Pool() as pool:
        pool.map(partial(apply_migrations, migrations=args.migrations), to_process)
