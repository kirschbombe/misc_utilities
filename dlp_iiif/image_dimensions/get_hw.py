import pandas as pd
from PIL import Image
from io import BytesIO
import requests
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

# Update DataFrame with image dimensions and add progress bar (tqdm)
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing images"):
    image_url_column = 'IIIF Access URL'  # Adjust based on your column name
    image_url = row[image_url_column]
    width, height = get_image_dimensions(image_url)
    df.at[index, 'media.width'] = width
    df.at[index, 'media.height'] = height

# Save the updated DataFrame to a new CSV
output_csv_file_path = 'dimensions_output.csv'
df.to_csv(output_csv_file_path, index=False)

print(f"Image dimensions added and saved to {output_csv_file_path}")
