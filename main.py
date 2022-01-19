#!/bin/python3
# -*- encoding: utf-8 -*-

import sys
import os
from Utils import *
from Checker import *

if __name__ == '__main__':
    BASE_PATH = sys.argv[1]

    for line in sys.stdin.readlines():
        old_rev, new_rev, ref_name = line.strip().split(' ')
        diff_files_list = BaseUtil.get_diff_files(old_rev, new_rev, ref_name)

        # 判断文件名是否符合规范
        for file in diff_files_list:
            is_syntax_correct, error_msg = FilenameChecker.filename_checker(file)
            if not is_syntax_correct:
                print(error_msg)
                sys.exit(1)

        # 创建各类文件的临时目录
        BaseUtil.mk_tmp_dir(BASE_PATH)

        # 将不同类别的代码文件挪动到不同的目录
        for file in diff_files_list:
            BaseUtil.move_tmp_file(new_rev, BASE_PATH, file)

        # 进行代码检查
        is_syntax_correct, error_msg = CodeStyleChecker.p3c_checker(BASE_PATH)

        # 删除各类文件的临时目录
        BaseUtil.rm_tmp_dir(BASE_PATH)

        if not is_syntax_correct:
            print(error_msg)
            sys.exit(1)
    sys.exit(0)

