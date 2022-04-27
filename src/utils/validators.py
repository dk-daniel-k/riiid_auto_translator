from os import PathLike
from pathlib import Path
from typing import List


class Validator:

    supported_filetypes = [".json", ".xlsx", ".xls"]

    def __init__(self, filepath, output_path):
        self.filepath = filepath
        self.output_path = output_path
        self.output_path_files = self.get_output_path_files()
        self.found_files = self.find_files()
        self.is_valid = self._is_valid()
        
    @property
    def filepath_type_correct(self) -> TypeError:
        """Raise error if the filepath is other than str type.

        Raises:
            TypeError: _filepath has to be str_
        """
        if not all([
            isinstance(self.filepath, str),
            isinstance(self.output_path, str)
        ]):
            raise TypeError("The path has to be a string.")

    @property
    def no_supported_file(self) -> FileNotFoundError:
        if Path(self.filepath).is_dir() and all(
            [f.suffix not in Validator.supported_filetypes for f in self.found_files]
        ):
            raise FileNotFoundError(
                f"Could not find a supported file. Currently supporting: {', '.join(Validator.supported_filetypes)}"
            )

    def _is_valid(self):
        return all([
            self.filepath_type_correct,
            self.no_supported_file
            ])

    def find_files(self) -> List[PathLike]:
        """Find files and return a list.

        Files that already exist in the output folder are skipped.

        Returns:
            _list_: _list of pathlike objects found in the given filepath_
        """
        if Path(self.filepath).is_dir():
            return [
                f for f in Path(self.filepath).rglob("*") 
                if f.suffix in Validator.supported_filetypes
                if f.relative_to(self.filepath) not in self.output_path_files
                ]
        if Path(self.filepath).is_file():
            if Path(self.filepath).relative_to(self.file_path) not in self.output_files:
                return [Path(self.filepath)]
            else:
                return []

    def get_output_path_files(self):
        found_op_files = Path(self.output_path).rglob("*")
        return [f.relative_to(self.output_path) for f in found_op_files]

