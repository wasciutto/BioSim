import csv
import json
import logging
import click
import configparser

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

    return {"Area Number":str(bio1.areaNumber), "Days Survived":str(environ.day), "Max Vegetation":str(bio1.maxVegetation)}

def run_trials(config, log, num_trials):
    trial_results = {}

    log.info("Simulation Started")
    for x in range(0, num_trials):
        trial_results[x] = run_trial(config, log)

    log.info("Simulation Complete")

    return trial_results

def generate_csv_report(config, trial_results):
    with open(config['CSV_REPORT_PATH'], 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(["Test Number", "Days Survived", "Max Vegetation"])

        for trial in trial_results:
            writer.writerow(trial_results[trial].values())

def generate_json_report(config, trial_results):
    with open(config['JSON_REPORT_PATH'], 'w', encoding='utf-8') as file:
        json.dump(trial_results, file, ensure_ascii=False, indent=4)

@click.command()
@click.option('--num_trials', default=50, help="Number of times to iterate simulation")
@click.option('--csv/--no-csv', default=True, help="Create a csv report.")
@click.option('--json/--no-json', default=False, help="Create a json report")
def run_cli(num_trials, csv, json):
    config = configparser.ConfigParser()
    config.read('sim_config.ini')

    log = logging.getLogger(__name__)

    trial_results = run_trials(config['DEFAULT'], log, num_trials)

    if csv: generate_csv_report(config['DEFAULT'], trial_results)
    if json: generate_json_report(config['DEFAULT'], trial_results)


if __name__ == "__main__":
    run_cli()
