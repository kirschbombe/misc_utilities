import os
import csv
import requests
import io
from PIL import Image, UnidentifiedImageError
import colorgram

# Function to extract prominent colors from an image
def extract_colors(image_path, num_colors=5):
    colors = colorgram.extract(image_path, num_colors)
    return [tuple(color.rgb) for color in colors]

# Input CSV file containing IIIF image URLs
input_csv = "input_iiif_urls.csv"

# Output CSV file path
output_csv = "output_colors.csv"

# List to store IIIF URLs and corresponding colors
iiif_data = []

# Read IIIF image URLs from the input CSV file
with open(input_csv, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        iiif_url = row[0]
        iiif_data.append((iiif_url, []))

# Iterate through each IIIF image URL and extract colors
for iiif_url, _ in iiif_data:
    try:
        response = requests.get(iiif_url)
        response.raise_for_status()
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes))
        image_path = "temp_image.jpg"
        image.save(image_path)
        colors = extract_colors(image_path)
        os.remove(image_path)
        for index, data in enumerate(iiif_data):
            if data[0] == iiif_url:
                iiif_data[index] = (iiif_url, colors)  # Replace tuple with new data
                break
    except (UnidentifiedImageError, requests.RequestException) as e:
        print(f"Error processing '{iiif_url}': {str(e)}")

# Write the data to a new CSV file
with open(output_csv, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["IIIF URL", "Colors"])
    for iiif_url, colors in iiif_data:
        csv_writer.writerow([iiif_url, colors])

print("Color data written to", output_csv)

