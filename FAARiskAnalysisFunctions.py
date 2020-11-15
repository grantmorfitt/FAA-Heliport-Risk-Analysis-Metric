"""
# Author: Grant Morfitt
# Description: Functions required to generate Risk Analysis Metric
# Output : N/A
"""

import pandas as pd
from geopy.distance import geodesic #Used for distance measurements of obstacles 
import tkinter as tk #will be used for generating GUI


airportData = {}
obstacleData = {} 
sortedObstacleData = {}

obstacleData = pd.read_csv('DOF.CSV',encoding='ISO-8859-1')
LZData = pd.read_csv('LZControl-Data_20201005.csv',encoding='ISO-8859-1')



#Testing with just NJ
airportData = LZData[LZData.lz_state == 'NJ']
sortedObstacleData = obstacleData[obstacleData.STATE == "NJ"]
#####################


def ObstaclesInArea(coordinates,obstacleList, dist):
    #Function inputs coordinates, a list of FAA Obstacles, and a distance(in nm) and returns
    #a DataFrame of obstacles that was within that distance
    
    obstacleNearLocation = pd.DataFrame() #Create empty dataframe
    
    for i,row in obstacleList.iterrows(): #Iterate through our obstacle list to compare distance from coordinates

        currentCoords = (row['LATDEC'], row['LONDEC'])
        distance = geodesic(coordinates, currentCoords).nm #Calculate distance from objects
     
        if distance <= dist:   
         
            df = pd.DataFrame(row).T
            df["Distance"] = distance #Add distance of obstacle to coordinates
        
            obstacleNearLocation = obstacleNearLocation.append(df) #Add to main dataframe
    
    obstacleNearLocation = obstacleNearLocation.reset_index(drop = True) #Removes the original index from the FAA Dataset
    
    return obstacleNearLocation

#Test the function
Obstacles = ObstaclesInArea((39.7, -75.033),sortedObstacleData,1)


#Next step is to iterate through LZData and compile obstacles for each set of coordinates 

#Testing GUI Stuff
"""
window = tk.Tk()
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
tk.mainloop()
"""