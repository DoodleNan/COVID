import csv
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.models import DatetimeTickFormatter
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.palettes import Viridis6 as palette

# Read confirmed csv file
csvFile = open("case_confirmed_luxembourg.csv", "r")
reader = csv.reader(csvFile)

result_c = {}
for item in reader:
    if reader.line_num == 1:
        continue
    date_formed = datetime.datetime.strptime(item[0], '%Y%m%d')
    result_c[date_formed] = item[1]

csvFile.close()
# Read died csv file
csvFile = open("case_died_luxembourg.csv", "r")
reader = csv.reader(csvFile)

result_d = {}
for item in reader:
    if reader.line_num == 1:
        continue
    date_formed = datetime.datetime.strptime(item[0], '%Y%m%d')
    result_d[date_formed] = item[1]

csvFile.close()

# Read recovered csv file
csvFile = open("case_recovered_luxembourg.csv", "r")
reader = csv.reader(csvFile)

result_r = {}
for item in reader:
    if reader.line_num == 1:
        continue
    date_formed = datetime.datetime.strptime(item[0], '%Y%m%d')
    result_r[date_formed] = item[1]

csvFile.close()

# Build plot
# Date list
date_list = list(result_c.keys())
date_list_str = []
for i in date_list:
    date_list_str.append(str(i.date()))

# Confirmed case list
case_nb_c = list(result_c.values())

# Died case list
case_nb_d = list(result_d.values())

# Recovered Case
case_nb_r = list(result_r.values())

diff_c = ['1']
case_nb_a = [int(case_nb_c[0])-int(case_nb_d[0])-int(case_nb_r[0])]
for i in range(1, len(case_nb_c)):
    tmp = (int(case_nb_c[i]) - int(case_nb_c[i - 1]))
    tmp = str(case_nb_c[i]) + ' (' + str(tmp) + ' new)'
    diff_c.append(tmp)
    case_nb_a.append(int(case_nb_c[i])-int(case_nb_d[i])-int(case_nb_r[i]))

# bokeh
source = ColumnDataSource(
    data=dict(x=date_list, xs=date_list_str, yc=case_nb_c, dc=diff_c, yd=case_nb_d, yr=case_nb_r, ya=case_nb_a))

TOOLTIPS = [("Date", "@xs"), ("Confirmed", "@dc"), ("Recovered", "@yr"), ("Dead", "@yd"), ("Active", "@ya")]

# Plot
output_file('plot.html')
p = figure(plot_width=322, plot_height=355, y_range=(-1, (int(case_nb_c[-1]) + 100)),
           x_axis_type='datetime', tooltips=TOOLTIPS, title='COVID-19 Outbreak in Luxembourg')
p.xaxis.axis_label = "Date from the First Case in Luxembourg"
p.yaxis.axis_label = "Case Number"

# Died Case
p.cross('x', 'yd', line_width=2, legend_label='Dead',
        line_color='black', source=source)
p.line('x', 'yd', line_width=1, legend_label='Dead',
       line_color='black', source=source)

# Recovered Case
p.asterisk('x', 'yr', line_width=2, legend_label='Recovered',
           line_color='orange', source=source)
p.line('x', 'yr', line_width=1, legend_label='Recovered',
       line_color='orange', source=source)

# Confirmed Case
p.circle('x', 'yc', line_width=2, line_color='red',
         source=source, legend_label='Confirmed', fill_color='red')
p.line('x', 'yc', line_width=2, line_color='red',
       source=source, legend_label='Confirmed')

# Active Case
# p.asterisk('x', 'ya', line_width=2, line_color='purple',
#          source=source, legend_label='Active', fill_color='red')
# p.line('x', 'ya', line_width=2, line_color='purple',
#        source=source, legend_label='Active')

p.xgrid.visible = False
# p.ygrid.visible = False
p.legend.location = "top_left"
show(p)
