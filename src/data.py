import hashlib
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

DATA_URL = ("https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
            "?query=select+*+from+cumulative&format=csv")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
RAW_PATH = DATA_DIR / "koi_cumulative.csv"
SPLIT_PATH = DATA_DIR / "split.csv"

EXPECTED_SHAPE = (9564, 153)
EXPECTED_SHA256 = None


#fingerprint of the file that changes if any byte changes
def file_sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


#download the csv with retries since the archive sometimes returns temporary errors
def download(attempts=3):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = RAW_PATH.with_suffix(".part")
    for attempt in range(1, attempts + 1):
        try:
            urllib.request.urlretrieve(DATA_URL, tmp)
            tmp.replace(RAW_PATH)
            print(f"Downloaded to {RAW_PATH}\nSHA-256: {file_sha256(RAW_PATH)}")
            return
        except urllib.error.URLError as err:
            tmp.unlink(missing_ok=True)
            if attempt == attempts:
                raise RuntimeError(f"Download failed ({err}). Try again later or save {DATA_URL} "
                                   f"as {RAW_PATH} in a browser") from err
            time.sleep(10 * attempt)


#load the raw table and check it is the audited version with a fixed row order
def load_data():
    if not RAW_PATH.exists():
        download()
    df = pd.read_csv(RAW_PATH, low_memory=False)
    if df.shape != EXPECTED_SHAPE:
        raise ValueError(f"Expected shape {EXPECTED_SHAPE} but got {df.shape}")
    if EXPECTED_SHA256 and file_sha256(RAW_PATH) != EXPECTED_SHA256:
        raise ValueError("File differs from the audited version")
    return df.sort_values("kepoi_name").reset_index(drop=True)


#labelled rows with the target y and the train test split from notebook 01
def load_labelled():
    if not SPLIT_PATH.exists():
        raise FileNotFoundError("data/split.csv not found so run notebooks/01_audit.ipynb first")
    split = pd.read_csv(SPLIT_PATH)
    labelled = load_data().merge(split, on="kepoi_name", validate="one_to_one").copy()
    labelled["y"] = (labelled["koi_disposition"] == "CONFIRMED").astype(int)
    return labelled
