"""
Created on Mon Jan 11 08:46:54 2021

@author: Grant E-INT Morfitt
"""


class Obstacle:
    
    def __init__(self,type = None,height = 0, latitude=0, longitude = 0,name = None, distance = 0,risk = 1):
        
        self.latitude = latitude
        self.longitude = longitude
        self.name = name
        self.distance = distance
        self.risk = risk
        self.type = type
        self.height = height
        
        
        
    