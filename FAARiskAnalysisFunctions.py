"""
# Author: Grant Morfitt
# Description: Functions required to generate Risk Analysis Metric
# Output : N/A
"""
import pandas as pd
import tkinter as tk #will be used for generating GUI

#data = None;

obstacleData = pd.read_csv('DOF.CSV',encoding='ISO-8859-1')
LZData = pd.read_csv('LZControl-Data_20201005.csv',encoding='ISO-8859-1')


#Dump both sets of data into dics, after sorting out non important information. 
#Radius of obstacle must be considered before filtering out non relevant obstacles




"""
window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
tk.mainloop()
"""