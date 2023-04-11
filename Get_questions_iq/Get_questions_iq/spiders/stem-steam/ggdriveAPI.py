from __future__ import print_function
import pickle
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import google.auth
#from google.cloud import storage
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# def implicit():
#
#
#     # If you don't specify credentials when constructing the client, the
#     # client library will look for credentials in the environment.
#     storage_client = storage.Client()
#
#     # Make an authenticated API request
#     buckets = list(storage_client.list_buckets())
#     print(buckets)
def main():
    """Based on the quickStart.py example at
    https://developers.google.com/drive/api/v3/quickstart/python
    """
    creds = {"web": {"client_id": "AIzaSyCPte4GFIjugzN7koKZb3DlfpWVJHF0Vao",
             "project_id": "valued-proton-341301", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
             "token_uri": "https://oauth2.googleapis.com/token",
             "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
             "client_secret": "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"}}
    creds ='AIzaSyCPte4GFIjugzN7koKZb3DlfpWVJHF0Vao'
    service = build('drive', 'v3', credentials=creds)

    folderId = "1xp_jj9j1mD9HQjRC6Ih-OZfUMsp6Sihu"
    fileID = '1c5-QxGZadePSbZk9t86ZhjOHbJqTMQgq'
    destinationFolder = r'F:\PycharmProjects\Source\Get_questions_iq\Get_questions_iq\spiders\stem-steam\Download'
    downloadFolder(service, folderId, destinationFolder)
    downloadFile(service, fileID, destinationFolder)

def downloadFolder(service, fileId, destinationFolder):
    if not os.path.isdir(destinationFolder):
        os.mkdir(path=destinationFolder)
    print('12')
    results = service.files().list(
        pageSize=300,
        q="parents in '{0}'".format(fileId),
        fields="files(id, name, mimeType)"
    ).execute()

    items = results.get('files', [])

    for item in items:
        itemName = item['name']
        itemId = item['id']
        itemType = item['mimeType']
        filePath = destinationFolder + "/" + itemName

        if itemType == 'application/vnd.google-apps.folder':
            print("Stepping into folder: {0}".format(filePath))
            downloadFolder(service, itemId, filePath)  # Recursive call
        elif not itemType.startswith('application/'):
            downloadFile(service, itemId, filePath)
        else:
            print("Unsupported file: {0}".format(itemName))


def downloadFile(service, fileId, filePath):
    # Note: The parent folders in filePath must exist
    print("-> Downloading file with id: {0} name: {1}".format(fileId, filePath))
    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(filePath, mode='wb')

    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)

        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries=2)
            if status:
                print("Download %d%%." % int(status.progress() * 100))
        print("Download Complete!")
    finally:
        fh.close()
if __name__ == '__main__':
    main()