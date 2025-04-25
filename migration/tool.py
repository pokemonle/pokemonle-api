import os
import csv
from contextlib import contextmanager

@contextmanager
def load_csv(db_name: str):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", f"{db_name}.csv")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file {file_path} does not exist.")
    with open(file_path, "r") as f:
        yield csv.DictReader(f)