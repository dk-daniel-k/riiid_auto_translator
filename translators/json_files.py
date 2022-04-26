import json
from pathlib import Path
from typing import Dict, List

from setenv import setenv
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


    # key_generator = (v for d in dict_list for v in list(d.keys()))
    # bool_map = (isinstance(v, str) for d in dict_list for v in list(d.values()))
    # original_value_list = (v for d in dict_list for v in list(d.values()))
    # string_value_list = [v for d in dict_list for v in list(d.values()) if isinstance(v, str)]

    # result_list = []
    # a = 10
    # for i in range(0, len(string_value_list), a):
    #     result = ah.translate_text(string_value_list[:i+a])
    #     result_list.extend([d['translatedText'] for d in result])
    
    

    


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

    supported_filetypes = [".json"]

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
    for ff in found_files:
        print("starting: " + ff.name)
        dl = get_dict_list(ff)
        tdl = get_translated_dict_list(dl)
        save_to_new_file(ff, tdl)
        


if __name__ == "__main__":

    
    filepath = r"C:\Users\admin\Downloads\parsed_rev\내신_2학년"
    setenv()
    main(filepath)

    # to do:

    # add capability for xls (just a matter of switching MIME type)

    # clean up the current code

    # separate a main.py and create a class that handles function usage
    # based on file extensions

    # try converting txts into docxs, translate, and turn them back into txt (for speed)
    
    # if I pick a folder with multiple folders inside, the structure should be replicated inside /output
    # so I don't have to do this manually

    # multiprocessing / progress bar

    # test (make sure input json # and output json # are the same)
    # write unit test but also write in-functionv validation

    # if there are files of same name, those files should be taken out of the queue