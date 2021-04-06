import configparser

import click
import matplotlib.pyplot as plt
import numpy

def plot_data(data: numpy.ndarray, headers: tuple):
    """Plots a weighted scatterplot of the BioArea trial data."""
    clr = plt.get_cmap("Reds", 255)
    fig, ax = plt.subplots()

    plt.scatter(data[headers[0]], data[headers[1]], c=data[headers[2]], cmap=clr, s=100, marker='o')
    ax.set_xlabel('Simulation #')
    ax.set_ylabel('Days Until Failure')
    ax.set_title('Vegetation Simulation Duration and Max Density')
    plt.show()

@click.command()
@click.option('--csv_path', default=None, help="Path to csv containing data")
def run_cli(csv_path):
    config = configparser.ConfigParser()
    config.read('sim_config.ini')
    config = config['DEFAULT']

    if csv_path is None:
        csv_path = config['CSV_REPORT_PATH']

    csv_data = numpy.genfromtxt(csv_path, dtype=int, delimiter=',', names=True)
    headers = csv_data.dtype.names

    plot_data(csv_data, headers)


if __name__ == "__main__":
    run_cli()