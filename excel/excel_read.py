# -*- coding: utf-8 -*-
import io

from python_calamine import CalamineWorkbook

from filepath import FileUtils


class ExcelReadUtils(object):
    
    def __init__(self, filename: str = None,  filelike: io.FileIO = None):
        self.filename = filename
        self.filelike = filelike

    def all_raw_data_by_calamine(self, filename, sheet_index: int = None, sheet_name: str = None):
        FileUtils.assert_path_exists(filename)
        FileUtils.assert_is_file(filename)
        
        workbook = CalamineWorkbook.from_path(filename)
        sheet_names = workbook.sheet_names
        print(sheet_names)
        
        if sheet_index is None and sheet_name is None:
            sheet_index = 0
        
        if sheet_index is not None:
            dst_sheet = workbook.get_sheet_by_index(sheet_index)
        else:
            dst_sheet = workbook.get_sheet_by_name(sheet_name)
        
        print(dst_sheet.name)
        
        
        # dst_sheet = None
        # if sheet_index is not None:
        #     dst_sheet =
        
        
        # data = {}
        # workbook = CalamineWorkbook.from_path(filename)
        # for sheet_name in workbook.sheet_names:
        #     lines = workbook.get_sheet_by_name(sheet_name).to_python()[1:]
        #     for data_id, name in lines:
        #         data[int(data_id)] = eval(name)
        # return data
    


if __name__ == '__main__':
    ExcelReadUtils().all_raw_data_by_calamine('/Users/jh/Downloads/1011-1122认证用户信息.xlsx')
