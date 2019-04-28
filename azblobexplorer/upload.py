__all__ = ['AzureBlobUpload']


class AzureBlobUpload:
    """
    Upload a file or a folder.
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

    def upload_file(self, file_path: str, upload_to: str = '.'):
        """
        Upload a file to a given blob path.

        :param upload_to:
            Give the path to upload.
        :param file_path:
            Absolute path of the file to upload.

        >>> from azblobexplorer import AzureBlobUpload
        >>> import os
        >>> az = AzureBlobUpload('account name', 'account key', 'container name')
        >>> here = os.path.abspath(os.path.dirname(__file__)) + os.sep
        >>> az.upload_file(os.path.join(here, 'file1.txt'), 'blob_folder/')
        """

        path = Path(file_path)

        if upload_to == '.':
            self.block_blob_service.create_blob_from_path(self.container_name, path.name, path)
        else:
            self.block_blob_service.create_blob_from_path(self.container_name,
                                                          upload_to + path.name, path)

    def upload_folder(self, folder_path: str, upload_to: str):
        """
        Upload a folder to a given blob path.

        :param upload_to:
            Give the path to upload.
        :param folder_path:
            Absolute path of the folder to upload.
        """
        pass
