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

def draw_basemap(fig, ax, lonsize, latsize, interval_lon=2, interval_lat=2):
    ax = fig.sca(ax)
    dmap = Basemap(projection = 'cyl',
                   llcrnrlat = min(latsize)-0.01,
                   urcrnrlat = max(latsize)+0.01,
                   llcrnrlon = min(lonsize)-0.01,
                   urcrnrlon = max(lonsize)+0.01,
                   resolution = 'h',ax=ax)
    dmap.drawparallels(np.arange(int(min(latsize)),
                                 int(max(latsize))+1,interval_lat),
                       labels=[1,0,0,0], linewidth=0,fontsize=20)
    dmap.drawmeridians(np.arange(int(min(lonsize))-1,
                                 int(max(lonsize))+1,interval_lon),
                       labels=[0,0,0,1], linewidth=0,fontsize=20)
    dmap.drawcoastlines()
    #dmap.fillcontinents(color='grey')
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
for i in range(8):
    #j = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    j = [0,0,0,0,0,0,0,0,0,0,0]
    dataNum.append(j)
'''
fig = plt.figure()
ax = fig.add_subplot(111)
draw_basemap(fig, ax, lonsize, latsize)
plt.plot([lonA, lonB, lonC, lonD, lonA], [latA, latB, latC, latD, latA], 'b-')
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
x1_d = [lons[0][0], lons[0][-1], lons[-1][-1],\
        lons[-1][0], lons[0][0]]
y1_d = [lats[0][0], lats[0][-1], lats[-1][-1],\
        lats[-1][0], lats[0][0]]
m.plot(x1_d, y1_d, color='b', latlon=True)
for i in range(0, 242, 22):      # Here use num smller than 81 because the last grid is too small
    m.plot([lons[0][i], lons[-1][i]], [lats[0][i], lats[-1][i]], 'b--', latlon=True)
for i in range(0, 105, 15):
    m.plot([lons[i][0], lons[i][-1]], [lats[i][0], lats[i][-1]], 'b--', latlon=True)
'''
for i in range(0, 75, 10):      # Here use num smller than 81 because the last grid is too small
    plt.plot([lons[i][0], lons[i][129]], [lats[i][0], lats[i][129]], 'b--')
for i in range(0, 129, 10):
    plt.plot([lons[0][i], lons[81][i]], [lats[0][i], lats[81][i]], 'b--')
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
    dataNum[m][n] += 1

'''
m1, m2 = 32.23944076281737, 46.61132781935112
n1, n2 = -80.51869016711879, -59.69028308386868
for s in range(10):
    a = np.arange(n1, n2, 0.631)
    b = np.arange(m1, m2, 0.47)
    for i, j, k in zip(a, b, dataNum[s]):
        print(i, j, k)
        plt.text(i, j, str(k), color='r',multialignment='center', ha='center')
    m1 = m1 + 0.408
    m2 = m2 + 0.408
    n1 = n1 - 0.45
    n2 = n2 - 0.45
plt.title('Distribution of Data', fontsize=16)
'''