import csv
import requests

def delete_urls_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        urls = [row[0] for row in reader]

    for url in urls:
        try:
            response = requests.delete(url)
            if response.status_code == 204 or response.status_code == 200:
                print(f"Successfully deleted URL: {url}")
            else:
                print(f"Failed to delete URL: {url} (Status code: {response.status_code})")
        except Exception as e:
            print(f"Error while deleting URL: {url} - {e}")

if __name__ == "__main__":
    csv_file_path = input("Enter the path to your CSV file: ")
    delete_urls_from_csv(csv_file_path)
