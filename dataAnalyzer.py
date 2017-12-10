import csv
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy
from collections import defaultdict

DATA_FILE_NAME = "csvfile.csv"

if __name__ == "__main__":
    csvDict = defaultdict(list)
    
    csvData = numpy.genfromtxt(DATA_FILE_NAME, dtype=int, delimiter=',', names=True)
    headers = (csvData.dtype.names)
    
    #data1 = map(data[headers[0]], data[headers[1]])
    #data2 = map(data[headers[0]], data[headers[2]])
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212)
    
    # ax.spines['top'].set_color('none')
    # ax.spines['bottom'].set_color('none')
    # ax.spines['left'].set_color('none')
    # ax.spines['right'].set_color('none')
    # ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    
    # ax.set_xlabel('Simulation #')
    # ax1.set_ylabel('Max Vegetation')
    # ax2.set_ylabel('Days Until Failure')
    
    # ax1.bar(data[headers[0]], data[headers[1]])
    # ax2.bar(data[headers[0]], data[headers[2]])
    
    # plt.show()
    
    clr = plt.get_cmap("Reds", 255)
    fig, ax = plt.subplots()
    
    plt.scatter(csvData[headers[0]], csvData[headers[1]], \
        c=csvData[headers[2]], cmap=clr, s=100, marker='o')
    ax.set_xlabel('Simulation #')
    ax.set_ylabel('Days Until Failure')
    ax.set_title('Vegetation Simulation Duration and Max Density')
    plt.show()