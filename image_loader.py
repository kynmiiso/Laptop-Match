"""Loads images from the csv file"""
from typing import Any
import pandas as pd


def load_image_links(csv_file: str):
    """Loads laptop image links from the CSV into a dictionary mapping IDs to URLs.

    Args:
        csv_file: Path to the laptops CSV file

    Returns:
        Dictionary mapping laptop index (ID) to image URL
    """
    """Loads images from the csv file"""
    from typing import Dict
    import pandas as pd

    df = pd.read_csv(csv_file)
    img_links = {}

    for _, row in df.reset_index().iterrows():
        img_links[int(row['index'])] = row['img_link']

    return img_links
