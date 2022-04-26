from setenv import setenv
from decouple import config
from pathlib import Path

from api_handler import translate_document

if __name__ == "__main__":
    setenv()
    filepath = r"C:\Users\admin\Documents\repos\riiid_auto_translator\translators\sample.xlsx"
    response = translate_document(config("PROJECT_ID"), filepath)

    output_folder = "output"

    newfilepath = Path(filepath)
    new_output_path = newfilepath.parent.joinpath(output_folder)
    new_output_path.mkdir(exist_ok=True)

    newfilepath = new_output_path / newfilepath.name
    newfilepath.touch()

    with newfilepath.open(mode="wb") as nfp:
        nfp.write(response)
