from utils.setenv import setenv
from utils.validators import Validator
from translators import json_files, xlsx
from utils.logger import logger
from collections import Counter
from utils.argparser import parser


args = parser.parse_args()


def main(filepath: str, output_path: str) -> None:
 
    # find and make a list of files
    found_files = Validator(filepath, output_path).found_files

    # set the environment for Google Cloud Translation key path
    setenv()

    extension_map = {
        '.json': json_files.translate,
        '.xlsx': xlsx.translate,
        '.xls': xlsx.translate
    }

    final_count = Counter({})
    # begin main function
    for ff in found_files:
        translator = extension_map.get(ff.suffix)
        meta = translator(ff, filepath, output_path)
        final_count += Counter(meta)
    
    logger.info(f"API calls made: {final_count['api_calls']}")
    logger.info(f"Number of chars sent: {final_count['api_chars']}")

if __name__ == "__main__":
    output_path = args.output_path
    filepath = args.file_path
    main(filepath, output_path)
