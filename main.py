import pandas as p
import math
from matplotlib.axis import Axis  
from matplotlib import pyplot
import matplotlib
import numpy as np
import glob

x_intercept = 7.81
tolerance = 1e-12

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

            pl, ax = pyplot.subplots()

            markers = []
            if (x_intercept is not None):
                poi = np.interp(x_intercept, list(data.iloc[:,0+i]),list(data.iloc[:,1+i]))
                print(f'POI: {poi}')
                for j, x in enumerate(list(data.iloc[:,1+i])):
                    if (equal_tolerance(x, poi, tolerance)):
                        print(round_to(poi, poi))
                        markers.append(j)
                        break
            
            pyplot.plot(data.iloc[:,0+i], data.iloc[:,1+i], color="#c3073f", markevery=markers, marker="o", markersize=12, markeredgecolor="#000000", linewidth=5)
            
            ax.yaxis.set_major_formatter(matplotlib.ticker.EngFormatter(unit=''))
            ax.xaxis.set_major_formatter(matplotlib.ticker.EngFormatter(unit=''))
            pyplot.xticks(rotation = 45, weight = 'semibold')
            pyplot.yticks(weight = 'semibold')

            pyplot.xlabel(f'{label_name_list[0+i].replace(";","")} ({label_unit_list[0+i].replace(";","")})', fontdict={'weight': 'extra bold'})
            pyplot.ylabel(f'{label_name_list[1+i]} ({label_unit_list[1+i]})', fontdict={'weight': 'extra bold'})
            plot_name = plot_name_list[i//2].replace(":","_").replace(";","").replace("/","!").replace('"',"'").replace('?',".")
            pl.suptitle(plot_name, fontdict={'weight': 'extra bold'})

            if (label_name_list[0+i].replace(";","") == "freq"):
                ax.set_xscale('log')
                

            for j, v in enumerate(data.iloc[:,1+i]):
                label = f'({format_si(j)},{format_si(v)})'
                if j in markers:
                    pyplot.annotate(label, (list(data.iloc[:,0+i])[j], list(data.iloc[:,1+i])[j]), xytext=(-10,15), textcoords="offset points")
                #ax.annotate(str(v), xy=(j,v), xytext=(0,0), textcoords='offset points')

            pl.tight_layout()
            pyplot.grid(True)
            pl.savefig(f"csv/img/{csv_name}-{plot_name}.png")
            pl.clear()