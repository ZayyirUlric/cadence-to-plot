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
            elif (i == 6):
                line1 = line.strip()
                break
        csv_name = (csv_file.split("csv\\")[1]).split(".csv")[0]

        data = p.read_csv(file, sep=',', header=None, skiprows=None)
        data.loc[-1] = [0, round(float(line1.split(",")[1]), 6)]
        data.index = data.index + 1 
        data.sort_index(inplace=True) 
        print(data.iloc[1,1])

        magnitude = [m for m in data.iloc[:,1]]
        magnitude = 10 ** (np.array(magnitude) / 20)

        for i in range(0,data.shape[1],2):
            plot_name_list = name_line.split(",")
            label_name_list = label_line.split(",")
            label_unit_list = label_unit_line.split(",")

            plot_name = plot_name_list[i//2].replace(":","_").replace(";","").replace("/","!").replace('"',"'").replace('?',".")


    ax1 = ax
    ax1.set_yscale('log')
    ax1.stem(data.iloc[:,0+i], magnitude,'b', label=csv_name.split(".vcsv")[0],   markerfmt=" ", basefmt="-b", bottom=-300)
    ax1.annotate(f'100Hz', xy=(1,1), xytext=(0, 0), textcoords='offset points', horizontalalignment='right', verticalalignment='top', zorder=-1000)

    pyplot.xticks(rotation = 45, weight = 'semibold')
    pyplot.yticks(weight = 'semibold')

    pyplot.xlabel(f'{label_name_list[0+i].replace(";","")} ({label_unit_list[0+i].replace(";","")})', fontdict={'weight': 'extra bold'})
    pyplot.ylabel(f'{label_name_list[1+i]} ({label_unit_list[1+i]})', fontdict={'weight': 'extra bold'})
    pl.suptitle(plot_name, fontdict={'weight': 'extra bold'})
    count += 1            

pl.tight_layout()
pyplot.legend()
pyplot.grid(True)
yticks = pyplot.yticks()[0]
pyplot.yticks(yticks, [f'{20 * np.log10(ytick):.0f} dB' for ytick in yticks])
pl.tight_layout()
pyplot.savefig(f"out/bode/{csv_name}-{plot_name}.png",dpi=300)