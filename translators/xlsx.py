from os import PathLike
from pathlib import Path

import pandas as pd
from decouple import config

from api_handler import translate_document


def convert_to_xlsx(filepath) -> PathLike:
    """Convert xls file to xlsx and return the new path im TMP"""
    filepath = filepath.as_posix()
    df = pd.read_excel(filepath)
    filepath = Path("/tmp") / Path(filepath + "x").name
    df.to_excel(filepath.as_posix())
    return filepath


def translate(filepath):
    if filepath.suffix == ".xls":
        filepath = convert_to_xlsx(filepath)

    response = translate_document(config("PROJECT_ID"), filepath)

    output_folder = "output"

    newfilepath = Path(filepath)
    new_output_path = newfilepath.parent.joinpath(output_folder)
    new_output_path.mkdir(exist_ok=True)

    newfilepath = new_output_path / newfilepath.name
    newfilepath.touch()

    with newfilepath.open(mode="wb") as nfp:
        nfp.write(response)


if __name__ == "__main__":
    pass





        

        

