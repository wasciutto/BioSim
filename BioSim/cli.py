import configparser
import csv
import logging

from .simulator import EnvironGenerator, BioArea

if __name__ == "__main__":
    """ Simulation test ground """
    config = configparser.ConfigParser()
    config.read('sim_config.ini')

    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
    log = logging.getLogger(__name__)

    cVeg = 0
    cDays = 0
    with open('../sim_output.csv', 'w', newline='') as file:

        writer = csv.writer(file)

        writer.writerow(["Test Number", "Days Survived", "Max Vegetation"])

        log.info("Simulation Started")
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
            log.debug(environ)
            log.debug(bio1)
            while bio1.vegetation > 1:
                environ.next_day()
                bio1.next_day()
                log.debug(environ)
                log.debug(bio1)
            writer.writerow([bio1.areaNumber, str(environ.day), str(bio1.maxVegetation)])

            cVeg += bio1.maxVegetation
            cDays += environ.day

    log.info("Simulation Complete")
    log.info("Average Max Vegetation Density: " + str(cVeg / 100))
    log.info("Average Number of Days: " + str(cDays / 100))