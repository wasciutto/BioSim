import random
import math
import configparser

from enum import Enum

class Precipitation(Enum):
    NONE = 0
    LIGHT = 1
    HEAVY = 2


class EnvironGenerator:
    
    def __init__(self, light_rain_chance, heavy_rain_chance):
        self.light_rain_chance = light_rain_chance
        self.heavy_rain_chance = heavy_rain_chance
        self.precipLevel = self.genPrecipLevel()
        self.day = 0
    
    def __str__(self):
        return "Day: " + str(self.day) \
        + "\nPrecipitation Level: " + str(self.precipLevel) + "\n"
    
    def nextDay(self):
        self.precipLevel = self.genPrecipLevel()
        self.day += 1
    
    #0 indicates no precip, 1 indicates light precip, 2 indicates heavy precip
    def genPrecipLevel(self):
        odds = random.randint(0,100)
        if (odds >= self.light_rain_chance and odds < self.heavy_rain_chance):
            return Precipitation.LIGHT
        elif (odds >= self.heavy_rain_chance):
            return Precipitation.HEAVY
        else:
            return Precipitation.NONE
    

class BioArea:
    areaNumber = 0
    
    def __init__(self, environ, starting_water_level, starting_veg_level, flat_evaporation, light_rain_amount,
                 heavy_rain_amount, long_drought_days, long_drought_multiplier, short_drought_days,
                 short_drought_multiplier):
        self.waterLevel = starting_water_level
        self.vegetation = starting_veg_level
        self.flat_evaporation = flat_evaporation
        self.light_rain_amount = light_rain_amount
        self.heavy_rain_amount = heavy_rain_amount
        self.long_drought_days = long_drought_days
        self.long_drought_multiplier = long_drought_multiplier
        self.short_drought_days = short_drought_days
        self.short_drought_multiplier = short_drought_multiplier
        BioArea.areaNumber += 1
        self.environ = environ
        self.vegeplier = 0
        self.maxVegetation = 0
        self.droughtStreak = 0
    
    #call order for bio area simulation actions
    def nextDay(self):
        
        self.drainWater()    
        self.checkPrecip()
        self.checkDroughtStreak()     
        self.setVegeplier()
        self.setVegetation()
        
        #Record maximum vegetation value
        if (self.vegetation > self.maxVegetation):
            self.maxVegetation = self.vegetation
    
    #removes water based on water absorption factors
    def drainWater(self):
        #Standard evaporation
        self.lowerWater(self.flat_evaporation)
        
        #Vegetation absorption formula
        absorptionRate = round(self.vegetation * (1/100), 2)
        self.lowerWater(absorptionRate)
    
    #increases water level based on precipitation
    def checkPrecip(self):
        if(environ.precipLevel == Precipitation.LIGHT):
            self.raiseWater(self.light_rain_amount)
        elif(environ.precipLevel == Precipitation.HEAVY):
            self.raiseWater(self.heavy_rain_amount)
    
    def setVegeplier(self):
        #drought multiplier (overrides vegetation growth formula)
        if(self.droughtStreak > self.long_drought_days):
            self.vegeplier = self.long_drought_multiplier
        elif(self.droughtStreak > self.short_drought_days):
            self.vegeplier = self.short_drought_multiplier
        #vegetation growth formula
        #vegeplier ranges from .75 to 1.25
        else: 
            self.vegeplier = 1 + round(((self.waterLevel - 50) * (1/200)),2)
    
    #increases drought streak by 1 if water level is 0
    def checkDroughtStreak(self):
        if(self.waterLevel == 0):
            self.droughtStreak += 1
        else:
            self.droughtStreak = 0    
    
    def lowerWater(self, amount):
        self.waterLevel = round(self.waterLevel - amount, 2)
        if (self.waterLevel < 0):
            self.waterLevel = 0
            
    def raiseWater(self, amount):
        self.waterLevel = round(self.waterLevel + amount, 2)
        if (self.waterLevel > 100):
            self.waterLevel = 100
    
    def setVegetation(self):
        self.vegetation = math.floor(self.vegeplier * self.vegetation)
        #if (self.vegetation > 1000):
        #    self.vegetation = 1000
        
    def __str__(self):
       return "Area #" + str(self.areaNumber) \
       + "\nWater Level: " + str(self.waterLevel) \
       + "\nVegetation: " + str(self.vegetation) \
       + "\nVegeplier: x" + str(self.vegeplier) + "\n"
        
#simulation test ground
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('sim_config.ini')


    cVeg = 0
    cDays = 0
    with open('csvfile.csv','w') as file:
    
        file.write("Test Number,Days Survived,Max Vegetation\n")
        
        for x in range(0, 50):    
            environ = EnvironGenerator(int(config['DEFAULT']['LIGHT_RAIN_CHANCE']),
                                       int(config['DEFAULT']['HEAVY_RAIN_CHANCE']))
            bio1 = BioArea(environ,
                           int(config['DEFAULT']['STARTING_WATER_LEVEL']),
                           int(config['DEFAULT']['STARTING_VEG_LEVEL']),
                           int(config['DEFAULT']['FLAT_EVAPORATION']),
                           int(config['DEFAULT']['LIGHT_RAIN_AMOUNT']),
                           int(config['DEFAULT']['HEAVY_RAIN_AMOUNT']),
                           int(config['DEFAULT']['LONG_DROUGHT_DAYS']),
                           int(config['DEFAULT']['SHORT_DROUGHT_DAYS']),
                           float(config['DEFAULT']['LONG_DROUGHT_MULTIPLIER']),
                           float(config['DEFAULT']['SHORT_DROUGHT_MULTIPLIER'])
                           )
            print(environ)
            print(bio1)
            while(bio1.vegetation > 1):
                environ.nextDay()
                bio1.nextDay()
                print(environ)
                print(bio1)
            line = str(bio1.areaNumber) + "," + str(environ.day) + "," + str(bio1.maxVegetation) + "\n"
            file.write(line)
            
            cVeg += bio1.maxVegetation
            cDays += environ.day
        
    print("Average Max Vegetation Density: " + str(cVeg / 100))
    print("Average Number of Days: " + str(cDays / 100))
    
    