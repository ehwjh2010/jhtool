# -*- coding: utf-8 -*-
import io
import shutil
from typing import List, Iterator, Dict, IO

from python_calamine import CalamineWorkbook


class SimpleExcelReader(object):
    """
    读取excel, 只适合小文件
    """
    
    def __init__(self, filename: str = None, filelike: IO = None):
        self.filename = filename
        self._filelike = filelike
    
    @property
    def filelike(self):
        """
        获取filelike
        :return:
        """
        if self.filename and (not self._filelike):
            self._filelike = io.BytesIO()
            with open(self.filename, 'rb') as f:
                shutil.copyfileobj(f, self._filelike)
        self._filelike.seek(0)
        return self._filelike
    
    def sheet_data_iter(self, sheet_index: int = None, sheet_name: str = None) -> Iterator[Dict[str, str]]:
        """
        读取excel数据, 只适合小文件
        :param sheet_index:
        :param sheet_name:
        :return:
        """
        workbook = CalamineWorkbook.from_filelike(self.filelike)
        if sheet_index is None and sheet_name is None:
            sheet_index = 0
        
        if sheet_index is not None:
            dst_sheet = workbook.get_sheet_by_index(sheet_index)
        else:
            dst_sheet = workbook.get_sheet_by_name(sheet_name)
        
        flag = False
        column_fields = []
        for item in dst_sheet.iter_rows():
            if not flag:
                column_fields = item
                flag = True
                continue
            yield dict(zip(column_fields, item))
    
    def sheet_data(self, sheet_index: int = None, sheet_name: str = None) -> List[Dict[str, str]]:
        """
        读取excel数据
        :param sheet_index:
        :param sheet_name:
        :return:
        """
        return list(self.sheet_data_iter(sheet_index=sheet_index, sheet_name=sheet_name))
    
    @property
    def first_sheet_data(self) -> List[Dict[str, str]]:
        """
        获取第一个sheet的数据
        :return:
        """
        return self.sheet_data(sheet_index=0)
    
    @property
    def sheet_names(self) -> List[str]:
        """
        获取sheet名称
        :return:
        """
        workbook = CalamineWorkbook.from_filelike(self.filelike)
        return workbook.sheet_names
    
    @property
    def first_sheet_name(self) -> str:
        """
        获取第一个sheet名称
        :return:
        """
        workbook = CalamineWorkbook.from_filelike(self.filelike)
        if not workbook.sheet_names:
            return ''
        return workbook.sheet_names[0]
    
    @property
    def sheet_count(self) -> int:
        """
        获取sheet数量
        :return:
        """
        workbook = CalamineWorkbook.from_filelike(self.filelike)
        return len(workbook.sheet_names)
    
    def get_sheet_columns(self, sheet_index: int = None, sheet_name: str = None) -> List[str]:
        """
        获取sheet的所有列, 默认获取第一个sheet
        :param sheet_index:
        :param sheet_name:
        :return:
        """
        workbook = CalamineWorkbook.from_filelike(self.filelike)
        if sheet_index is None and sheet_name is None:
            sheet_index = 0
        
        if sheet_index is not None:
            dst_sheet = workbook.get_sheet_by_index(sheet_index)
        else:
            dst_sheet = workbook.get_sheet_by_name(sheet_name)
        
        result = []
        for item in dst_sheet.iter_rows():
            result = item
            break
        return result
    
    @property
    def first_sheet_columns(self) -> List[str]:
        """
        获取第一个sheet的所有列
        :return:
        """
        return self.get_sheet_columns(sheet_index=0)


if __name__ == '__main__':
    excel = SimpleExcelReader(r'/Users/jh/Downloads/orders.xlsx')
    print(excel.sheet_names)
    for i in excel.sheet_data_iter():
        print(i)
