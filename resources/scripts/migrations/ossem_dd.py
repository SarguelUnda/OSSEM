import os
from ruamel.yaml import YAML
from multiprocessing import Pool
from functools import partial
import sys

yaml=YAML(typ='rt')
yaml.width = float("inf")
yaml.default_flow_style = False
yaml.preserve_quotes = True
yaml.allow_unicode = True


DEFAULT_IGNORED_FILE_OR_DIR = ['ressources', ".git"]

def event_code_to_event_id(data_dictionary):
    if data_dictionary and "event_code" in data_dictionary:
        # This code is so that the order of key is the same after renaming
        data_dictionary_items = list(data_dictionary.items())
        (position, value) = next((i, x[1]) for (i,x) in enumerate(data_dictionary_items) if x[0]=="event_code")
        data_dictionary_items[position] = ("event_id", value)
        data_dictionary = dict(data_dictionary_items)
    return data_dictionary

def title_to_name(data_dictionary):
    if data_dictionary and "title" in data_dictionary:
        # This code is so that the order of key is the same after renaming
        data_dictionary_items = list(data_dictionary.items())
        (position, value) = next((i, x[1]) for (i,x) in enumerate(data_dictionary_items) if x[0]=="title")
        data_dictionary_items[position] = ("name", value)
        data_dictionary = dict(data_dictionary_items)
    return data_dictionary

def event_version_are_string(data_dictionary):
    if data_dictionary and "event_version" in data_dictionary:
        if not isinstance(data_dictionary["event_version"], str):
            print(f"WARNING! in {data_dictionary['name']}")
    return data_dictionary

POSSIBLE_MIGRATIONS = {
    'm1':event_code_to_event_id,
    'm2':title_to_name,
    'm3':event_version_are_string,
}

def crawl_data_dictionaries(path: str, ignored_file_or_dir=DEFAULT_IGNORED_FILE_OR_DIR):
    """
    Recursive function that visit all datadictionaries and apply migration on it before saving the dictionary back

    **Parameters**:

    - **path**: path of the directory that contains all of the data dictionaries ( usually: OSSEM-DD )
    - **ignored_directories**: directories to ignore when parsing the data dictionaries in `path`
    """

    to_process = []

    for file_or_dir in os.listdir(path):

        if file_or_dir in ignored_file_or_dir:
            continue

        file_or_dir_path = os.path.join(path, file_or_dir)

        # Directory - Recurse
        if os.path.isdir(file_or_dir_path):
            print(f"visiting {file_or_dir_path}", file=sys.stderr)
            to_process.extend(crawl_data_dictionaries(file_or_dir_path, ignored_file_or_dir))

        # File - Parse, and add to data_dictionary
        else:
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

    parser = argparse.ArgumentParser(description='Apply migration to ossem DD')
    parser.add_argument('migrations', metavar='migrations', type=str, nargs='+', help='an integer for the accumulator')

    args = parser.parse_args()
    to_process = crawl_data_dictionaries("OSSEM-DD")

    with Pool() as pool:
        pool.map(partial(apply_migrations, migrations=args.migrations), to_process)