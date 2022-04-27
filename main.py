from utils.setenv import setenv
from utils.validators import Validator
from translators import json_files, xlsx


def main(filepath, output_path):
 
    found_files = Validator(filepath).found_files

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
    output_path = "./output"
    filepath = r"C:\Users\admin\Downloads\mock_data"
    main(filepath, output_path)