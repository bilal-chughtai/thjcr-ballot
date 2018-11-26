import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
from utils import parse_gspread_date


class GoogleSheetReader():
    """ Class provides raw access to a given Google Doc's single sheet via gspread"""

    def __init__(self, credentials_file, sheet_name, reauthorize_interval=60*15):
        """ Create a Google Sheet access object with the given credentials, sheet name, and intervals in seconds to reauthorize the gspread client"""

        self._credentials = credentials_file
        self._sheet_name = sheet_name
        self._reauthorize_interval = reauthorize_interval

        self._client = self._new_client()

    def get_sheet(self):
        self._reauth_client_if_expired()

        all_google_docs = self._client.openall()

        # TODO take doc name, for now just takes the most recently updated google doc
        all_google_docs.sort(key=lambda s: parse_gspread_date(s.updated), reverse=True)
        active_document = all_google_docs[0]
		
        # iterate over all sheets and retrieve the one matching our sheet name
        for sheet in active_document.worksheets():
            if self._sheet_name == sheet.title:
                return sheet
    
    def get_doc_id(self):
        self._reauth_client_if_expired()
        all_google_docs = self._client.openall()
        
        # TODO take doc name, for now just takes the most recently updated google doc

        all_google_docs.sort(key=lambda s: parse_gspread_date(s.updated), reverse=True)
        return all_google_docs[0].id

        

    def _new_client(self):
        self._client_created = datetime.now()
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self._credentials, scope)
        return gspread.authorize(creds)
    
    def _reauth_client_if_expired(self):
        if datetime.now() - self._client_created > self._reauthorize_interval:
            self._client = self._new_client()