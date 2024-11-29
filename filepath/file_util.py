# -*- coding: utf-8 -*-
from pathlib import Path


class NotFileErr(OSError):
    """ 不是文件. """


class PathNotFound(OSError):
    """ 路径不存在. """


class FileUtils(object):
    
    @classmethod
    def path_exists(cls, path):
        return Path(path).exists()
    
    @classmethod
    def assert_path_exists(cls, path):
        if not cls.path_exists(path):
            raise PathNotFound
    
    @classmethod
    def file_exists(cls, file_path):
        p = Path(file_path)
        return p.is_file() and p.exists()

    @classmethod
    def is_file(cls, file_path):
        p = Path(file_path)
        return p.is_file()
    
    @classmethod
    def assert_is_file(cls, file_path):
        p = Path(file_path)
        if not p.is_file():
            raise NotFileErr
