import os
from datetime import datetime
import numpy as np
from tqdm import tqdm

def load_data(dataset: str, datasource: str) -> list[tuple[np.ndarray, datetime]]:
    """
        Load data based on the specified datasource. Return a list of tuples containing the dbz map and its corresponding time frame.
    """
    if datasource == "numpy_grid":
        return load_numpy_grid_data(dataset)
    elif datasource == "windy":
        return load_windy_dataset(dataset)
    else:
        raise ValueError(f"Invalid datasource: {datasource}. Must be 'numpy_grid' or 'windy'.")

def load_numpy_grid_data(dataset: str) -> list[tuple[np.ndarray, datetime]]:
    """
        Load numpy grid data and extract time frames from file names. Return a list of tuples containing the dbz map and its corresponding time frame.
    """
    from src.preprocessing import read_numpy_grid
    DATASET_PATH = "data/numpy_grid/"

    source_path = os.path.join(DATASET_PATH, dataset)
    img_paths = [os.path.join(source_path, img_name) for img_name in sorted(os.listdir(source_path)) if img_name.endswith('.npy')]
    dbz_maps: list[tuple[np.ndarray, datetime]] = []

    for path in tqdm(img_paths, desc="Processing images and detecting storms"):
        file_name = path.split("/")[-1].split(".")[0]

        time_frame = datetime.strptime(file_name[4:19], "%Y%m%d_%H%M%S")
        img = read_numpy_grid(path)
        dbz_maps.append((img, time_frame))
    
    return dbz_maps

def load_windy_dataset(dataset: str) -> list[tuple[np.ndarray, datetime]]:
    from src.preprocessing import windy_preprocessing_pipeline
    import cv2
    DATASET_PATH = "data/windy/"

    source_path = os.path.join(DATASET_PATH, dataset)
    print(f"Loading dataset from {source_path}...")
    img_paths = [os.path.join(source_path, img_name) for img_name in sorted(os.listdir(source_path)) if img_name.endswith('.png')]
    print(f"Found {len(img_paths)} images in the dataset.")
    dbz_maps: list[tuple[np.ndarray, datetime]] = []

    for path in tqdm(img_paths, desc="Processing images and detecting storms"):
        file_name = path.split("/")[-1].split(".")[0]

        time_frame = datetime.strptime(file_name, "%Y%m%d-%H%M%S")
        img = cv2.imread(path)
        img = windy_preprocessing_pipeline(img)
        dbz_maps.append((img, time_frame))

    return dbz_maps