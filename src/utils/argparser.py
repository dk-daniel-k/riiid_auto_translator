import argparse

parser = argparse.ArgumentParser(description="Json, Xlsx translator")

parser.add_argument("file_path", type=str, help="Location of your files that require translation")
parser.add_argument("output_path", type=str, help="Your desired output path")
