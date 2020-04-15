# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 09:31:54 2020

@author: Mingchao
"""

import netCDF4
import datetime
import os
import pandas as pd
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

#Hardcodes
path = 'E:\\Mingchao\\paper\\vessel_dfs_C.csv'
url = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his'
save_path = 'E:\\Mingchao\\paper\\distribution_of_fishing.png'

def draw_basemap(fig, ax, lonsize, latsize, interval_lon=4, interval_lat=4):
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
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1] ,linewidth=0,)
    dmap.drawcoastlines(color='grey')
    dmap.fillcontinents(color='grey')
    dmap.drawmapboundary()

def whichArea(arg, lst):
    #Calculate certain point belongs to which area.
    i = len(lst)//2
    if i != 0: 
        if arg >= lst[i]:
            r = i + whichArea(arg, lst[i:])
        elif arg < lst[i]:
            r = whichArea(arg, lst[:i])
    else: 
        r = i
    return r    

def get_doppio_url(date):
    url='http://tds.marine.rutgers.edu/thredds/dodsC/roms/doppio/2017_da/his/runs/History_RUN_2018-11-12T00:00:00Z'
    return url.replace('2018-11-12',date)

#main
data = pd.read_csv(path, index_col=0)
'''
data_nc = netCDF4.Dataset(url)
lons, lats = data_nc.variables['lon_rho'], data_nc.variables['lat_rho']
lonA, latA = lons[81][0], lats[81][0] # Vertex of ROMS area.
lonB, latB = lons[81][129], lats[81][129]
lonC, latC = lons[0][129], lats[0][129]
lonD, latD = lons[0][0], lats[0][0]
'''
date_str = '2020-03-05'#input date to url of models'code to get url
date_time = datetime.datetime.strptime(date_str+' 00:00:00', '%Y-%m-%d %H:%M:%S')
url_doppio = get_doppio_url(date_str)
nc_doppio = netCDF4.Dataset(str(url_doppio))
lons = nc_doppio.variables['lon_rho'][:]
lats = nc_doppio.variables['lat_rho'][:]
lonsize = [np.amin(lons), np.amax(lons)]
latsize = [np.amin(lats), np.amax(lats)]
dataNum = []
#for i in range(9):
for i in range(7):
    j = [0,0,0,0,0,0,0,0,0,0,0]
    #j = [0,0,0,0,0,0,0,0,0]
    dataNum.append(j)

fig = plt.figure(figsize=(9,9))
size=min(fig.get_size_inches())
ax = fig.add_subplot(111)

draw_basemap(fig, ax, lonsize, latsize)
#plt.plot([lonA, lonB, lonC, lonD, lonA], [latA, latB, latC, latD, latA], 'b-')
'''
m = Basemap(projection='stere',lon_0=(-80-60)/2,lat_0=(38+46)/2,lat_ts=0,llcrnrlat=31., urcrnrlat=46.,\
            llcrnrlon=-80.,urcrnrlon=-58.,rsphere=6371200.,resolution='f',area_thresh=100)
# draw coastlines
m.drawcoastlines()
 # draw parallels.
parallels = np.arange(31,46,5)
m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
# draw meridians
meridians = np.arange(-77,-58,8)
m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
'''
x1_d = [lons[0][0], lons[0][-1], lons[-1][-1],\
        lons[-1][0], lons[0][0]]
y1_d = [lats[0][0], lats[0][-1], lats[-1][-1],\
        lats[-1][0], lats[0][0]]
plt.plot(x1_d, y1_d, color='b')
'''
#for i in range(0, 242, 22):      # Here use num smller than 81 because the last grid is too small
for i in range(0, 242, 28):
    m.plot([lons[0][i], lons[-1][i]], [lats[0][i], lats[-1][i]], 'b--', latlon=True)
#for i in range(0, 105, 15):
for i in range(0, 105, 19):
    m.plot([lons[i][0], lons[i][-1]], [lats[i][0], lats[i][-1]], 'b--', latlon=True)
'''
#for i in range(0, 242, 28):
for i in range(0, 242, 22):
    plt.plot([lons[0][i], lons[-1][i]], [lats[0][i], lats[-1][i]], 'b--')
#for i in range(0, 105, 19):
for i in range(0, 105, 15):
    plt.plot([lons[i][0], lons[i][-1]], [lats[i][0], lats[i][-1]], 'b--')
'''
r1 = range(0, 105, 15)
r2 = range(0, 242, 22)
nearestIndex = []
indx = np.where(abs(data['difference']) < 6)[0]
for i in indx:
    nearestIndex.append((data['lat'][i],data['lon'][i]))  

for i in nearestIndex:
    m = whichArea(i[0], r1)
    n = whichArea(i[1], r2)
    errorNum[m][n] += 1
'''
x_cut = pd.cut(data.lat, np.linspace(32, 47, 8), right=False)
y_cut = pd.cut(data.lon, np.linspace(-80, -59, 12), right=False)
# group and count
count_df = data.groupby([x_cut, y_cut]).count()
#drop null value only save the counting 
count_df = count_df['difference'].dropna()

#lat_i = [44.5, 44.5, 44.5, 42, 42, 42, 42, 39.5, 39.5, 34.5]
#lon_j = [-73, -70.667, -68.333, -75.333, -73, -70.667, -68.333, -75.333, -73, -75.333]
#dataNum_k = [64, 1069, 46, 67, 1345, 533, 288, 46, 120, 14]

dataNum[2][2] = 17
dataNum[2][3] = 28
dataNum[3][3] = 305
dataNum[3][4] = 205
dataNum[3][5] = 7
dataNum[3][6] = 33
dataNum[4][3] = 30
dataNum[4][4] = 1094
dataNum[4][5] = 583
dataNum[4][6] = 476
dataNum[5][4] = 568
dataNum[5][5] = 245
dataNum[5][6] = 1
#x, y = m(lon_j, lat_i)
#for i in range(len(lon_j)):
#    plt.text(lon_j[i], lat_i[i], dataNum_k[i], color='r')
#plt.title('Distribution of Data', fontsize=16)

#dataNum.reverse()
#m1, m2 = 37.20694434507049, 46.61132781935112
#n1, n2 = -80.51869016711879, -75.19030604271552
m1, m2 = 32.24, 41.08
n1, n2 = -75.19, -59.69
for s in range(7):
    #a = np.arange(n1, n2, 1.597)
    a = np.arange(n1, n2,  1.409)
    #b = np.arange(m1, m2, 1.044931497142292)
    #b = np.arange(m1, m2, 0.8036)
    b = np.arange(m1, m2, 0.9)
    for i, j, k in zip(a, b, dataNum[s]):
        #print(i, j, k)
        if k>0:
            plt.text(i, j, k, color='r',multialignment='center', ha='center', rotation=30)
    m1 = m1 + 0.73
    m2 = m2 + 0.73
    n1 = n1 - 0.7
    n2 = n2 - 0.7
plt.title('Distribution of Fishing DATA',  fontsize=2.5*size, va='center_baseline')
plt.savefig(save_path)
plt.show()