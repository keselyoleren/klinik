import os
import io
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from urllib.parse import urlparse, parse_qs


import datetime
# Define the scope for Google Docs API


class GoogleDocumentProvider:
    def __init__(self, template_id=None, params=None, file_name=None):
        self.SCOPES = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/documents.readonly",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.DRIVE = build("drive", "v3", credentials=self.creds)
        self.DOCS = build("docs", "v1", credentials=self.creds)
        self.template_id = template_id
        self.params = params
        self.file_name = file_name

    def copy_template(self):
        time = datetime.datetime.now()
        try:
            body = {'name': f"{self.file_name} ({time})"}
            response = self.DRIVE.files().copy(fileId=self.template_id, supportsAllDrives=True, supportsTeamDrives=True,
                                            body=body).execute()
            return response.get('id')
        except HttpError as error:
            return error

    def process_document(self):
        document_id = self.copy_template()
        file_info = self.DRIVE.files().get(fileId=self.template_id, supportsAllDrives=True,
                                            supportsTeamDrives=True).execute()
        if file_info['mimeType'] in ['application/vnd.google-apps.document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            context = self.params.iteritems() if hasattr({}, 'iteritems') else self.params.items()
            reqs = [{'replaceAllText': {
                'containsText': {
                    'text': '{%s}' % str(key),
                    'matchCase': False,
                },
                'replaceText': str(value) if value else '',
            }} for key, value in context]
            response = self.DOCS.documents().batchUpdate(body={'requests': reqs}, documentId=document_id, fields='').execute()
            document_id = response.get('documentId')
            document = self.DOCS.documents().get(documentId=document_id).execute()
            
            return f"https://docs.google.com/document/d/{document_id}/edit"
    
    def download_google_docs_as_pdf(self, url):
        # Parse the Google Docs URL to extract the document ID
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        document_id = query_params['id'][0]

        # Authenticate with Google Drive API using credentials.json
        creds = Credentials.from_authorized_user_file('credentials.json', scopes=['https://www.googleapis.com/auth/drive'])
        service = build('drive', 'v3', credentials=creds)

        try:
            # Export the Google Docs document as PDF
            request = service.files().export_media(fileId=document_id, mimeType='application/pdf')
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

            # Prepare HTTP response to serve the PDF file as a downloadable attachment
            response = HttpResponse(fh.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="downloaded_document.pdf"'
            return response

        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

document_id = '1q7V1wYTGRjr6PnCLFssaQaIH2h9baIwDguXgj9q5Wv8'
params = {
            "nama":"M hadi Sasmito",
            "alamat":"jalan damai sekali"
        }
file_name = 'document format'
# file_id = GoogleDocumentProvider(document_id, params, file_name).process_document()
# print(file_id)