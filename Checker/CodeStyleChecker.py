#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time     : 2022/1/19 17:34
# @Author   : YuLei
# @Filename : CodeStyleChecker.py


import os
import subprocess
import fileinput


class CodeStyleChecker:
    # Todo: 用来检查各类代码风格是否符合规范

    def __init__(self):
        pass

    @staticmethod
    def p3c_checker(base_path) -> tuple:
        """ 用于检测各类代码是否符合规范
        规范请见相应代码类别的文档

        :param base_path: 存放临时目录的基础路径
        :return:
            is_syntax_correct：True 符合规范；False 不符合规范
            error_msg: 错误信息
        """
        is_syntax_correct = True
        error_msg = ''

        # 检查代码类文件文件名是否符合规范
        # 1.检测 java 代码
        #is_syntax_correct, error_msg = CodeStyleChecker.java_p3c_checker(base_path)
        # 2.检测 C++ 代码
        #is_syntax_correct, error_msg = CodeStyleChecker.cpp_checker(base_path)
        # 3.检测 Python 代码
        #is_syntax_correct, error_msg = CodeStyleChecker.python_p3c_checker(base_path)
        java_live = os.path.exists({base_path} + '/tmp/java')
        cpp_live = os.path.exists({base_path} + '/tmp/c++')
        python_live = os.path.exists({base_path} + '/tmp/python')
        if java_live is True:
            is_syntax_correct, error_msg = CodeStyleChecker.java_p3c_checker(base_path)
            if is_syntax_correct is False:
                pass
            else:
                if cpp_live is True:
                    is_syntax_correct, error_msg = CodeStyleChecker.cpp_p3c_checker(base_path)
                    if is_syntax_correct is False:
                        pass
                else:
                    if python_live is True:
                        is_syntax_correct, error_msg = CodeStyleChecker.python_p3c_checker(base_path)
                    else:
                        is_syntax_correct is False
                        error_msg = ''
        else:
            if cpp_live is True:
                is_syntax_correct, error_msg = CodeStyleChecker.cpp_p3c_checker(base_path)
                if is_syntax_correct is False:
                    pass
                else:
                    if python_live is True:
                        is_syntax_correct, error_msg = CodeStyleChecker.python_p3c_checker(base_path)
            else:
                if python_live is True:
                    is_syntax_correct, error_msg = CodeStyleChecker.python_p3c_checker(base_path)
                else:
                    is_syntax_correct is False
                    error_msg = ''
        return is_syntax_correct, error_msg

    @staticmethod
    def java_p3c_checker(base_path: str) -> tuple:
        """ 用于判断 java 代码是否符合规范，基于 alibaba p3c 插件
        规范详见 《Java开发手册（嵩山版）.pdf》

        :param base_path: 存放临时目录的基础路径
        :return:
            is_syntax_correct：True 符合规范；False 不符合规范
            error_msg: 错误信息
        """
        is_syntax_correct = True
        error_msg = ''

        cmd = f'''/usr/bin/java -Dpmd.language=en -cp {base_path}/p3c-pmd-2.1.0.jar net.sourceforge.pmd.PMD ''' + \
              f'''-d {base_path}/tmp/java -R rulesets/java/ali-comment.xml,rulesets/java/ali-concurrent.xml,''' + \
              f'''rulesets/java/ali-constant.xml,rulesets/java/ali-exception.xml,rulesets/java/ali-flowcontrol.xml,''' + \
              f'''rulesets/java/ali-naming.xml,rulesets/java/ali-oop.xml,rulesets/java/ali-other.xml,''' + \
              f'''rulesets/java/ali-set.xml -f text'''

        sub = subprocess.run(cmd, shell=True)
        if int(sub.returncode) != 0:
            is_syntax_correct = False
            error_msg = 'Java 代码格式不规范，请修改后重新提交'

        return is_syntax_correct, error_msg

    @staticmethod
    def get_file_path(root_path, file_list, dir_list):
        # 获取该目录下所有的文件名称和目录名称
        dir_or_files = os.listdir(root_path)
        for dir_file in dir_or_files:
            # 获取目录或者文件的路径
            dir_file_path = os.path.join(root_path, dir_file)
            # 判断该路径为文件还是路径
            if os.path.isdir(dir_file_path):
                dir_list.append(dir_file_path)
                # 递归获取所有文件和目录的路径
                get_file_path(dir_file_path, file_list, dir_list)
            else:
                file_list.append(dir_file_path)

    @staticmethod
    def cpp_checker(base_path: str) -> tuple[bool, str]:
        error_msg=''
        is_syntax_correct=True

        # 根目录路径
        root_path = f'''{base_path}/tmp/c++'''
        # 用来存放所有的文件路径
        file_list = []
        # 用来存放所有的目录路径
        dir_list = []
        # 获取全部文件列表
        CodeStyleChecker.get_file_path(root_path, file_list, dir_list)
        for path in file_list:
            cmd = f'''cpplint {path}'''
            is_syntax_correct = subprocess.run(cmd, shell=True)
            if is_syntax_correct.returncode != 0:
                error_msg='c++ 代码格式不规范，请修改后重新提交'
                return 0, error_msg
        return True, error_msg

    @staticmethod
    def python_p3c_checker(base_path: str) -> tuple[bool, str]:
        error_msg = ''
        is_syntax_correct = True
        pylint_load = base_path +'/tmp/python'
        for root, dirs,files in os.walk(pylint_load):
            for file in files:
                pylint_file_load = os.path.join(root,file)
                cmd = f'''pylint {pylint_file_load} --disable=missing-docstring'''
                print(cmd)
                is_syntax_correct = subprocess.run(cmd, shell=True)
                if is_syntax_correct.returncode != 0:
                    error_msg = 'Python 语法存在问题'
                    return 0, error_msg
        return True, error_msg


