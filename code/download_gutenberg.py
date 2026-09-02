"""Converts the gutenberg csv into the right download links and downloads the respective books"""

import os
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


def download_book(row):
    path = Path(f"text/raw/{row.title}.txt")
    if not path.exists():
        urlretrieve(row.url, path)
    else:
        urlretrieve(row.url, f"text/raw/{row.title}2.txt")


if __name__ == "__main__":
    df = pd.read_csv("books_gutenberg.csv")

    df["url"] = [f"https://gutenberg.org/cache/epub/{x}/pg{x}.txt" for x in df["id_number"]] # save right urls for download
    # make path for the prepared data
    os.makedirs("text/raw/", exist_ok=True)

    print("Downloading the Top 100 engish books from gutenberg.org")

    for row in df.itertuples():
        download_book(row)

    print("Downloads from gutenberg.org finished")
