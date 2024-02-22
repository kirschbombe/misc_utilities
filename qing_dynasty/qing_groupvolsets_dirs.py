import os
import re
import shutil

def find_and_move_folders(source_dir, destination_dir):
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Regular expression to match the pattern "uclaeal_[a number]_[string]"
    pattern = r'uclaeal_([0-9]+)_'

    # Dictionary to store matching folders
    folders_dict = {}

    # Traverse the source directory and find matching folders
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)
        if os.path.isdir(folder_path):
            match = re.match(pattern, folder_name)
            if match:
                number = match.group(1)
                if number in folders_dict:
                    folders_dict[number].append(folder_path)
                else:
                    folders_dict[number] = [folder_path]

    # Move matching folders to the destination directory
    for number, folders in folders_dict.items():
        new_folder_name = f"uclaeal_{number}"
        new_folder_path = os.path.join(destination_dir, new_folder_name)

        # Create the new folder if it doesn't exist
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # Move each matching folder to the new folder
        for folder in folders:
            shutil.move(folder, new_folder_path)

if __name__ == "__main__":
    # Get source and destination directories from the user
    source_directory = input("Enter the path to the source directory: ")
    destination_directory = input("Enter the path to the destination directory: ")

    find_and_move_folders(source_directory, destination_directory)