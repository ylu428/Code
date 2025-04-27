'''
Wafer ID stacker for inline spc data analysis
yi-han lu
'''

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def IDstack(df):
    LotID = [df.iloc[[i],[0]].to_string(header=False, index=False)[:7] for i in range(len(df))]
    WaferID = []
    for j in range(len(LotID)):
        for i in range(25):
            if df.iloc[[j], [i+8]].to_string(header=False, index=False) != 'NaN':
                slotNo = df.iloc[[j], [i+8]].values 
                slotNo2 = str(int(slotNo)).rjust(2, '0')    # make every element in slotNo into a string of two digits
                WaferID.append(LotID[j] + slotNo2)
    return WaferID

file = filedialog.askopenfilename()
dir_path = os.path.dirname(os.path.realpath(file)) #get filepath
df=pd.read_excel(file,header = 0)
data = pd.DataFrame(IDstack(df))
data.to_csv(dir_path+'\Wafer_ID.txt', sep='\t',
            index=False, header = 0)
data.to_clipboard(index=False, header = 0)

        


