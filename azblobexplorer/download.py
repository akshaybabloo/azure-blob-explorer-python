import os
from datetime import datetime, timedelta
from pathlib import Path

from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas

from .exceptions import NoBlobsFound

__all__ = ['AzureBlobDownload']


class AzureBlobDownload:
    """
    Download a file or folder.
    """

    def __init__(self, account_name: str, account_key: str, container_name: str):
        """
        :param account_name:
            Azure storage account name.
        :param account_key:
            Azure storage key.
        :param container_name:
            Azure storage container name, URL will be added automatically.
        """
        self.account_name = account_name
        self.account_key = account_key
        self.container_name = container_name

        block_blob_service = BlobServiceClient.from_connection_string(
            f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net")
        self.container_client = block_blob_service.get_container_client(self.container_name)

    def download_file(self, blob_name: str, download_to: str = None):
        """
        Download a file to a location.

        :param blob_name:
            Give a blob path with file name.
        :param download_to:
            Give a local absolute path to download.
        :raises OSError: If the directory for ``download_to`` does not exists

        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.download_file('some/name/file.txt')
        """

        file_dict = self.read_file(blob_name)
        file_name = Path(file_dict['file_name']).name

        if download_to is None:
            write_to = file_name
        else:
            write_to = Path(os.path.join(download_to, file_name))
            write_to.parent.mkdir(parents=True, exist_ok=True)

        with open(write_to, 'wb') as file:
            file.write(file_dict['content'])

    def download_folder(self, blob_folder_name: str, download_to: str = None):
        """
        Download a blob folder.

        :param blob_folder_name:
            Give a folder name.
        :param download_to:
            Give a local path to download.
        :raises NoBlobsFound: If the blob folder is empty or is not found.
        :raises OSError: If the directory for ``download_to`` does not exists

        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.download_folder('some/folder/name')
        """

        blobs = list(self.container_client.list_blobs(blob_folder_name))

        if len(blobs) == 0:
            raise NoBlobsFound(
                "There where 0 blobs found with blob path '{}'".format(blob_folder_name))

        if download_to is None:
            for blob in blobs:
                name = blob['name']
                path = Path(name)
                path.parent.mkdir(parents=True, exist_ok=True)
                _blob = self.read_file(name)
                file = open(path, 'wb')
                file.write(_blob['content'])
                file.close()
        else:
            for blob in blobs:
                name = blob['name']
                path = Path(os.path.join(download_to, name))
                path.parent.mkdir(parents=True, exist_ok=True)
                _blob = self.read_file(name)
                file = open(path, 'wb')
                file.write(_blob['content'])
                file.close()

    def read_file(self, blob_name: str) -> dict:
        """
        Read a file.

        :param blob_name:
            Give a file name.
        :return:
            Returns a dictionary of name, content,

        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.read_file('some/name/file.txt')
        {
            'file_name': 'file.txt',
            'content': byte content,
            'file_size_bytes': size in bytes
        }
        """

        blob_obj = self.container_client.get_blob_client(blob_name)
        blob_properties = blob_obj.get_blob_properties()
        download_blob = blob_obj.download_blob()

        return {
            'file_name': blob_properties['name'],
            'content': download_blob.readall(),
            'file_size_bytes': blob_properties['size']
        }

    def generate_url(self, blob_name: str, read: bool = True, add: bool = False,
                     create: bool = False, write: bool = False, delete: bool = False,
                     sas: bool = False, access_time: int = 1) -> str:
        """
        Generate's blob URL. It can also generate Shared Access Signature (SAS) if ``sas=True``.

        :param write: Write access
        :param create: Create access
        :param add: Add access
        :param read: Read access
        :param delete: Delete access
        :param access_time: Time till the URL is valid
        :param blob_name: Name of the blob, this could be a path
        :param sas: Set ``True`` to generate SAS key
        :return: Blob URL

        **Example without ``sas``**

        >>> import os
        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.generate_url("filename.txt")
        https://containername.blob.core.windows.net/blobname/filename.txt

        **Example with ``upload_to`` and ``sas``**

        >>> import os
        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.generate_url("filename.txt", sas=True)
        https://containername.blob.core.windows.net/blobname/filename.txt?se=2019-11-05T16%3A33%3A46Z&sp=w&sv=2019-02-02&sr=b&sig=t%2BpUG2C2FQKp/Hb8SdCsmaZCZxbYXHUedwsquItGx%2BM%3D
        """

        blob = self.container_client.get_blob_client(blob_name)

        if sas:
            sas_token = generate_blob_sas(
                blob.account_name,
                blob.container_name,
                blob.blob_name,
                account_key=blob.credential.account_key,
                permission=BlobSasPermissions(read, add, create, write, delete),
                expiry=datetime.utcnow() + timedelta(hours=access_time)
            )
            return blob.url + '?' + sas_token
        else:
            return blob.url

    def generate_url_mime(self, blob_name: str, mime_type: str, sas: bool = False,
                          read: bool = True, add: bool = False, create: bool = False,
                          write: bool = False, delete: bool = False, access_time: int = 1) -> str:
        """
        Generate's blob URL with MIME type. It can also generate Shared Access Signature (SAS) if ``sas=True``.

        :param write: Write access
        :param create: Create access
        :param add: Add access
        :param read: Read access
        :param delete: Delete access
        :param access_time:
        :param blob_name: Name of the blob
        :param access_time: Time till the URL is valid
        :param mime_type: MIME type of the application
        :param sas: Set ``True`` to generate SAS key
        :return: Blob URL

        >>> import os
        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.generate_url_mime("filename.zip", sas=True, mime_type="application/zip")
        https://containername.blob.core.windows.net/blobname/filename.zip?se=2019-11-05T16%3A33%3A46Z&sp=w&sv=2019-02-02&sr=b&sig=t%2BpUG2C2FQKp/Hb8SdCsmaZCZxbYXHUedwsquItGx%2BM%3D
        """

        blob = self.container_client.get_blob_client(blob_name)

        if sas:
            sas_token = generate_blob_sas(
                blob.account_name,
                blob.container_name,
                blob.blob_name,
                account_key=blob.credential.account_key,
                permission=BlobSasPermissions(read, add, create, write, delete),
                expiry=datetime.utcnow() + timedelta(hours=access_time),
                content_type=mime_type
            )
            return blob.url + '?' + sas_token
        else:
            return blob.url
