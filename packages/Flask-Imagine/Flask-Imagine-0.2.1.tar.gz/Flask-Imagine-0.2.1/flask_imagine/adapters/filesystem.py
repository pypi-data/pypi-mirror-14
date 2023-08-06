"""
This module implement a filesystem storage adapter.
"""
import errno
import os
from flask import current_app
from .interface import ImagineAdapterInterface
from PIL import Image


class ImagineFilesystemAdapter(ImagineAdapterInterface):
    """
    Filesystem storage adapter
    """
    source_folder = None
    cache_folder = None

    def __init__(self, **kwargs):
        """
        Init adapter
        :param kwargs: parameters
        :return:
        """
        if 'source_folder' in kwargs:
            self.source_folder = kwargs.pop('source_folder').strip('/')
        else:
            raise ValueError('Folder is not set.')

        self.cache_folder = kwargs['cache_folder'].strip('/')

    def get_item(self, path):
        """
        Get resource item
        :param path: string
        :return: Image
        """
        return Image.open(
            '%s/%s/%s' % (
                current_app.root_path,
                self.source_folder,
                path.strip('/')
            )
        )

    def create_cached_item(self, path, content):
        """
        Create cached resource item
        :param path: string
        :param content: Image
        :return:
        """
        item_path = '%s/%s/%s/%s' % (
            current_app.root_path,
            self.source_folder,
            self.cache_folder,
            path.strip('/')
        )
        self.make_dirs(item_path)

        content.save(item_path)

        return '/%s/%s/%s' % (self.source_folder, self.cache_folder, path.strip('/'))

    def get_cached_item(self, path):
        """
        Get cached resource item
        :param path: string
        :return:
        """
        return Image.open(
            '%s/%s/%s/%s' % (
                current_app.root_path,
                self.source_folder,
                self.cache_folder,
                path.strip('/')
            )
        )

    def check_cached_item(self, path):
        """
        Check for cached resource item exists
        :param path: string
        :return:
        """
        return os.path.isfile(
            '%s/%s/%s/%s' % (
                current_app.root_path,
                self.source_folder,
                self.cache_folder,
                path.strip('/')
            )
        )

    def remove_cached_item(self, path):
        """
        Remove cached resource item
        :param path: string
        :return:
        """
        os.remove(
            '%s/%s/%s/%s' % (
                current_app.root_path,
                self.source_folder,
                self.cache_folder,
                path.strip('/')
            )
        )

        return True

    @staticmethod
    def make_dirs(path):
        """
        Create directories if not exist
        :param path: string
        :return:
        """
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
