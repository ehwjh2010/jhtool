# -*- coding: utf-8 -*-
import json
import os.path
import shutil
import typing
from dataclasses import dataclass, field
from enum import IntEnum
from functools import partial
from pathlib import Path


class FilePathException(OSError):
    """ 文件路径异常 """


class NotFileException(FilePathException):
    """ 不是文件. """


class PathNotFoundException(FilePathException):
    """ 路径不存在. """


class DirNotFoundException(FilePathException):
    """ 不是文件夹 """


class FileTypeEnum(IntEnum):
    """ 文件类型 """
    FILE = 1
    DIR = 2


def file_ext_filter(ext: str) -> typing.Callable:
    """
    过滤文件后缀
    :param ext: 文件后缀, 后缀包含. 例如: .jpg, .png
    :return:
    """
    
    def _file_ext_filter(p: Path, suffix: str) -> bool:
        if not p.is_file():
            return False
        
        if not suffix:
            return True
        
        if p.suffix == suffix:
            return True
        
        return False
    
    return partial(_file_ext_filter, suffix=ext)


def file_keyword_filter(keyword: str) -> typing.Callable:
    """
    过滤文件名
    :param keyword: 关键字
    :return:
    """
    
    def _file_keyword_filter(p: Path, kw: str) -> bool:
        if not p.is_file():
            return False
        
        if not kw:
            return True
        
        if p.name.find(kw) != -1:
            return True
        
        return False
    
    return partial(_file_keyword_filter, kw=keyword)


class ExistUtils(object):
    # *********文件、文件是否夹存在*******
    @classmethod
    def path_exists(cls, path) -> bool:
        """ 路径是否存在 """
        return Path(path).exists()
    
    @classmethod
    def assert_path_exists(cls, path) -> typing.NoReturn:
        """ 断言路径存在 """
        if not cls.path_exists(path):
            raise PathNotFoundException
    
    @classmethod
    def file_exists(cls, file_path) -> bool:
        """ 文件是否存在 """
        p = Path(file_path)
        return p.exists() and p.is_file()
    
    @classmethod
    def assert_file_exists(cls, file_path) -> typing.NoReturn:
        """ 断言文件存在 """
        p = Path(file_path)
        if not p.exists():
            raise PathNotFoundException
        
        if not p.is_file():
            raise NotFileException
    
    @classmethod
    def dir_exists(cls, file_path) -> bool:
        """ 文件夹是否存在 """
        p = Path(file_path)
        return p.exists() and p.is_dir()
    
    @classmethod
    def assert_dir_exists(cls, file_path) -> typing.NoReturn:
        """ 断言文件夹存在 """
        p = Path(file_path)
        if not p.exists():
            raise PathNotFoundException
        if not p.is_dir():
            raise DirNotFoundException


@dataclass
class ListData(object):
    """
    name: 文件名
    abspath: 绝对路径
    file_type: 文件类型
    
    """
    name: str
    abspath: str
    file_type: int
    sub_list: typing.List['ListData'] = field(default=None)
    
    def is_file(self) -> bool:
        return self.file_type == FileTypeEnum.FILE
    
    def is_dir(self) -> bool:
        return self.file_type == FileTypeEnum.DIR


@dataclass
class FileData(object):
    """
    name: 文件名
    abspath: 绝对路径
    """
    name: str
    abspath: str
    
    @property
    def file_type(self) -> int:
        return FileTypeEnum.FILE.value
    
    def is_file(self) -> bool:
        return True
    
    def is_dir(self) -> bool:
        return False


@dataclass
class PathData(object):
    """
    last_name: 末位路径
    file_type: 文件类型
    superior_path: 上级路径
    """
    last_name: str
    file_type: int
    superior_path: str


