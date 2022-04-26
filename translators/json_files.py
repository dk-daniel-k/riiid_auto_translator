import json
import os
from pathlib import Path
from typing import Dict, List

from decouple import config

import api_handler as ah


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

    This function iterates each dict in the list and call Google Translation
    API which responds with translated text. Each value is then replaced with
    the translated text.

    Params
    ------
    dict_list (list): list of json dictionaries

    Return
    ------
    List[dict]
    """
    new_dict_list = []

    for d in dict_list:
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


def save_to_new_file(newfilepath: str, dict_list: List[Dict]) -> None:
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

    # creation of new folder and files is a common function and should be
    # separated into another file.
    output_folder = "output"

    newfilepath = Path(newfilepath)
    new_output_path = newfilepath.parent.joinpath(output_folder)
    new_output_path.mkdir(exist_ok=True)

    newfilepath = new_output_path / newfilepath.name
    newfilepath.touch()

    with newfilepath.open(mode="w", encoding="utf-8") as nfp:
        nfp.write(json.dumps(dict_list, indent=2))


def main(filepath):

    if not isinstance(filepath, str):
        raise TypeError("newfilepath has to be str type.")

    supported_filetypes = [".json", ".xlsx"]

    # find files and make a list
    if Path(filepath).is_dir():
        found_files = list(Path(filepath).rglob("*"))
    if Path(filepath).is_file():
        found_files = [Path(filepath)]

    # check the list and raise error if supported types not found
    if Path(filepath).is_dir() and all(
        [f.suffix not in supported_filetypes for f in found_files]
    ):
        raise FileNotFoundError(
            f"Could not find a supported file. Currently supporting: {', '.join(supported_filetypes)}"
        )

    # begin main function
    dl = get_dict_list(filepath)
    tdl = get_translated_dict_list(dl)
    save_to_new_file(filepath, tdl)


if __name__ == "__main__":

    key_path = config("GOOGLE_KEY_PATH")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path
    filepath = r"C:\Users\admin\Documents\repos\riiid_auto_translator\translators\1학년_YBM(박).hwp.json"

    main(filepath)
