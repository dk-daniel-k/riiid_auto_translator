from decouple import config
import os


def setenv():
    """Add the google cloud translation key path to the environment
    """
    key_path = config("GOOGLE_KEY_PATH")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path