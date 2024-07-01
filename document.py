import os
import io
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.http import HttpResponse
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from urllib.parse import urlparse, parse_qs
from decouple import config
import datetime

# Define the scope for Google Docs API
CRED = config("GOOGLE_CREDENTIALS", "./cred.json")

class GoogleDocumentProvider:
    def __init__(self, template_id=None, params=None, file_id=None, file_name=None):
        self.SCOPES = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/documents.readonly",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/drive.metadata",
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/drive.photos.readonly",
            "https://www.googleapis.com/auth/drive.scripts"
        ]
        self.creds = service_account.Credentials.from_service_account_file(CRED, scopes=self.SCOPES)
        self.DRIVE = build("drive", "v3", credentials=self.creds)
        self.DOCS = build("docs", "v1", credentials=self.creds)
        self.template_id = template_id
        self.params = params
        self.file_id = file_id
        self.file_name = file_name

    def create_document_from_template(self):
        try:
            # Copy the template document
            copied_file = self.DRIVE.files().copy(
                fileId=self.template_id,
                body={"name": self.file_name}
            ).execute()
            self.file_id = copied_file.get('id')
            return self.file_id
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def replace_text_in_document(self, doc_id, replacements):
        try:
            requests = []
            for key, value in replacements.items():
                requests.append({
                    "replaceAllText": {
                        "containsText": {
                            'text': '{%s}' % key,
                            "matchCase": True
                        },
                        "replaceText": value
                    }
                })

            result = self.DOCS.documents().batchUpdate(
                documentId=doc_id, body={"requests": requests}).execute()
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def download_document(self, file_id, file_name):
        try:
            request = self.DRIVE.files().export_media(fileId=file_id, mimeType='application/pdf')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.seek(0)

            with open(file_name, 'wb') as f:
                f.write(fh.read())
            print(f"File {file_name} saved successfully.")
            return file_name
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

# Example usage
# Initialize the provider
provider = GoogleDocumentProvider(
    template_id='1c2_9URuApDF9rkJtoFuxmFsz_3j7EXrnYanIOPH_ick',
    file_name='New Document',
    params={'name': 'John Doe', 'date': '2024-07-01'}
)

# Create a document from a template
doc_id = provider.create_document_from_template()

# Replace text in the created document
if doc_id:
    provider.replace_text_in_document(doc_id, provider.params)

# Download the document as a PDF and save it to a local file
if doc_id:
    provider.download_document(doc_id, 'Updated_Document.pdf')
