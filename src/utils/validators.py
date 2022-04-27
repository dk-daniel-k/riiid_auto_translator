from os import PathLike
from pathlib import Path
from typing import List


class Validator:

    supported_filetypes = [".json", ".xlsx", ".xls"]

    def __init__(self, filepath):
        self.filepath = filepath
        self.found_files = self.find_files()

    def find_files(self) -> List[PathLike]:
        """Find files and return a list.

        Returns:
            _list_: _list of pathlike objects found in the given filepath_
        """
        if Path(self.filepath).is_dir():
            return [
                f for f in Path(self.filepath).rglob("*") 
                if f.suffix in Validator.supported_filetypes
                ]
        if Path(self.filepath).is_file():
            return [Path(self.filepath)]

    @property
    def filepath_type_correct(self) -> TypeError:
        """Raise error if the filepath is other than str type.

        Raises:
            TypeError: _filepath has to be str_
        """
        if not isinstance(self.filepath, str):
            raise TypeError("THe path has to be a string.")

    @property
    def no_supported_file(self) -> FileNotFoundError:
        if Path(self.filepath).is_dir() and all(
            [f.suffix not in Validator.supported_filetypes for f in self.found_files]
        ):
            raise FileNotFoundError(
                f"Could not find a supported file. Currently supporting: {', '.join(Validator.supported_filetypes)}"
            )
