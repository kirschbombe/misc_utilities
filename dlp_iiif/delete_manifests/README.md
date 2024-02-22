
Python script to delete IIIF manifests from the server.

To use:
- Create a CSV file with a list of the manifest URLs to delete. The CSV should have no header rows, only manifest URLS.
- Run `python delete_manifests.py`. The script will prompt you for a path to a CSV with a list of manifest URLs.