# 1. Takes the user input for the directory path.
# 2. Checks if the directory exists. If not, it displays an error message.
# 3. Calls the get_level_2_folders function to find all level 2 folders and their last modified dates.
# 4. Creates a CSV file named "level_2_folders.csv" and writes the data into it.
# 5. Script prints a success message or a message indicating that no level 2 folders were found.

import os
import csv

# Function to get level 2 folders and their last modified dates
def get_level_2_folders(directory):
    level_2_folders = []

    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if len(dir_path.split(os.sep)) - len(directory.split(os.sep)) == 2:
                last_modified = os.path.getmtime(dir_path)
                level_2_folders.append((dir_name, dir_path, last_modified))
    
    return level_2_folders

# Function to create a CSV file
def create_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Folder Name", "Folder Path", "Last Modified Date"])
        csv_writer.writerows(data)

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ")

    if not os.path.exists(directory_path):
        print("Directory does not exist.")
    else:
        level_2_folders_data = get_level_2_folders(directory_path)
        if level_2_folders_data:
            csv_file_path = "level_2_folders.csv"
            create_csv(csv_file_path, level_2_folders_data)
            print(f"CSV file '{csv_file_path}' has been created successfully.")
        else:
            print("No level 2 folders found in the directory.")
