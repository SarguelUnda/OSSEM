import json
import os
from functools import partial

from .dd import get_data_dictionaries
from .cdm import get_common_data_model
from .dm import get_detection_model

def load_ossem(ossem_parsing_function,
                ossem_name=None,
                from_cache=True,
                cache_path="./build/",
                ossem_path=None):
    """
    Loads an ossem project definition from a directory or json file

    Loads either by:
    - loading a json object when `from_cache=True`
    - parsing yaml files in a directory containing the data dicitonaries

    **Parameters**:

    - ossem_parsing_function: parsing function to use when getting yml file one of (get_flat_data_dictionaries, get_common_data_model, get_detection_model)
    - from_cache: whether to load ossem variable state from `file_path` ie not watching any change in ossem directories
    - cache_path: path to the json directory that contains the cached ossem json file
    - ossem_path: directory from which to recursively parse yaml files if None default to ossem_name
    """

    if not ossem_name:
        raise ValueError("Need ossem Name to be a string")

    file_path = os.path.join(cache_path, ossem_name + ".json")

    ossem_definition = None

    if from_cache:
        if os.path.isfile(file_path):
            ossem_definition = json.load(open(file_path, "rb"))
    else:
        ossem_path = ossem_path or ossem_name
        ossem_definition = ossem_parsing_function(ossem_path)

    return ossem_definition

#
# Convinience
#
load_ossem_dd = partial(load_ossem, get_data_dictionaries, ossem_name="OSSEM-DD")
load_ossem_cdm = partial(load_ossem, get_common_data_model, ossem_name="OSSEM-CDM", ossem_path="OSSEM-CDM/schemas/entities")
load_ossem_dm = partial(load_ossem, get_detection_model, ossem_name="OSSEM-DM", ossem_path="OSSEM-DM/relationships")