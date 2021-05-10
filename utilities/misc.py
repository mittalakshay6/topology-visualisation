import os


def create_dir(path):
    """
    Create directory if not exists.
    """

    is_exists = os.path.isdir(path)
    if not is_exists:
        os.makedirs(path)
        print("created folder : ", path)