class PathBaseUtils(object):
    
    @classmethod
    def raw_path_join(cls, root: str, *args: str) -> str:
        """ 拼接路径 """
        return str(Path().joinpath(root, *args))
    
    @classmethod
    def path_join(cls, root: str, *args: str) -> str:
        """ 拼接路径 """
        format_args = (i.removeprefix("/") for i in args)
        return str(Path().joinpath(root, *format_args))
    
    @classmethod
    def home(cls):
        """ 获取家目录 """
        return str(Path.home())
    
    @classmethod
    def pwd(cls):
        """ 获取当前目录 """
        return str(Path.cwd())
    
    @classmethod
    def abspath(cls, path: str) -> str:
        """ 获取绝对路径 """
        return os.path.abspath(path)
    
    @classmethod
    def __list_files(cls, p: Path, file_filter: typing.Callable = None) -> typing.List[FileData]:
        r = []
        for f in p.iterdir():
            if f.is_dir():
                r.extend(cls.__list_files(f, file_filter))
            else:
                if (not file_filter) or file_filter(f):
                    r.append(FileData(
                        name=f.name,
                        abspath=str(f.absolute())
                    ))
        return r
    
    @classmethod
    def list_files(cls, path: str, file_filter: typing.Callable = None) -> typing.List[FileData]:
        """
        显示路径下的所有文件
        :param path: 路径
        :param file_filter: 筛选条件, 目前支持后缀 file_ext_filter, 关键字 file_keyword_filter 筛选
        :return:
        """
        p = os.path.abspath(path)
        return cls.__list_files(Path(p), file_filter)
    
    @classmethod
    def __list_objs(cls, path: Path, filter_func: typing.Callable = None):
        r = []
        for f in path.iterdir():
            if f.is_file():
                r.append(ListData(
                    name=f.name,
                    abspath=str(f.absolute()),
                    file_type=FileTypeEnum.FILE.value
                ))
            elif f.is_dir():
                r.append(ListData(
                    name=f.name,
                    abspath=str(f.absolute()),
                    file_type=FileTypeEnum.DIR.value,
                    sub_list=cls.__list_objs(f, filter_func)
                ))
        return r
    
    @classmethod
    def list_objs(cls, path: str) -> typing.List[ListData]:
        """
        显示路径下的所有对象
        :param path: 路径
        :return:
        """
        return cls.__list_objs(Path(os.path.abspath(path)))
    
    @classmethod
    def split_path(cls, path: str) -> PathData:
        """
        分割路径
        :param path: 路径
        :return:
        """
        path = os.path.abspath(path)
        p = Path(path)
        dirname, filename = os.path.split(path)
        file_type = None
        if p.is_file():
            file_type = FileTypeEnum.FILE.value
        elif p.is_dir():
            file_type = FileTypeEnum.DIR.value
        return PathData(
            last_name=filename,
            file_type=file_type,
            superior_path=dirname
        )


class FileBaseUtils(object):
    
    @classmethod
    def get_file_name(cls, path: str) -> str:
        """
        获取文件名
        :param path: 路径
        :return:
        """
        return Path(os.path.abspath(path)).name
    
    @classmethod
    def get_file_ext(cls, path: str) -> str:
        """
        获取文件后缀
        :param path: 路径
        :return:
        """
        return Path(os.path.abspath(path)).suffix
    
    @classmethod
    def get_dir_path(cls, path: str) -> str:
        """
        获取父级目录
        :param path: 路径
        :return:
        """
        return str(Path(os.path.abspath(path)).parent)


