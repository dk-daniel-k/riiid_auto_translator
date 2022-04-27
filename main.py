from utils.setenv import setenv
from utils.validators import Validator
import translators


def main(filepath):
 
    filepath = r"C:\Users\admin\Downloads\parsed_rev\문법"
    found_files = Validator(filepath).found_files

    setenv()

    extension_map = {
        '.json': translators.json_files.translate,
        '.xlsx': translators.xlsx.translate,
        '.xls': translators.xls.translate
    }

    # begin main function
    for ff in found_files:
        translator = extension_map.get(ff.suffix)
        translator()
        
