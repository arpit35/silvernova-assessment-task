import os
import pickle
from typing import Any


def load_pkl_file(folder: str, filename: str) -> Any:
    file_path = os.path.join(folder, f"{filename}.pkl")

    with open(file_path, "rb") as f:
        return pickle.load(f)


def dump_pkl_file(folder: str, filename: str, data: Any) -> None:
    file_path = os.path.join(folder, f"{filename}.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(data, f)
