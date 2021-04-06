import configparser
import csv
import json
import logging
import click

from BioSim.model import EnvironGenerator, BioArea

def run_trial(config, log):
    environ = EnvironGenerator(int(config['LIGHT_RAIN_CHANCE']),
                               int(config['HEAVY_RAIN_CHANCE']))
    bio1 = BioArea(environ,
                   int(config['STARTING_WATER_LEVEL']),
                   int(config['STARTING_VEG_LEVEL']),
                   int(config['FLAT_EVAPORATION']),
                   int(config['LIGHT_RAIN_AMOUNT']),
                   int(config['HEAVY_RAIN_AMOUNT']),
                   int(config['LONG_DROUGHT_DAYS']),
                   int(config['SHORT_DROUGHT_DAYS']),
                   float(config['LONG_DROUGHT_MULTIPLIER']),
                   float(config['SHORT_DROUGHT_MULTIPLIER'])
                   )
    log.debug(environ)
    log.debug(bio1)
    while bio1.vegetation > 1:
        environ.next_day()
        bio1.next_day()
        log.debug(environ)
        log.debug(bio1)

    return [str(bio1.areaNumber), str(environ.day), str(bio1.maxVegetation)]

def run_trials(config, log, num_trials):
    trial_results = {}

    log.info("Simulation Started")
    for x in range(0, num_trials):
        trial_results[x] = run_trial(config, log)

    log.info("Simulation Complete")

    return trial_results

def generate_csv_report(trial_results):
    with open('sim_output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Test Number", "Days Survived", "Max Vegetation"])

        for trial in trial_results:
            writer.writerow(trial_results[trial])

def generate_json_report(trial_results):
    with open('sim_output.json', 'w', encoding='utf-8') as f:
        json.dump(trial_results, f, ensure_ascii=False, indent=4)

@click.command()
@click.option('--num_trials', default=50, help="Number of times to iterate simulation")
def run_cli(num_trials):
    config = configparser.ConfigParser()
    config.read('sim_config.ini')

    log = logging.getLogger(__name__)

    trial_results = run_trials(config['DEFAULT'], log, num_trials)

    generate_csv_report(trial_results)
    generate_json_report(trial_results)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(asctime)s %(message)s')
    run_cli()
