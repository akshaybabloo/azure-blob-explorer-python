from .base import BlobBase
from .exceptions import NoBlobsFound


class AzureBlobDelete(BlobBase):
    """
    Delete file and folder from Azure blob storage.
    """

    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from Azure Storage Blob.

        :param file_name:
            Give a file name to delete/
        :rtype: bool
        :returns: ``True`` if a file is deleted.

        >>> from azblobexplorer import AzureBlobDelete
        >>> az = AzureBlobDelete('account name', 'account key', 'container name')
        >>> az.delete_file('file_name.txt')
        True
        """

        self.block_blob_service.delete_blob(self.container_name, file_name)

        return True

    def delete_files(self, file_names: list) -> bool:
        """
        Delete a list of file from Azure Storage Blob.

        :param file_names:
            Give a list of file names to delete/
        :rtype: bool
        :returns: ``True`` if files are deleted.


        >>> from azblobexplorer import AzureBlobDelete
        >>> az = AzureBlobDelete('account name', 'account key', 'container name')
        >>> blob_list = [
        ...     'folder_1/file1.txt',
        ...     'file3.txt'
        ... ]
        >>> az.delete_files(blob_list)
        True
        """

        for file in file_names:
            self.delete_file(file)

        return True

    def delete_folder(self, blob_folder_name: str) -> bool:
        """
        Delete a folder from Azure Storage Blob.

        :param blob_folder_name:
            Give a folder name to delete
        :rtype: bool
        :returns: ``True`` if a folder is deleted.
        :raises NoBlobsFound: If the blob folder is empty or is not found.

        >>> from azblobexplorer import AzureBlobDelete
        >>> az = AzureBlobDelete('account name', 'account key', 'container name')
        >>> az.delete_folder('temp/')
        True
        """

        blobs = list(self.block_blob_service.list_blobs(self.container_name, blob_folder_name))

        if len(blobs) == 0:
            raise NoBlobsFound(
                "There where 0 blobs found with blob path '{}'".format(blob_folder_name))

        for blob in blobs:
            self.delete_file(blob.name)

        return True

    def delete_container(self) -> bool:
        """
        Delete the current container.

        :rtype: bool
        :return: Returns ``True`` is the current container is deleted.

        >>> from azblobexplorer import AzureBlobDelete
        >>> az = AzureBlobDelete('account name', 'account key', 'container name')
        >>> az.delete_container()
        True
        """

        self.block_blob_service.delete_container(self.container_name)

        return True
