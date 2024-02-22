import pandas as pd
from PIL import Image
from io import BytesIO
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# Function to get image dimensions from URL
def get_image_dimensions(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        return width, height
    except Exception as e:
        print(f"Error getting dimensions for {url}: {e}")
        return None, None

# Get input CSV file path from user
csv_file_path = input("Enter the path to the input CSV file: ")

# Read CSV file
df = pd.read_csv(csv_file_path)

# Create new columns for height and width
df['media.height'] = None
df['media.width'] = None

# Function to update DataFrame with image dimensions
def update_dimensions(index, row):
    image_url_column = 'IIIF Access URL'
    image_url = row[image_url_column]
    width, height = get_image_dimensions(image_url)
    df.at[index, 'media.width'] = width
    df.at[index, 'media.height'] = height

# Update DataFrame with image dimensions in parallel using concurrent.futures module
with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers based on your system
    futures = [executor.submit(update_dimensions, index, row) for index, row in df.iterrows()]
    for future in tqdm(futures, total=len(futures), desc="Processing images"):
        future.result()

# Save the updated DataFrame to a new CSV file
output_csv_file_path = 'dimensions_output.csv'
df.to_csv(output_csv_file_path, index=False)

print(f"Image dimensions added and saved to {output_csv_file_path}")
