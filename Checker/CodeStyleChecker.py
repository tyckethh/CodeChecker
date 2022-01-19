#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time     : 2022/1/19 17:34
# @Author   : YuLei
# @Filename : CodeStyleChecker.py

# Todo: 用来检查各类代码风格是否符合规范
import os


class CodeStyleChecker:

    def __init__(self):
        pass

    @staticmethod
    def p3c_checker(base_path) -> tuple[bool, str]:
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
        is_syntax_correct, error_msg = CodeStyleChecker.java_p3c_checker(base_path)

        return is_syntax_correct, error_msg

    @staticmethod
    def java_p3c_checker(base_path: str) -> tuple[bool, str]:
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

        cmd_echo = os.system(cmd)
        # print(f'''cmd_echo = {cmd_echo}''')
        if int(cmd_echo) != 0:
            is_syntax_correct = False
            error_msg = 'Java 代码格式不规范，请修改后重新提交'

        return is_syntax_correct, error_msg
