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

    def download_file(self, file_name: str, download_to: str):
        """
        Download a file to a location.

        :param file_name:
            Give a blob path with file name.
        :param download_to:
            Give a local path to download.
        """
        pass

    def download_folder(self, folder_name: str, download_to: str):
        """
        Download a folder to a location.

        :param folder_name:
            Give a folder name.
        :param download_to:
            Give a local path to download.
        """
        pass

    def read_file(self, file_name: str):
        """
        Read a file.

        :param file_name:
            Give a file name.
        :return:
            A ``.read()`` file-type object.
        """
        pass
