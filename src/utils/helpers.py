from pathlib import Path


class PathHandler:

    def __init__(self, filepath, ff, output_path):
        self.filepath = filepath
        self.ff = ff
        self.output_path = output_path

    def get_output_path(self):
        return self.filepath / Path(self.output_path) / self.ff.relative_to(self.filepath)

    def create_file_folder(self):
        output_path = self.get_output_path()
        output_path.parent.mkdir(parents=True,exist_ok=True)
        output_path.touch()

        return output_path
