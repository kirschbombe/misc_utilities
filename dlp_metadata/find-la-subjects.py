import os
import csv

def find_matching_csvs(folder_path):
    matching_csvs = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                try:
                    if has_subject_column_with_prefix(file_path, 'Actors'):
                        matching_csvs.append(file_path)
                except UnicodeDecodeError:
                    print(f"Skipped '{file_path}' due to encoding issue.")

    return matching_csvs

def has_subject_column_with_prefix(file_path, prefix, encoding='utf-8'):
    with open(file_path, 'r', newline='', encoding=encoding) as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader, None)
        if header is not None:
            header = [column.lower() for column in header]  # Convert header to lowercase
            if 'subject' in header:  # Check for 'subject' in lowercase header
                subject_index = header.index('subject')
                for row in reader:
                    if len(row) > subject_index and row[subject_index].startswith(prefix):
                        return True
    return False

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    matching_csvs = find_matching_csvs(folder_path)

    if matching_csvs:
        print("Matching CSV files:")
        for csv_file in matching_csvs:
            print(csv_file)
    else:
        print("No matching CSV files found.")
