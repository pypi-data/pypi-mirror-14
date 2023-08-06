from __future__ import absolute_import
from __future__ import division

import arrow
from googleapiclient import http
import httplib2
import mimetypes
import os
from apiclient import discovery
from oauth2client.client import SignedJwtAssertionCredentials


AUTH_URL = 'https://www.googleapis.com/auth/drive'
API_VERSION = 'v3'


class GDriveClient(object):
    """
    this is a python client for the google drive APIs
    it is a wrapper over google-api-python-client
    ref: https://developers.google.com/drive/v3/reference/
    """

    MIME_TYPE_FOLDER = 'application/vnd.google-apps.folder'

    # MIME type conversion; taken from here
    # https://github.com/kgritesh/GDocOffice/blob/master/launcher.py

    APPLICATION_MAP = {
        'spreadsheet': ['.csv','.xls', '.xlsx', '.xlsm', '.xlt', '.xltx',
                        '.xltm' '.ods', '.tsv', '.tab'],
        'document': ['.docx', '.doc' '.docm', '.dot', '.dotx', '.dotm', '.html', '.txt',
                     '.rtf', '.odt'],
        'presentation': ['.ppt', '.pptx', '.pptm', '.pps', '.ppsx', '.ppsm', '.pot',
                         '.potx', '.potm']
    }

    def __init__(self, client_email, private_key):
        self.ext_map = self.create_ext_app_map()
        self.drive = self._authenticate(client_email, private_key)

    @staticmethod
    def _authenticate(client_email, private_key):
        credentials = SignedJwtAssertionCredentials(client_email, private_key,
                                                    AUTH_URL)
        http = credentials.authorize(httplib2.Http())
        return discovery.build('drive', API_VERSION, http=http)

    @staticmethod
    def get_mime_type_gdrive(app_type):
        return 'application/vnd.google-apps.{}'.format(app_type)

    @staticmethod
    def get_mime_type_standard(ext):
        addition_extensions = {
            '.json': 'application/json',
            '.rar': 'application/x-rar-compressed'
        }

        if ext in addition_extensions:
            return addition_extensions.get(ext)

        return mimetypes.types_map.get(ext)


    def create_ext_app_map(self):
        ext_map = {}
        for app, extensions in self.APPLICATION_MAP.items():
            for ext in extensions:
                ext_map[ext] = app
        return ext_map

    def delete_file(self, file_id):
        self.drive.files().delete(fileId=file_id).execute()

    def list_files_in_folder(self, file_id):
        """
        lists files in the google drive's given folder

        @param file_id: string: id of the parent
        @return a dict of file names to file id mapping
        """
        if file_id is None:
            return {}

        file_dict = {}
        query = "'{}' in parents and trashed = false".format(file_id) if file_id else None

        while True:
            res = self.drive.files().list(q=query,
                                          fields='nextPageToken, files(id, name)'
            ).execute()

            for file in res.get('files', []):
                file_dict[file.get('name')] = file.get('id')

            page_token = res.get('nextPageToken')

            if page_token is None:
                break

        return file_dict

    def find_file(self, file_name, parent_id=None):
        """
        Search a file with its name in drive

        @param file_name: string: file name
        @param parent_id: id of the parent: string: optional, if not specified
                          returns all the folders with the given name
        """
        if file_name is None:
            return []
        else:
            query = "name = '{}' and trashed = false".format(file_name)

            if parent_id is not None:
                query += " and '{}' in parents".format(parent_id)

            res = self.drive.files().list(q=query,
                                          fields='files(id, name)'
            ).execute()
            return res.get('files', [])

    def get_or_create_folder(self, folder_name, parent_id):
        folders = self.find_file(folder_name, parent_id)
        if not folders:
            folder_id = self.create_folder(folder_name, parent_id)
            return folder_id
        else:
            return folders[0].get('id')

    def get_files_in_folder(self, folder_name, parent_id):
        folder_id = self.get_or_create_folder(folder_name, parent_id)
        return folder_id, self.list_files_in_folder(file_id=folder_id)

    def create_folder(self, name, parent_id=None):
        """
        creates a folder in Google Drive

        @param name: string name of the folder
        @param parent_id: string unique id of the previously created folder
        """
        mime_type = self.MIME_TYPE_FOLDER

        file_metadata = {
            'name' : name,
            'parents': [parent_id],
            'mimeType': mime_type,
            'modifiedTime' : arrow.utcnow().isoformat()
        }

        file_ = self.drive.files().create(body=file_metadata,
                                          fields='id').execute()

        return file_.get('id')

    def upload_file(self, file_name, file_obj_or_path,
                    parent_id=None, in_memory_stream=False):
        """
        uploads a file to Google Drive

        @param file_name: string name of the file in gdrive
        @param file_obj_or_path: string path of the file to be uploaded
        @param parent_id: string unique id of the previously created folder
        """
        __, ext = os.path.splitext(file_name)
        app_type = self.ext_map.get(ext)

        if app_type is not None:
            mime_type = self.get_mime_type_gdrive(app_type)
        else:
            mime_type = self.get_mime_type_standard(ext)
        
        file_metadata = {
            'name': file_name,
            'parents': [parent_id],
            'mimeType': mime_type,
            'modifiedTime': arrow.utcnow().isoformat()
        }

        if in_memory_stream:
            media = http.MediaIoBaseUpload(file_obj_or_path,
                                           mimetype=mime_type,
                                           resumable=True)
        else:
            media = http.MediaFileUpload(file_obj_or_path,
                                         mimetype=mime_type,
                                         resumable=True)

        file_ = self.drive.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
        return file_.get('id')

    def upload_files(self, files_dict):
        """
        uploads multiple files at once

        @param files_dict: dict the dict will have following structure
               {
                 'file_name': {
                     'file_path': '<string>',
                     'parent_id': '<string>'
                 }
               }
        """
        res = {}
        for file_name, metadata in files_dict.iteritems():
            file_path = metadata['file_path']
            parent_id = metadata['parent_id']
            res[file_name] = self.upload_file(file_name, file_path, parent_id)
        return res
