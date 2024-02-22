import io
import csv
import requests
import pandas as pd
from PIL import Image
from webcolors import hex_to_name
import tempfile  # Import the tempfile module
import urllib.parse

# Define the color categories
color_categories = {
    'red': ['red'],
    'pink': ['pink'],
    'orange': ['orange'],
    'yellow': ['yellow'],
    'green': ['green', 'lime', 'olive'],
    'blue': ['blue', 'cyan', 'teal'],
    'brown': ['brown', 'maroon'],
    'purple': ['purple', 'magenta'],
    'white': ['white'],
    'gray': ['gray', 'silver'],
}

def get_prominent_color(image_url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        
        # Encode the URL to handle special characters
        encoded_url = urllib.parse.quote(image_url, safe='/:')
        
        response = requests.get(encoded_url, headers=headers)
        response.raise_for_status()

        # Save the image content to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response.content)

        # Open the temporary file using Pillow
        image = Image.open(tmp_file.name)
        image.thumbnail((100, 100))  # Resize the image for faster processing

        # Convert the image to RGB if it's not
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get the colors from the image
        colors = image.getcolors(image.width * image.height)
        if colors:
            prominent_color = max(colors, key=lambda item: item[0])[1]
            return prominent_color
        else:
            return None
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        return None

# map the color HEX values to color names
def get_color_name(color_hex):
    color_name = hex_to_name(color_hex, spec='css3')
    for category, color_list in color_categories.items():
        if color_name in color_list:
            return category
    return None

# Load IIIF URLs from the CSV
df = pd.read_csv('iiif_images.csv')

# Process each IIIF image and write color names to CSV
with open('output.csv', 'w', newline='') as output_csv:
    csv_writer = csv.writer(output_csv)
    csv_writer.writerow(['IIIF_URL', 'Color_Name'])

    for url in df['IIIF_URL']:
        try:
            color_hex = get_prominent_color(url)
            if color_hex:
                color_name = get_color_name(color_hex)
                csv_writer.writerow([url, color_name])
            else:
                csv_writer.writerow([url, 'unknown'])
        except Exception as e:
            print(f"Error processing {url}: {e}")
