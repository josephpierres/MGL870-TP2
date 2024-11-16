import os
import requests
import zipfile
from tqdm import tqdm

# Create the "input" folder if it doesn't exist
os.makedirs("input", exist_ok=True)

# Create results folders if they don't exist
os.makedirs("HDFS_results", exist_ok=True)
os.makedirs("BGL_results", exist_ok=True)

# List of files to download with their URLs and extraction folders
files_to_download = [
    {"url": "https://zenodo.org/records/8196385/files/HDFS_v1.zip?download=1", "name": "HDFS_v1.zip", "extract_to": "input/HDFS_v1"},
    {"url": "https://zenodo.org/records/8196385/files/BGL.zip?download=1", "name": "BGL.zip", "extract_to": "input/BGL"}
]

for file_info in files_to_download:
    # Define the output path for the current file
    output_path = os.path.join("input", file_info["name"])
    extract_to = file_info["extract_to"]

    # Create the extraction folder if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)

    # Stream the file and display a progress bar
    response = requests.get(file_info["url"], stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(output_path, "wb") as file, tqdm(
            desc=f"Downloading {file_info['name']}",
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        print(f"File downloaded to {output_path}")

        # Unzip the downloaded file to the specific folder
        with zipfile.ZipFile(output_path, "r") as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"File unzipped to '{extract_to}'")

    else:
        print(f"Failed to download {file_info['name']}. HTTP status code: {response.status_code}")
