import json
from pathlib import Path
from typing import Dict, List, Callable
import logging
import concurrent.futures
from tqdm import tqdm

from . import api_handler as ah
from utils.helpers import create_file_folder


def get_dict_list(filepath: str) -> List[Dict]:
    """Handle json files.

    Params
    ------
    filepath (str): file path

    Return
    ------
    List[dict]
    """
    with Path(filepath).open(mode="r", encoding="utf-8") as fp:
        return json.load(fp)


def get_translated_dict(d: Dict) -> Dict:
    """Translate a singular dict with google cloud translation

    Args:
        d (Dict): original dict containing the source language

    Returns:
        Dict: translated dict with the target language
    """

    bool_map = [isinstance(v, str) for v in d.values()]
    original_value_list = [v for v in d.values()]
    string_value_list = [v for v in d.values() if isinstance(v, str)]

    # call Google cloud translation API

    result = ah.translate_text_with_model("en", string_value_list)
    result = [v["translatedText"] for v in result]

    # create a new list with the translation based on the bool map

    new_list = []
    for i in range(0, len(original_value_list)):
        if bool_map[i] is True:
            new_list.append(result[i])
        else:
            new_list.append(original_value_list[i])

    return dict(zip(d.keys(), new_list))


def tqdm_multithreading(f: Callable, dict_list: List) -> List:
    """Use multithreding and tqdm to call `f`.

    Args:
        f (Callable): main translator function
        dict_list (List): list of dicts to be translated

    Returns:
        List: list of translated dicts
    """

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(f, dict_list), total=len(dict_list)))

    return results


def get_translated_dict_list(dict_list: List[Dict]) -> tuple[List[Dict], Dict]:
    """Handle translation.

    This function iterates each dict in the list, creates a list sequence of
    the dict's values and call Google Translation API which responds with
    a list sequence of translated texts. Each item in the list of translation
    is then compared agains the bool_map in order to create a dict with
    translated text and also with other non-strings that were not sent to
    Google for translation.

    Params
    ------
    dict_list (list): list of json dictionaries

    Return
    ------
    List[dict]
    {
        api_calls: int,
        api_chars: int
    }
    """

    new_dict_list = tqdm_multithreading(get_translated_dict, dict_list)
    new_dict_list = sorted(new_dict_list, key=lambda x: x['sequence']) # this won't work if the json doesn't have 'sequence'

    meta = {
        "api_calls": len(dict_list),
        "api_chars": len(
            "".join([v for d in dict_list for k, v in d.items() if isinstance(v, str)])
        ),
    }

    return new_dict_list, meta


def save_to_new_file(
    filepath: Path, ff: str, dict_list: List[Dict], output_path: str
) -> None:
    """Save the new file.

    If the output folder doesn't exist, a new output folder will be created
    and the file is saved in that folder with the same original name.

    Params
    ------
    dict_list (list): list of translated json dictionaries

    Return
    ------
    None
    """

    output_path = create_file_folder(filepath, ff, output_path)

    with output_path.open(mode="w", encoding="utf-8") as nfp:
        nfp.write(json.dumps(dict_list, indent=2))


def translate(ff, filepath, output_path):

    logger = logging.getLogger(__name__)
    logger.info(f"Starting: {ff.name}")

    dl = get_dict_list(ff)
    tdl, meta = get_translated_dict_list(dl)
    save_to_new_file(filepath, ff, tdl, output_path)

    return meta


if __name__ == "__main__":
    pass
