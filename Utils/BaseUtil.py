#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time     : 2022/1/19 16:22
# @Author   : YuLei
# @Filename : BaseUtil.py
import os
import re


# Todo: 用于执行一些 shell 命令
import shutil


class BaseUtil:
    TMP_PATH = 'tmp'
    TMP_PATH_DICT = {
        ".java": 'java',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_diff_files(old_rev, new_rev, ref_name) -> list[str]:
        """ 用于获取 git 两个版本之间发生变动的文件名

        :param old_rev:  旧版本的 hash
        :param new_rev:  新版本的 hash
        :param ref_name: 分支
        :return:
            diff_files_list：发生变动的文件名列表
        """
        diff_files_list = []

        cmd = f'''git diff --name-only {old_rev} {new_rev}'''
        for echo_line in os.popen(cmd).readlines():
            echo_line = echo_line.strip()
            diff_files_list.append(echo_line)

        return diff_files_list

    @staticmethod
    def mk_tmp_dir(base_path: str):
        """ 用于在指定路径下创建存档临时文件所需要的目录

        :param base_path: 存放临时目录的基础路径
        :return: None

        >>> BaseUtil.mk_tmp_dir("E:/3_gitlab_checker/CodeChecker")
        """
        for key, value in BaseUtil.TMP_PATH_DICT.items():
            target_path = os.path.join(base_path, os.path.join(BaseUtil.TMP_PATH, value))
            if not os.path.exists(target_path):
                os.makedirs(target_path)

    @staticmethod
    def rm_tmp_dir(base_path: str):
        """ 用于删除临时目录

        :param base_path: 存放临时目录的基础路径
        :return: None

        # >>> BaseUtil.rm_tmp_dir("E:/3_gitlab_checker/CodeChecker")
        """
        target_path = os.path.join(base_path, BaseUtil.TMP_PATH)
        if os.path.exists(target_path):
            shutil.rmtree(os.path.join(base_path, BaseUtil.TMP_PATH))

    @staticmethod
    def move_tmp_file(new_rev, base_path, filename):
        """

        :param new_rev:   新版本的 hash
        :param base_path: 存放临时目录的基础路径
        :param filename:  移动的文件名
        :return:

        # >>> BaseUtil.move_tmp_file("d308dc331ba9effd34d9f37b887d0f3d54665e1d", "E:/3_gitlab_checker/CodeChecker", "README.md")
        """
        try:
            file_extension_name = os.path.splitext(filename)[1].lower()
            target_path = os.path.join(base_path,
                                       os.path.join(BaseUtil.TMP_PATH,
                                                    BaseUtil.TMP_PATH_DICT[file_extension_name])
                                       )
            cmd = f'''git show {new_rev}:{filename} > {target_path}/{filename}'''
            # print(cmd)
            os.popen(cmd)
        except:
            pass


