import logging
from os import PathLike
from pathlib import Path

import pandas as pd
from decouple import config
from utils.helpers import create_file_folder

from .api_handler import translate_document


def convert_to_xlsx(filepath) -> PathLike:
    """Convert xls file to xlsx and return the new path im TMP"""
    filepath = filepath.as_posix()
    df = pd.read_excel(filepath)
    filepath = Path("/tmp") / Path(filepath + "x").name
    df.to_excel(filepath.as_posix())
    return filepath


def translate(ff, filepath, output_path):
    logger = logging.getLogger(__name__)
    logger.info("starting: " + ff.name)
    if ff.suffix == ".xls":
        excel_ff = convert_to_xlsx(ff)
    else:
        excel_ff = ff

    response = translate_document(config("PROJECT_ID"), excel_ff)

    output_path = create_file_folder(filepath, ff, output_path)

    with output_path.open(mode="wb") as nfp:
        nfp.write(response)


if __name__ == "__main__":
    pass





        

        

