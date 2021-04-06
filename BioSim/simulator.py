import configparser
import csv
import logging
import click

from BioSim.model import EnvironGenerator, BioArea

def simulate(config, log, num_trials):
    c_veg = 0
    c_days = 0
    trial_results = []

    log.info("Simulation Started")
    for x in range(0, num_trials):
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
        trial_results.append([bio1.areaNumber, str(environ.day), str(bio1.maxVegetation)])

        c_veg += bio1.maxVegetation
        c_days += environ.day

    log.info("Simulation Complete")
    log.info("Average Max Vegetation Density: " + str(c_veg / 100))
    log.info("Average Number of Days: " + str(c_days / 100))

    return trial_results

def generate_csv_report(trial_results):
    with open('sim_output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Test Number", "Days Survived", "Max Vegetation"])

        for result in trial_results:
            writer.writerow(result)

@click.command()
@click.option('--num_trials', default=50, help="Number of times to iterate simulation")
def run_cli(num_trials):
    config = configparser.ConfigParser()
    config.read('sim_config.ini')

    log = logging.getLogger(__name__)

    trial_results = simulate(config, log, num_trials)

    generate_csv_report(trial_results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
    run_cli()
