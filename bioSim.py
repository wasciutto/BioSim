import random
import math

NO_RAIN = 0
LIGHT_RAIN = 1
HEAVY_RAIN = 2
LIGHT_RAIN_CHANCE = 80
HEAVY_RAIN_CHANCE = 95
STARTING_WATER_LEVEL = 100
STARTING_VEG_LEVEL = 100
FLAT_EVAPORATION = 5
LIGHT_RAIN_AMOUNT = 30
HEAVY_RAIN_AMOUNT = 50
LONG_DROUGHT_DAYS = 4
SHORT_DROUGHT_DAYS = 1
LONG_DROUGHT_MULTIPLIER = .5
SHORT_DROUGHT_MULTIPLIER = .75

class EnvironGenerator:
    
    def __init__(self):
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
        if (odds >= LIGHT_RAIN_CHANCE and odds < HEAVY_RAIN_CHANCE):
            return LIGHT_RAIN
        elif (odds >= HEAVY_RAIN_CHANCE):
            return HEAVY_RAIN
        else:
            return NO_RAIN
    

class BioArea:
    areaNumber = 0
    
    def __init__(self, environ):
        self.waterLevel = STARTING_WATER_LEVEL
        self.vegetation = STARTING_VEG_LEVEL
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
        self.lowerWater(FLAT_EVAPORATION)
        
        #Vegetation absorption formula
        absorptionRate = round(self.vegetation * (1/100), 2)
        self.lowerWater(absorptionRate)
    
    #increases water level based on precipitation
    def checkPrecip(self):
        if(environ.precipLevel == LIGHT_RAIN):
            self.raiseWater(LIGHT_RAIN_AMOUNT)
        elif(environ.precipLevel == HEAVY_RAIN):
            self.raiseWater(HEAVY_RAIN_AMOUNT)
    
    def setVegeplier(self):
        #drought multiplier (overrides vegetation growth formula)
        if(self.droughtStreak > LONG_DROUGHT_DAYS):
            self.vegeplier = LONG_DROUGHT_MULTIPLIER
        elif(self.droughtStreak > SHORT_DROUGHT_DAYS):
            self.vegeplier = SHORT_DROUGHT_MULTIPLIER
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
    cVeg = 0
    cDays = 0
    with open('csvfile.csv','w') as file:
    
        file.write("Test Number,Days Survived,Max Vegetation\n")
        
        for x in range(0, 50):    
            environ = EnvironGenerator()
            bio1 = BioArea(environ)
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
    
    