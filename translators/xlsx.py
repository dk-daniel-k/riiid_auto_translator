from setenv import setenv
from decouple import config
from pathlib import Path
import pandas as pd

from api_handler import translate_document

if __name__ == "__main__":
    setenv()
    filepaths = Path(r"C:\Users\admin\Downloads\parsed_rev\문법").glob('*')

    for filepath in filepaths:
        if filepath.is_dir():
            continue

        filepath = filepath.as_posix()
        df = pd.read_excel(filepath)

        filepath += 'x'
        df.to_excel(filepath)


        response = translate_document(config("PROJECT_ID"), filepath)

        output_folder = "output"

        newfilepath = Path(filepath)
        new_output_path = newfilepath.parent.joinpath(output_folder)
        new_output_path.mkdir(exist_ok=True)

        newfilepath = new_output_path / newfilepath.name
        newfilepath.touch()

        with newfilepath.open(mode="wb") as nfp:
            nfp.write(response)
