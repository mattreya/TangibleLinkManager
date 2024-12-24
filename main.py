from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google.cloud import storage, firestore
import os

# Authentication setup
SERVICE_ACCOUNT_FILE = 'path_to_your_service_account.json'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

# Firestore setup (for metadata storage)
db = firestore.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Google Drive folder ID
FOLDER_ID = 'your_google_drive_folder_id'

def list_new_files():
    # Query Google Drive for new files in the folder
    query = f"'{FOLDER_ID}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
    return results.get('files', [])

def save_to_firestore(file_metadata):
    # Save file metadata to Firestore
    db.collection('project_tangibles').add(file_metadata)

def main():
    files = list_new_files()
    for file in files:
        metadata = {
            'id': file['id'],
            'name': file['name'],
            'link': file['webViewLink']
        }
        save_to_firestore(metadata)
        print(f"Saved: {file['name']} -> {file['webViewLink']}")

if __name__ == '__main__':
    main()
