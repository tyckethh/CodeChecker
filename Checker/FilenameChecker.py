#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time     : 2022/1/19 17:34
# @Author   : YuLei
# @Filename : FilenameChecker.py

import os
import re


class FilenameChecker:
    CODE_FILE_EXTENSION_NAME = ('.java', '.py')

    def __init__(self):
        pass

    @staticmethod
    def filename_checker(filename: str) -> tuple:
        """ 用于检测各类文件名是否符合规范
        规范请见相应类别的文件检测函数

        :param filename: 包括相对路径的文件名
        :return:
            is_syntax_correct：True 符合规范；False 不符合规范
            error_msg: 错误信息
        """
        is_syntax_correct = True
        error_msg = ''

        # 检查代码类文件文件名是否符合规范
        if filename.endswith(FilenameChecker.CODE_FILE_EXTENSION_NAME):
            is_syntax_correct, error_msg = FilenameChecker.code_filename_checker(filename)

        return is_syntax_correct, error_msg

    @staticmethod
    def code_filename_checker(filename: str) -> tuple:
        """ 用于判断代码的文件名是否符合规范。
        存放代码的文件夹应该只包括数字字母下划线
        代码文件名只能包括字母、数字和下划线

        :param filename: 包括相对路径的文件名
        :return:
            is_syntax_correct：True 符合规范；False 不符合规范
            error_msg: 错误信息

        # >>> FilenameChecker.code_filename_checker("AAAA__ni123_.java")
        # (True, '')
        # >>> FilenameChecker.code_filename_checker("AAAA你好.java")
        # (False, '"AAAA你好.java" 不符合代码类文件名规范。代码类文件名应只包含数字、字母、下划线')
        """
        is_syntax_correct = True
        error_msg = ''

        # 获取路径、文件名、去掉后缀的文件名
        dir_name = os.path.dirname(filename)
        base_name = os.path.basename(filename)
        base_name_no_suffix = os.path.splitext(base_name)[0]

        # 正则表达式判断不包含路径和后缀的文件名是否存在非法字符
        regex_str = r'[^a-zA-Z0-9_]'
        if re.search(regex_str, base_name_no_suffix):
            is_syntax_correct = False
            error_msg = f'''"{filename}" 不符合代码类文件名规范。代码类文件名应只包含数字、字母、下划线'''

        # 正则表达式判断路径是否是否存在非法字符
        regex_str = r'[^a-zA-Z0-9_/]'
        if re.search(regex_str, dir_name):
            is_syntax_correct = False
            error_msg = f'''"{filename}" 不符合存放代码的文件夹规范。代码类文件夹应只包含数字、字母、下划线'''

        return is_syntax_correct, error_msg
