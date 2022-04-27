from utils.setenv import setenv
from utils.validators import Validator
from translators import json_files, xlsx
from pathlib import Path

def main(filepath, output_path):
 
    # find and make a list of files
    found_files = Validator(filepath, output_path).found_files

    # set the environment for Google Cloud Translation key path
    setenv()

    extension_map = {
        '.json': json_files.translate,
        '.xlsx': xlsx.translate,
        '.xls': xlsx.translate
    }

    # begin main function
    for ff in found_files:
        translator = extension_map.get(ff.suffix)
        translator(ff, filepath, output_path)

if __name__ == "__main__":
    output_path = r"C:\Users\admin\Downloads\output"
    filepath = r"C:\Users\admin\Downloads\mock_data"
    main(filepath, output_path)