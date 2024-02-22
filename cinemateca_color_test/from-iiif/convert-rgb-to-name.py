import csv
import ast
import webcolors

# Read CSV file containing RGB tuples and IIIF URLs
input_csv = "input_colors.csv"

# Output CSV file path
output_csv = "output_color_names.csv"

# List to store RGB tuples and corresponding color names
color_data = []

# Read RGB tuples from the input CSV file
with open(input_csv, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip header
    for row in csv_reader:
        if len(row) >= 1:
            rgb_str = row[0]
            try:
                rgb_tuple = ast.literal_eval(rgb_str)
                if isinstance(rgb_tuple, tuple) and len(rgb_tuple) == 3:
                    color_data.append((rgb_tuple, ""))
                else:
                    print(f"Invalid RGB tuple format in row: {rgb_str}")
            except (ValueError, SyntaxError):
                print(f"Invalid RGB format in row: {rgb_str}")

# Convert RGB tuples to color names
for index, (rgb_tuple, _) in enumerate(color_data):
    try:
        color_name = webcolors.rgb_to_name(rgb_tuple)
        color_data[index] = (rgb_tuple, color_name)
    except ValueError:
        color_data[index] = (rgb_tuple, "Unknown")

# Write the data to a new CSV file
with open(output_csv, "w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["RGB Tuple", "Color Name"])
    for rgb_tuple, color_name in color_data:
        csv_writer.writerow([rgb_tuple, color_name])

print("Color names data written to", output_csv)
