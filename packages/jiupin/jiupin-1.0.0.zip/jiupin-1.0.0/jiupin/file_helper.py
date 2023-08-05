# -*- coding: utf-8 -*-
# boois flask 框架,作者:周骁鸣 boois@qq.com
"""file_helper模块用来统一文件的读写操作"""
import os


def write(path, content, override=False):
    """写入一个文件"""
    if not override:
        if os.path.exists(path):
            return

    # 检测目录是否存在,不存在则创建
    pdir = os.path.dirname(path)
    if not os.path.exists(pdir):
        os.makedirs(pdir)

    with open(path, "w+") as _file:
        _file.write(content)
        _file.close()


def write_b(path, data):
    """用二进制流方式写入一个文件"""
    if data is None or data == "":
        return
    with open(path, "wb") as _file:
        _file.write(data)
        _file.flush()
        _file.close()


def read(path):
    """读取一个文件"""
    with open(path) as _file:
        content = _file.read()
        _file.close()
        return content
