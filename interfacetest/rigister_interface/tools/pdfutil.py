#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: jutao
@version: V1.0
@file: pdfutil.py
@date: 2021/12/16 0016
"""
import fitz


def get_pdf_picture(pdf_file_path, save_dir):
    pdf = fitz.open(pdf_file_path)
    for i in range(len(pdf)):
        img_list = pdf.get_page_images(i)
        for j, img in enumerate(img_list):
            xref = img[0]
            pix = fitz.Pixmap(pdf, xref)   # make pixmap from image
            if pix.n - pix.alpha < 4:      # can be saved as PNG
                pix.save(save_dir + "/p%s-%s.png" % (i+1, j+1))
            else:                          # CMYK: must convert first
                pix0 = fitz.Pixmap(fitz.csRGB, pix)
                pix0.save(save_dir + "p%s-%s.png" % (i+1, j+1))
