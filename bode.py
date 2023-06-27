import pandas as p
import math
from matplotlib.axis import Axis  
from matplotlib import pyplot
import matplotlib
import numpy as np
import glob

bode = True
x_intercept = None
tolerance = 1e-11
y_cheat = None

def equal_tolerance(x, y, tolerance=1e-9):
    return abs(x - y) < tolerance

def round_to(number_to_round, reference_number):
    decimal_places = len(str(reference_number).split('.')[-1])
    return round(number_to_round, decimal_places)

def format_si(value):
    units = ["p", "n", "µ", "m", "", "k", "M", "G", "T"]
    magnitude = 4
    if abs(value) > 1:
        while abs(value) >= 1000 and magnitude < len(units) - 1:
            value /= 1000
            magnitude += 1
    else:
        while abs(value) < 1 and magnitude > 0:
            value *= 1000
            magnitude -= 1
    return "{:.3f} {}".format(value, units[magnitude])

input_csvs = glob.glob("csv/*.vcsv")

pl, ax = pyplot.subplots()
count = 0
for csv_file in input_csvs:
    with open(csv_file, newline='') as file:
        for i, line in enumerate(file):
            if (i == 1):
                name_line = line.strip()
            elif (i == 4):
                label_line = line.strip()
            elif (i == 5):
                label_unit_line = line.strip()
            elif (i > 7):
                break
        csv_name = (csv_file.split("csv\\")[1]).split(".csv")[0]
        data = p.read_csv(file, sep=',', skiprows=5)

        
        for i in range(0,data.shape[1],2):
            plot_name_list = name_line.split(",")
            label_name_list = label_line.split(",")
            label_unit_list = label_unit_line.split(",")

            plot_name = plot_name_list[i//2].replace(":","_").replace(";","").replace("/","!").replace('"',"'").replace('?',".")

    if (count == 0):   
        ax1 = ax
        ax1.semilogx(data.iloc[:,0+i], data.iloc[:,1+i], linewidth=4, label=csv_name.split(".vcsv")[0], color="red")
        ax1.annotate(f'{round(data.iloc[400,1],2)} dB', xy=(data.iloc[400,0], data.iloc[400,1]), xytext=(-30, -5), textcoords='offset points', horizontalalignment='right', verticalalignment='top')
        
    elif (count > 0):
        ax2 = ax1.twinx()
        ax2.semilogx(data.iloc[:,0+i], data.iloc[:,1+i], "--", linewidth=2, label=csv_name.split(".vcsv")[0], color="blue")
        ax2.set_ylabel('Phase (deg)')
   
    pyplot.xticks(rotation = 45, weight = 'semibold')
    pyplot.yticks(weight = 'semibold')

    pyplot.xlabel(f'{label_name_list[0+i].replace(";","")} ({label_unit_list[0+i].replace(";","")})', fontdict={'weight': 'extra bold'})
    pyplot.ylabel(f'{label_name_list[1+i]} ({label_unit_list[1+i]})', fontdict={'weight': 'extra bold'})
    pl.suptitle(plot_name, fontdict={'weight': 'extra bold'})
    count += 1            

pl.tight_layout()
pyplot.xticks([0.01, 0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000])#])#

xmin, xmax = ax1.get_xlim()
log_min = np.floor(np.log10(xmin))
log_max = np.ceil(np.log10(xmax))
minor_ticks = []
for i in range(int(log_min), int(log_max)):
    major_ticks = np.logspace(i, i+1, 2)
    minor_ticks.append(np.sqrt(major_ticks[0] * major_ticks[1]))
    for j in range(1, 7):
        minor_ticks.append(minor_ticks[-1] + (major_ticks[1] - major_ticks[0]) / 9)

minor_ticks = [tick for tick in minor_ticks if tick >= xmin and tick <= xmax]

ax1.set_xticks(minor_ticks, minor=True)
ax1.tick_params(axis='x', which='minor', labelbottom=False)
ax1.grid(True, which='major', axis='both')
ax1.grid(True, which='minor', axis='x')

lines = ax1.get_lines() + ax2.get_lines()
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels)

pyplot.savefig(f"out/bode/{csv_name}-{plot_name}.png",dpi=300)