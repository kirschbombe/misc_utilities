import os
import pandas as pd

def process_csv(file_path):
    df = pd.read_csv(file_path)
    columns_to_modify = []

    for column in df.columns:
        if 'oclc' in column.lower():
            columns_to_modify.append(column)

    if columns_to_modify:
        for column in columns_to_modify:
            if df[column].notna().any():
                df.rename(columns={column: 'Identifier'}, inplace=True)
            else:
                df.drop(columns=column, inplace=True)
        
        df.to_csv(file_path, index=False)

def process_csv_files_in_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                process_csv(file_path)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    if os.path.exists(folder_path):
        process_csv_files_in_directory(folder_path)
    else:
        print("Folder does not exist. Please provide a valid folder path.")
