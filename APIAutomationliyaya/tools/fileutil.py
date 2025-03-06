#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: caijj
@version: V1.0
@file: fileutil.py
@time: 2021/09/20
"""

import os
import docx


def get_docx_file_content(file_path):
    doc = docx.Document(file_path)
    full_content = []
    for i in doc.paragraphs:
        full_content.append(i.text)
    return '\n'.join(full_content)


def delete_file(file_path):
    os.remove(file_path)


if __name__ == '__main__':
   pass
