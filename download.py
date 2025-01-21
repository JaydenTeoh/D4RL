import urllib.request
import os
import sys


def download_dataset_from_url(dataset_url, output_name=None):
    if output_name is None:
        _, dataset_name = os.path.split(dataset_url)
        output_name = dataset_name

    if not os.path.exists('datasets'):
        os.makedirs('datasets')
    
    filepath = f'datasets/{output_name}'
    
    urllib.request.urlretrieve(dataset_url, filepath)
    
    if not os.path.exists(filepath):
        raise IOError("Failed to download dataset from %s" % dataset_url)
    
    return filepath


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python download_dataset.py <dataset_url> [output_name]")
        sys.exit(1)

    dataset_url = sys.argv[1]

    # Get the output name (optional)
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        filepath = download_dataset_from_url(dataset_url, output_name)
        print(f"Dataset downloaded successfully as '{filepath}'")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)