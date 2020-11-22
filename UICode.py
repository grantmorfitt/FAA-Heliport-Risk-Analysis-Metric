# helloworld.py
import tkinter as tk
import pygubu
from FAARiskAnalysisFunctions import HelipadList
 
class RiskAnalysisApp:

    def __init__(self):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('RiskAnalysisUI.ui')

        #3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow')
        builder.connect_callbacks(self)
        
    def run(self):
        self.mainwindow.mainloop()
        
    def on_button1_clicked(self): #Function to control enter button
    
        textInput = self.builder.get_object('state_entry')
        LocationList = self.builder.get_object("LocationList")
        scrollbar = self.builder.get_object("scrollbar_1")
        
        scrollbar.configure(command = LocationList.yview) #Edit scrollbar to control list
        LocationList.configure(yscrollcommand = scrollbar.set)#Set list scroll to scrollbar
        
        
        state = textInput.get() #Eventually this needs to make sure it is a state
        
        padList = HelipadList(state)
        print("list generated")
        
        
      
        for i in LocationList.get_children(): #Clear old Helipad list
            LocationList.delete(i)
        
        
        for i,v in padList.iterrows():
            print(i)
            LocationList.insert('', 'end', text = str(v.lz_name) )
    

if __name__ == '__main__':
    app = RiskAnalysisApp()
    app.run()