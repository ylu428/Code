# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 14:32:59 2020

@author: apm41
"""

import tabula

#import pdfplumber

import os
import tkinter as tk
from tkinter.filedialog import askdirectory
from tkinter import filedialog

# choose the directory to save the file
root = tk.Tk()
root.withdraw()

file_path = askdirectory()
os.chdir(file_path)
#os.chdir("D:\\Google Drive\\PhD in GT\\Research\\Fluorescence Anisotropy\\2019.04.19 AgNC En_OADF_N2\\0 glycerol\\Air")
###
# Choose the file
root = tk.Tk()
root.withdraw()
file_name = filedialog.askopenfilename()
# In[] tabula: give a list with three dataframe. Harder to use a for loop to convert all of the data
table= tabula.read_pdf(file_name, lattice=True, pages=12)

for i in range(13,64):
    df = tabula.read_pdf(file_name, lattice=True, pages=i)
    table.append(df, ignore_index=True)

# In[]

import pdfplumber
import pandas as pd

with pdfplumber.open(file_name) as pdf:
    page = pdf.pages[8]
    table = page.extract_tables()
    for t in table:
        # 得到的table是嵌套list类型，转化成DataFrame更加方便查看和分析
        database = pd.DataFrame(t[1:], columns=t[0])
    '''for loop for the tabels in different pages'''
    for i in range(9, 64):
        page = pdf.pages[i]
        table1 = page.extract_tables()
        for t in table1:
            df2 = pd.DataFrame(t[0:], columns=table[0][0])  # table is a list with one list consist of 19 lists. Each list contain 9 string. we just need the 9 strings in the first list of the first list. Weird, right?
#            df2 = df2[2:]
        database = database.append(df2, ignore_index=True)

database.to_csv('AgNC_sequence_database(2020).csv')             
