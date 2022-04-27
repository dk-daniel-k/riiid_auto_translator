import json
from pathlib import Path
from typing import Dict, List

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


def get_translated_dict_list(dict_list: List[Dict]) -> List[Dict]:
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
    """
    new_dict_list = []

    for d in dict_list:
        print(f"{dict_list.index(d)}", end="\r")
        bool_map = [isinstance(v, str) for v in d.values()]
        original_value_list = [v for v in d.values()]
        string_value_list = [v for v in d.values() if isinstance(v, str)]

        # google cloud translation API call made here
        result = ah.translate_text_with_model("en", string_value_list)
        result = [v["translatedText"] for v in result]

        new_list = []
        for i in range(0, len(original_value_list)):
            if bool_map[i] is True:
                new_list.append(result[i])
            else:
                new_list.append(original_value_list[i])

        new_dict = dict(zip(d.keys(), new_list))
        new_dict_list.append(new_dict)

    return new_dict_list


def save_to_new_file(filepath: Path, ff: str, dict_list: List[Dict], output_path: str) -> None:
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
    print("starting: " + ff.name)
    dl = get_dict_list(ff)
    tdl = get_translated_dict_list(dl)
    save_to_new_file(filepath, ff, tdl, output_path)


if __name__ == "__main__":
    pass