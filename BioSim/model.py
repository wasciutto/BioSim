import random
import math

from enum import Enum

class PrecipLevel(Enum):
    NONE = 0
    LIGHT = 1
    HEAVY = 2


class EnvironGenerator:
    
    def __init__(self, light_rain_chance, heavy_rain_chance):
        self.light_rain_chance = light_rain_chance
        self.heavy_rain_chance = heavy_rain_chance
        self.precipLevel = self.gen_precip_level()
        self.day = 0
    
    def __str__(self):
        return "\nDay: " + str(self.day) \
        + "\nPrecipitation Level: " + str(self.precipLevel) + "\n"
    
    def next_day(self):
        self.precipLevel = self.gen_precip_level()
        self.day += 1

    def gen_precip_level(self):
        odds = random.randint(0,100)
        if self.light_rain_chance <= odds < self.heavy_rain_chance:
            return PrecipLevel.LIGHT
        elif odds >= self.heavy_rain_chance:
            return PrecipLevel.HEAVY
        else:
            return PrecipLevel.NONE
    

class BioArea:
    areaNumber = 0
    
    def __init__(self, environment, starting_water_level, starting_veg_level, flat_evaporation, light_rain_amount,
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
        self.environment = environment
        self.vegeplier = 0
        self.maxVegetation = 0
        self.droughtStreak = 0
    
    #
    def next_day(self):
        """Call order for bio area simulation actions."""
        
        self.drain_water()
        self.check_precip()
        self.check_drought_streak()
        self.set_vegeplier()
        self.set_vegetation()
        
        #Record maximum vegetation value
        if (self.vegetation > self.maxVegetation):
            self.maxVegetation = self.vegetation

    def drain_water(self):
        """Removes water based on water absorption factors."""

        #Standard evaporation
        self.lower_water(self.flat_evaporation)
        
        #Vegetation absorption formula
        absorption_rate = round(self.vegetation * (1/100), 2)
        self.lower_water(absorption_rate)
    

    def check_precip(self):
        """Increases water level based on precipitation."""

        if self.environment.precipLevel == PrecipLevel.LIGHT:
            self.raise_water(self.light_rain_amount)
        elif self.environment.precipLevel == PrecipLevel.HEAVY:
            self.raise_water(self.heavy_rain_amount)
    
    def set_vegeplier(self):
        #drought multiplier (overrides vegetation growth formula)
        if self.droughtStreak > self.long_drought_days:
            self.vegeplier = self.long_drought_multiplier
        elif self.droughtStreak > self.short_drought_days:
            self.vegeplier = self.short_drought_multiplier
        #vegetation growth formula
        #vegeplier ranges from .75 to 1.25
        else: 
            self.vegeplier = 1 + round(((self.waterLevel - 50) * (1/200)),2)

    def check_drought_streak(self):
        """Increases drought streak by 1 if water level is 0."""
        if self.waterLevel == 0:
            self.droughtStreak += 1
        else:
            self.droughtStreak = 0    
    
    def lower_water(self, amount):
        self.waterLevel = round(self.waterLevel - amount, 2)
        if self.waterLevel < 0:
            self.waterLevel = 0
            
    def raise_water(self, amount):
        self.waterLevel = round(self.waterLevel + amount, 2)
        if self.waterLevel > 100:
            self.waterLevel = 100
    
    def set_vegetation(self):
        self.vegetation = math.floor(self.vegeplier * self.vegetation)
        #if (self.vegetation > 1000):
        #    self.vegetation = 1000
        
    def __str__(self):
       return "\nArea #" + str(self.areaNumber) \
       + "\nWater Level: " + str(self.waterLevel) \
       + "\nVegetation: " + str(self.vegetation) \
       + "\nVegeplier: x" + str(self.vegeplier) + "\n"
        


    
    