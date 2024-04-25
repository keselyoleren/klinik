import os
import io, re
from django.http import HttpResponse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2 import service_account
from django.conf import settings
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from urllib.parse import urlparse, parse_qs


import datetime
# Define the scope for Google Docs API


class GoogleDocumentProvider:
    def __init__(self, template_id=None, params=None, file_name=None):
        # self.SCOPES = [
        #     "https://www.googleapis.com/auth/documents",
        #     "https://www.googleapis.com/auth/documents.readonly",
        #     "https://www.googleapis.com/auth/drive",
        #     "https://www.googleapis.com/auth/drive.file",
        #     "https://www.googleapis.com/auth/drive.readonly",
        # ]
        # self.creds = None
        # if os.path.exists('token.json'):
        #     self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        # if not self.creds or not self.creds.valid:
        #     flow = InstalledAppFlow.from_client_secrets_file(
        #         'credentials.json', self.SCOPES)
        #     self.creds = flow.run_local_server(port=0)
        #     # Save the credentials for the next run
        #     with open('token.json', 'w') as token:
        #         token.write(self.creds.to_json())
        
        # self.DRIVE = build("drive", "v3", credentials=self.creds)
        # self.DOCS = build("docs", "v1", credentials=self.creds)

        self.SCOPES = [
            "https://www.googleapis.com/auth/documents",
            "https://www.googleapis.com/auth/documents.readonly",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive.readonly",
        ]
        self.creds = service_account.Credentials.from_service_account_file(settings.GOOGLE_CREDENTIALS,
                                                                           scopes=self.SCOPES)
        self.DRIVE = build("drive", "v3", credentials=self.creds)
        self.DOCS = build("docs", "v1", credentials=self.creds)
        self.template_id = template_id
        self.params = params
        self.file_name = file_name
        print(self.DRIVE)

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

    def process_document(self):
        document_id = self.copy_template()
        file_info = self.DRIVE.files().get(fileId=self.template_id, supportsAllDrives=True,
                                            supportsTeamDrives=True).execute()
        print('file info', file_info)
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
            try:
                text_replace = self._extract_text_from_document(document)
                self._replace_text_in_document(document_id, text_replace)
            except Exception as e:
                print(e)
            print(document_id)
            return document_id

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

    def create_blank_document(self):
        try: 
            body = {
                'title': 'testing name'
            }
            response = self.DOCS.documents().create(body=body).execute()
            document_id = response.get('documentId', None)
            file = self.DRIVE.files().get(fileId=document_id, fields='parents').execute()
            previous_parents = ",".join(file.get('parents'))
            self.DRIVE.files().update(fileId=document_id, addParents=settings.DOCUMENT_ROOT_DRIVE,
                                      removeParents=previous_parents, supportsAllDrives=True, supportsTeamDrives=True,
                                      fields='id, parents').execute()
            print(document_id)
            return document_id
        except HttpError as error:
            print(error)
    
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
    

