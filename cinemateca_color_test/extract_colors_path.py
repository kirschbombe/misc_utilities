import csv
from PIL import Image
import webcolors
import colorsys

# Function to get the closest CSS color name given an RGB tuple
def get_closest_css_color_name(rgb_color):
    min_distance = float('inf')
    css_color_name = None

    for css_name, css_hex in webcolors.HTML4_NAMES_TO_HEX.items():
        css_rgb = webcolors.hex_to_rgb(css_hex)
        distance = color_distance(rgb_color, css_rgb)
        if distance < min_distance:
            min_distance = distance
            css_color_name = css_name

    return css_color_name

# Function to calculate the color distance between two RGB tuples
def color_distance(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    return (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2

# Function to get the prominent color from an image
def get_prominent_color(image_path):
    image = Image.open(image_path)
    image.thumbnail((100, 100))  # Resize the image for faster processing

    pixels = list(image.getdata())
    rgb_values = [color[:3] for color in pixels]

    # Calculate the average color
    avg_color = tuple(map(lambda x: int(sum(x) / len(x)), zip(*rgb_values)))

    return avg_color

# Read image paths from the CSV file
input_csv_file = 'input_images.csv'
output_csv_file = 'output_colors.csv'

with open(input_csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    rows = list(reader)

# Process images and write results to the output CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Image Path', 'Prominent Color', 'CSS Color Name'])

    for row in rows:
        image_path = row[0]
        try:
            prominent_color = get_prominent_color(image_path)
            css_color_name = get_closest_css_color_name(prominent_color)

            writer.writerow([image_path, prominent_color, css_color_name])
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