class PathWriteUtils(object):
    @classmethod
    def rename(cls, old_path: str, new_path: str) -> typing.NoReturn:
        """
        重命名
        :param old_path: 原名称
        :param new_path: 新名称
        :return:
        """
        Path(os.path.abspath(old_path)).rename(os.path.abspath(new_path))
    
    @classmethod
    def rm_file(cls, path: str, miss_ok: bool = True) -> typing.NoReturn:
        """
        删除文件
        :param path: 文件路径
        :param miss_ok: 忽略文件不存在报错
        :return:
        """
        Path(os.path.abspath(path)).unlink(missing_ok=miss_ok)
    
    @classmethod
    def rm_dir(cls, path: str) -> typing.NoReturn:
        """
        删除目录
        :param path: 目录路径
        :return:
        """
        shutil.rmtree(os.path.abspath(path))
    
    @classmethod
    def remove(cls, path: str, miss_ok: bool = True) -> typing.NoReturn:
        """
        删除文件或目录
        :param path: 路径
        :param miss_ok: 忽略文件不存在报错
        :return:
        """
        if Path(os.path.abspath(path)).is_file():
            cls.rm_file(path, miss_ok)
        else:
            cls.rm_dir(path)
    
    @classmethod
    def copy_file(cls, src_path: str, dst_path: str) -> typing.NoReturn:
        """
        拷贝文件
        :param src_path: 源文件
        :param dst_path: 目标文件
        :return:
        """
        src, dst = os.path.abspath(src_path), os.path.abspath(dst_path)
        cls.assert_file_exists(src)
        dir_path = str(Path(dst).parent)
        os.makedirs(dir_path, exist_ok=True)
        shutil.copy(src, dst, follow_symlinks=True)
    
    @classmethod
    def copy_dir(cls, src_path: str, dst_path: str, dirs_exist_ok: bool = True) -> typing.NoReturn:
        """
        拷贝目录
        :param src_path: 源目录
        :param dst_path: 目标目录
        :param dirs_exist_ok: 忽略目录已存在
        :return:
        """
        shutil.copytree(os.path.abspath(src_path), os.path.abspath(dst_path), dirs_exist_ok=dirs_exist_ok)
    
    @classmethod
    def copy(cls, src_path: str, dst_path: str) -> typing.NoReturn:
        """
        拷贝
        :param src_path: 源路径
        :param dst_path: 目标路径
        :return:
        """
        src, dst = os.path.abspath(src_path), os.path.abspath(dst_path)
        p = Path(src)
        if not p.exists():
            raise PathNotFoundException
        
        if p.is_file():
            cls.copy_file(src, dst)
        else:
            cls.copy_dir(src, dst)
    
    @classmethod
    def copy_file_obj(cls, src: typing.IO, dst: typing.IO) -> typing.NoReturn:
        """
        :param src:
        :param dst:
        :return:
        """
        shutil.copyfileobj(src, dst)
    
    @classmethod
    def move(cls, src: str, dst: str) -> typing.NoReturn:
        """
        移动
        :param src:
        :param dst:
        :return:
        """
        shutil.move(os.path.abspath(src), os.path.abspath(dst))
    
    @classmethod
    def mkdirs(cls, path: str, exist_ok: bool = True) -> typing.NoReturn:
        """
        创建目录
        :param path: 目录路径
        :param exist_ok: 存在则忽略
        :return:
        """
        os.makedirs(os.path.abspath(path), exist_ok=exist_ok)
    
    @classmethod
    def touch(cls, path: str, exist_ok: bool = True) -> typing.NoReturn:
        """
        创建文件
        :param path: 文件路径
        :param exist_ok: 存在则忽略
        :return:
        """
        Path(os.path.abspath(path)).touch(exist_ok=exist_ok)


class FileWriteUtils(object):
    @classmethod
    def write(cls, path: str, content: typing.Union[str, bytes, typing.IO]) -> typing.NoReturn:
        """
        写文件, 只适合小文件
        :param path:
        :param content:
        :return:
        """
        _path = os.path.abspath(path)
        p = Path(_path)
        if isinstance(content, str):
            os.makedirs(os.path.dirname(_path), exist_ok=True)
            p.write_text(content)
        elif isinstance(content, bytes):
            os.makedirs(os.path.dirname(_path), exist_ok=True)
            p.write_bytes(content)
        else:
            cls.write(path, content.read())
    
    @classmethod
    def read(cls, path: str) -> bytes:
        """
        读文件, 只适合小文件
        :param path:
        :return:
        """
        cls.assert_file_exists(path)
        with open(os.path.abspath(path), 'rb') as f:
            return f.read()
    
    @classmethod
    def write_json(cls,
                   path: str,
                   data: typing.Union[list, dict],
                   ensure_ascii: bool = False,
                   indent: int = 4
                   ) -> typing.NoReturn:
        """
        写json, 只适合小文件
        :param path:
        :param data:
        :param ensure_ascii:
        :param indent:
        :return:
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(obj=data, fp=f, ensure_ascii=ensure_ascii, indent=indent)


class FilePathUtils(
    ExistUtils,
    PathBaseUtils,
    PathWriteUtils,
    FileBaseUtils,
    FileWriteUtils,
):
    """
    操作路径相关工具类
    """


if __name__ == '__main__':
    pass
