
import io
from django.http import HttpResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from django.conf import settings


import datetime
# Define the scope for Google Docs API


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
        self.creds = service_account.Credentials.from_service_account_file(settings.GOOGLE_CREDENTIALS, scopes=self.SCOPES)
        self.DRIVE = build("drive", "v3", credentials=self.creds)
        self.DOCS = build("docs", "v1", credentials=self.creds)
        self.template_id = template_id
        self.params = params
        self.file_id = file_id
        self.file_name = file_name

    def copy_template(self):
        time = datetime.datetime.now()
        try:
            body = {
                    'name': f"{self.file_name} ({time})", 
                    'parents':['1uhQrqdepaaAenyqSXqaSQr12WdQGue4b']
                }
            response = self.DRIVE.files().copy(fileId=self.template_id, supportsAllDrives=True, supportsTeamDrives=True,
                                            body=body).execute()
            return response.get('id')
        except HttpError as error:
            return error
    
    def create_document_from_template(self):
        try:
            copied_file = self.DRIVE.files().copy(
                fileId=self.template_id,
                body={"name": self.file_name}
            ).execute()
            self.file_id = copied_file.get('id')
            return self.file_id
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

    def process_document(self):
        doc_id = self.create_document_from_template()

        try:
            context = self.params.iteritems() if hasattr({}, 'iteritems') else self.params.items()
            requests = [{"replaceAllText": {"containsText": {'text': '{%s}' % key, "matchCase": True}, "replaceText": str(value) if value else '',}} for key, value in context]

            result = self.DOCS.documents().batchUpdate(
                documentId=doc_id, body={"requests": requests}).execute()

            return doc_id
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    
    def download_google_docs_as_pdf(self, document_id):
        request = self.DRIVE.files().export_media(fileId=document_id, mimeType='application/pdf')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        response = HttpResponse(fh.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.file_name}.pdf"'
        return response
    

