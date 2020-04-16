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
path = 'E:\\Mingchao\\paper\\vessel_dfs_D.csv'
url = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his'
save_path = 'E:\\Mingchao\\paper\\distribution_of_fishing.png'

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
    #j = [0,0,0,0,0,0,0,0,0,0]
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
#x_cut = pd.cut(data.lat, np.linspace(32, 47, 8), right=False)
#y_cut = pd.cut(data.lon, np.linspace(-80, -59, 12), right=False)
x_cut = pd.cut(data.lat, np.linspace(32.24, 46.612, 8), right=False)
y_cut = pd.cut(data.lon, np.linspace(-80.52, -59.7, 12), right=False)
# group and count
count_df = data.groupby([x_cut, y_cut]).count()
#drop null value only save the counting 
count_df = count_df['difference'].dropna()

#lat_i = [44.5, 44.5, 44.5, 42, 42, 42, 42, 39.5, 39.5, 34.5]
#lon_j = [-73, -70.667, -68.333, -75.333, -73, -70.667, -68.333, -75.333, -73, -75.333]
#dataNum_k = [64, 1069, 46, 67, 1345, 533, 288, 46, 120, 14]
'''
lat_list = [36.286, 36.286, 38.429, 38.429, 38.429, 38.429,\
            40.571, 40.571, 40.571, 40.571, 42.714, 42.714,\
            42.714]
lon_list = [-76.182, -74.273, -74.273, -72.364, -70.455, -68.545,\
            -74.273, -72.364, -70.455, -68.545, -72.364, -70.455,\
            -68.545]
dataNum_list = [17, 28, 305, 205, 7, 33, 30,\
                1094, 583, 476, 568, 245, 1]

lat_list = [36.346, 38.399, 38.399, 38.399, 38.399, 40.453,\
            40.453, 40.453, 40.453, 40.453, 42.506, 42.506
           ]
lon_list = [-74.842, -74.842, -72.949, -71.056, -69.164, -74.842,\
            -72.949, -71.056, -69.164, -67.271, -71.056, -69.164
           ]
dataNum_list = [51, 34, 436, 23, 9, 54, 1214,\
                537, 550, 33, 980, 16]
def judge_index(lat, lon):
#get the index of x and y
    lat_index = [32.24, 34.293, 36.346, 38.399, 40.453, 42.506, 44.559]
    lon_index = [-80.52, -78.627, -76.735, -74.842, -72.949, -71.056,\
                 -69.164, -67.271, -65.378, -63.485, -61.593]
    for i in lat_index:
        if lat == i:
            m = lat_index.index(i)
    for j in lon_index:
        if lon == j:
            n = lon_index.index(j)
    return m, n 

for i in range(len(lat_list)):
    m, n = judge_index(lat_list[i], lon_list[i])
    dataNum[m][n] = dataNum_list[i]
for i in range(len(lat_list)):
     plt.text(lon_list[i]-1, lat_list[i]-1, dataNum_list[i], color='r',multialignment='center', ha='center')
'''
dataNum[2][5] = 9
dataNum[3][2] = 51
dataNum[3][4] = 23
dataNum[3][7] = 33
dataNum[4][3] = 436
dataNum[4][6] = 550
dataNum[5][3] = 34
dataNum[5][4] = 1214
dataNum[5][5] = 537
dataNum[5][7] = 16
dataNum[6][4] = 54
dataNum[6][6] = 980
'''
#x, y = m(lon_j, lat_i)
#for i in range(len(lon_j)):
#    plt.text(lon_j[i], lat_i[i], dataNum_k[i], color='r')
#plt.title('Distribution of Data', fontsize=16)

#dataNum.reverse()
#m1, m2 = 37.20694434507049, 46.61132781935112
#n1, n2 = -80.51869016711879, -75.19030604271552
'''
m1, m2 = 32.24, 41.08
n1, n2 = -75.19, -59.69
for s in range(7):
    #a = np.arange(n1, n2,  1.409)
    #b = np.arange(m1, m2, 0.9)
    a = np.arange(n1, n2,  1.435)
    b = np.arange(m1, m2, 0.867)
    for i, j, k in zip(a, b, dataNum[s]):
        #print(i, j, k)
        if k>0:
            plt.text(i, j, k, color='r',multialignment='center', ha='center', rotation=30)
    #m1 = m1 + 0.73
    m1 = m1 + 0.76
    m2 = m2 + 0.76
    n1 = n1 - 0.7
    n2 = n2 - 0.7
plt.title('Distribution of Fishing DATA',  fontsize=2.5*size, va='center_baseline')
plt.savefig(save_path)
plt.show()