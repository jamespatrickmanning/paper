# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 14:32:45 2020

Plot distribution of emolt_QCed.csv from 2015-06-13 to now.
If you need,you can add start time and end time on the area of filter data,get the time range you want.

@author: Mingchao
"""

import netCDF4
import datetime
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib import path

#Hardcodes
emolt_path = 'https://www.nefsc.noaa.gov/drifter/emolt_QCed.csv'
url = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his'
save_path = 'E:\\Mingchao\\paper\\emolt_binning.png'

def draw_basemap(fig, ax, lonsize, latsize, interval_lon=3, interval_lat=3):
    ax = fig.sca(ax)
    dmap = Basemap(projection = 'cyl',
                   llcrnrlat = min(latsize)-0.01,
                   urcrnrlat = max(latsize)+0.01,
                   llcrnrlon = min(lonsize)-0.01,
                   urcrnrlon = max(lonsize)+0.01,
                   resolution = 'h',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0] ,linewidth=0,)
                       #labels=[1,0,0,0])
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1] ,linewidth=0,)
                       #labels=[0,0,0,1])
    dmap.drawcoastlines(color='grey')
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()

def get_doppio_url(date):
    url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/doppio/2017_da/his/runs/History_RUN_2018-11-12T00:00:00Z'
    return url.replace('2018-11-12',date)

#####
# HARDOCDES
date_str = '2020-03-05'#input date to url of models'code to get url
######

#main
data = pd.read_csv(emolt_path, index_col=0)#get data from emolt_QCed.csv
for i in range(len(data)):
    if not 30<data['lat'][i]<50  or data['flag'][i]~=0:#filter the data are not well
        data = data.drop(i)
data.index = range(len(data))
#data = data[0:500]
date_time = datetime.datetime.strptime(date_str+' 00:00:00', '%Y-%m-%d %H:%M:%S')
url_doppio = get_doppio_url(date_str)
nc_doppio = netCDF4.Dataset(str(url_doppio))
lons = nc_doppio.variables['lon_rho'][:]
lats = nc_doppio.variables['lat_rho'][:]
lonsize = [np.amin(lons), np.amax(lons)]
latsize = [np.amin(lats), np.amax(lats)]
dataNum = []#create a list for storing distrubution of number
for i in range(7):
    j = [0,0,0,0,0,0,0,0,0,0,0]
    dataNum.append(j)

fig = plt.figure(figsize=(9,9))
size = min(fig.get_size_inches())
ax = fig.add_subplot(111)
draw_basemap(fig, ax, lonsize, latsize)
#plot boundary of Doppio
x1_d = [lons[0][0], lons[0][-1], lons[-1][-1],\
        lons[-1][0], lons[0][0]]
y1_d = [lats[0][0], lats[0][-1], lats[-1][-1],\
        lats[-1][0], lats[0][0]]
plt.plot(x1_d, y1_d, color='b')

#plot grid in figure
for i in range(0, 242, 22): # need to explain this "242, 22"
    plt.plot([lons[0][i], lons[-1][i]], [lats[0][i], lats[-1][i]], 'b--')
for i in range(0, 105, 15):
    plt.plot([lons[i][0], lons[i][-1]], [lats[i][0], lats[i][-1]], 'b--')

#loop data and append distribution of number into list
# at some point, if we get back to this program, we will need to explain how these numbers were obtained
# what if we someday want to make smaller grid cells?
for j in range(len(data)):
   for i in range(0,11):
       #list_00 is the box of left bottom,it is 0 row 0 column
       list_00 = [(32.23944076+i*0.81119, -75.19030604+i*1.40909), (33.04333746+i*0.81119, -73.78121304+i*1.40909),\
                  (33.7602733+i*0.81119, -74.53623985+i*1.40909), (32.94908413+i*0.81119, -75.95150377+i*1.40909)]
       p1 = path.Path([list_00[0], list_00[1], list_00[2], list_00[3]])
       if p1.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           #if p1.contains_points([ii,jj])[0] == False:
           dataNum[0][i] += 1
       #list_10 is 1 row 0 column
       list_10 = [(32.94908413+i*0.81119, -75.95150377+i*1.40909), (33.7602733+i*0.81119, -74.53623985+i*1.40909),\
                  (34.47720913+i*0.81119, -75.29126667+i*1.40909), (33.6587275+i*0.81119, -76.71270151+i*1.40909)]               
       p2 = path.Path([list_10[0], list_10[1], list_10[2], list_10[3]])
       if p2.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[1][i] += 1
       list_20 = [(33.6587275+i*0.81119, -76.71270151+i*1.40909), (34.47720913+i*0.81119, -75.29126667+i*1.40909),\
                  (35.19414496+i*0.81119, -76.04629348+i*1.40909), (34.36837087+i*0.81119, -77.47389924+i*1.40909)]
       p3 = path.Path([list_20[0], list_20[1], list_20[2], list_20[3]])
       if p3.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[2][i] += 1
       list_30 = [(34.36837087+i*0.81119, -77.47389924+i*1.40909), (35.19414496+i*0.81119, -76.04629348+i*1.40909),\
                  (35.9110808+i*0.81119, -76.8013203+i*1.40909), (35.07801424+i*0.81119, -78.23509697+i*1.40909)]
       p4 = path.Path([list_30[0], list_30[1], list_30[2], list_30[3]])
       if p4.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[3][i] += 1
       list_40 = [(35.07801424+i*0.81119, -78.23509697+i*1.40909), (35.9110808+i*0.81119, -76.8013203+i*1.40909),\
                  (36.62801663+i*0.81119, -77.55634711+i*1.40909), (35.78765761+i*0.81119, -78.9962947+i*1.40909)]
       p5 = path.Path([list_40[0], list_40[1], list_40[2], list_40[3]])
       if p5.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[4][i] += 1
       list_50 = [(35.78765761+i*0.81119, -78.9962947+i*1.40909), (36.62801663+i*0.81119, -77.55634711+i*1.40909),\
                  (37.34495247+i*0.81119, -78.31137393+i*1.40909), (36.49730098+i*0.81119, -79.75749244+i*1.40909)]
       p6 = path.Path([list_50[0], list_50[1], list_50[2], list_50[3]])
       if p6.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[5][i] += 1
       list_60 = [(36.49730098+i*0.81119, -79.75749244+i*1.40909), (37.34495247+i*0.81119, -78.31137393+i*1.40909),\
                  (38.0618883+i*0.81119, -79.06640074+i*1.40909), (37.20694435+i*0.81119 ,-80.51869017+i*1.40909)]
       p7 = path.Path([list_60[0], list_60[1], list_60[2], list_60[3]])
       if p7.contains_points([(data['lat'][j],data['lon'][j])])[0] != False:
           dataNum[6][i] += 1
#loop every number of distribution in list,match the box in grid
m1, m2 = 32.24, 41.08#(m1,n1) and (m2,n2) are coordinates of grid of left bottom and right bottom
n1, n2 = -75.19, -59.69
for s in range(7):
    a = np.arange(n1, n2,  1.435)#a,b is the position for showing in figure
    b = np.arange(m1, m2, 0.867)
    for i, j, k in zip(a, b, dataNum[s]):
        if k>0:#only display the  distribution had fishing
            plt.text(i, j, k, color='r',multialignment='center', ha='center', rotation=30)
    #m1 = m1 + 0.73
    m1 = m1 + 0.76#adjust the space for more better
    m2 = m2 + 0.76
    n1 = n1 - 0.7
    n2 = n2 - 0.7
plt.title('Distribution of Fishing DATA',  fontsize=2.5*size, va='center_baseline')
plt.savefig(save_path)
plt.show()
