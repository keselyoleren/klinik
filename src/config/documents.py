
import io
import re
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
            document = self.DOCS.documents().get(documentId=doc_id).execute()
            try:
                text_replace = self._extract_text_from_document(document)
                self._replace_text_in_document(doc_id, text_replace)
            except Exception as e:
                print(f"An error occurred: {e}")
            return doc_id
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        
    def _extract_text_from_document(self, document):
        text_replace = []

        for element in document['body']['content']:
            if 'paragraph' in element:
                paragraph = element['paragraph']
                for run in paragraph['elements']:
                    if 'textRun' in run:
                        text_run = run['textRun']
                        if 'content' in text_run:
                            content = text_run['content']
                            updated_content = re.findall(r"\{([^{}]*)\}", content)
                            text_replace.extend(iter(updated_content))
        tables = self._extract_tables_from_document(document)
        for table in tables:
            # Access the table data and perform operations
            rows = table['tableRows']
            for row in rows:
                cells = row['tableCells']
                for cell in cells:
                    cell_content = cell['content']
                    for content_element in cell_content:
                        if 'paragraph' in content_element:
                            paragraph = content_element['paragraph']
                            for element in paragraph['elements']:
                                if 'textRun' in element:
                                    text_run = element['textRun']
                                    if 'content' in text_run:
                                        text_content = text_run['content']
                                        updated_content = re.findall(r"\{([^{}]*)\}", text_content)
                                        text_replace.extend(iter(updated_content))
        return text_replace

    def _extract_tables_from_document(self, document):
        return [element['table'] for element in document['body']['content'] if 'table' in element]

    def _replace_text_in_document(self, document_id, text_replace):
        requests = [
            {
                'replaceAllText': {
                    'replaceText': " ",
                    'containsText': {
                        'text': '{%s}' % variable,
                        'matchCase': False
                    }
                }
            }
            for variable in text_replace
        ]
        self.DOCS.documents().batchUpdate(documentId=document_id, body={'requests':requests}).execute()


    
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
    

