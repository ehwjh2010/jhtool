# -*- coding: utf-8 -*-
import io
from typing import List

from openpyxl import Workbook


class SimpleExcelWriter(object):
    """
    excel 写入, 只适合小文件
    """
    
    @classmethod
    def save(cls, content: List[List[str]], filename: str, headers: List[str]):
        """
        保存到本地文件
        :param content: 内容
        :param filename: 文件地址, 文件格式: .xlsx
        :param headers: 表头
        :return:
        """
        wb = Workbook()
        ws = wb.active
        if headers:
            ws.append(headers)
        
        if content:
            for item in content:
                ws.append(item)
        
        wb.save(filename)
    
    @classmethod
    def virtual_save(cls, content: List[List[str]], headers: List[str]):
        """
        保存到内存
        :param content: 内容
        :param headers: 表头
        :return:
        """
        wb = Workbook()
        ws = wb.active
        if headers:
            ws.append(headers)
        
        if content:
            for item in content:
                ws.append(item)
        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        return buffer
