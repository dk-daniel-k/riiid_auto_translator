from pathlib import Path

def create_file_folder(filepath, ff, output_path):
    output_path = filepath / Path(output_path) / ff.relative_to(filepath)
    output_path.parent.mkdir(parents=True,exist_ok=True)
    output_path.touch()

    return output_path