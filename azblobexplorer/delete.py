class AzureBlobDelete:
    """
    Delete file and folder from Azure blob storage.
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

    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from Azure Storage Blob.

        :param file_name:
            Give a file name to delete/
        :rtype: bool
        :returns: ``True`` if a folder is deleted.
        """
        pass

    def delete_folder(self, folder_name: str) -> bool:
        """
        Delete a folder from Azure Storage Blob.

        :param folder_name:
            Give a folder name to delete
        :rtype: bool
        :returns: ``True`` if a folder is deleted.
        """
        pass

    def delete_container(self) -> bool:
        """
        Delete the current container.

        :return: bool
        """
        pass
