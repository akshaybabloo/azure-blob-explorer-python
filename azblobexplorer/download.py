import os
from pathlib import Path

from azure.storage.blob import BlockBlobService

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

        self.block_blob_service = BlockBlobService(self.account_name, self.account_key)

    def download_file(self, blob_name: str, download_to: str = None,
                      create_directory: bool = False):
        """
        Download a file to a location.

        :param blob_name:
            Give a blob path with file name.
        :param download_to:
            Give a local absolute path to download.
        :param create_directory:
            If ``download_to`` is a directory and if it does not exists, setting this to ``True``
            will create one

        >>> from azblobexplorer import AzureBlobDownload
        >>> az = AzureBlobDownload('account name', 'account key', 'container name')
        >>> az.download_file('some/name/file.txt')
        """

        file_dict = self.read_file(blob_name)

        if download_to is None:
            write_to = Path(file_dict['file_name'])
        else:
            if not create_directory:
                if Path(download_to).exists():
                    write_to = Path(os.path.join(download_to, file_dict['file_name']))
                else:
                    raise OSError('Directory does not exists, set creat_directory=True to create.')
            else:
                os.makedirs(Path(download_to), exist_ok=True)
                write_to = Path(os.path.join(download_to, file_dict['file_name']))

        with open(write_to, 'wb') as file:
            file.write(file_dict['content'])

    def download_folder(self, folder_name: str, download_to: str):
        """
        Download a folder to a location.

        :param folder_name:
            Give a folder name.
        :param download_to:
            Give a local path to download.
        """
        pass

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

        blob_obj = self.block_blob_service.get_blob_to_bytes(self.container_name, blob_name)

        return {
            'file_name': blob_obj.name,
            'content': blob_obj.content,
            'file_size_bytes': blob_obj.properties.content_length
        }
