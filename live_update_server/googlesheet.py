import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
from utils import parse_gspread_date


class GoogleSheetReader():
    """ Class provides raw access to a given Google Doc's single sheet via gspread"""

    def __init__(self, credentials_file, reauthorize_interval=60*15, logger=None):
        """ Create a Google Sheet access object with the given credentials, sheet name, and intervals in seconds to reauthorize the gspread client"""

        self._credentials = credentials_file
        self._reauthorize_interval = reauthorize_interval

        self._client = self._new_client()
        self._logger = logger

    def get_sheet(self, doc_name, sheet_name):
        
        active_document = self._get_doc(doc_name)

        # iterate over all sheets and retrieve the one matching our sheet name
        for sheet in active_document.worksheets():
            if sheet_name == sheet.title:
                return sheet

    def get_doc_id(self, doc_name):
        return self._get_doc(doc_name).id

    def _get_doc(self, doc_name):
        self._reauth_client_if_expired()
        all_google_docs = self._client.openall()
        if self._logger is not None:
            self._logger.log("Authorized Google docs: {0}".format(all_google_docs))
        
        for doc in all_google_docs:
            if doc.title == doc_name:
                return doc

    def _new_client(self):
        self._client_created = datetime.now()
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self._credentials, scope)
        return gspread.authorize(creds)

    def _reauth_client_if_expired(self):
        if (datetime.now() - self._client_created).total_seconds() > self._reauthorize_interval:
            self._client = self._new_client()