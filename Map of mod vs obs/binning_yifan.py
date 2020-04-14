# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 13:23:41 2020

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 16:00:47 2020

@author: Administrator
"""

'''
Divide the whole area into drifferent girds, and plot the number of observation
and error in each grid.
'''
import netCDF4
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
import pandas as pd
from turtleModule import str2ndlist, np_datetime, draw_basemap,whichArea
###########################MAIN CODE###############################################
criteria = 2                # criteria for error
url = 'http://tds.marine.rutgers.edu/thredds/dodsC/roms/espresso/2009_da/his'#'http://tds.marine.rutgers.edu:8080/thredds/dodsC/roms/espresso/hidden/2006_da/his?lon_rho[0:1:81][0:1:129],lat_rho[0:1:81][0:1:129],u[0:1:69911][0:1:35][0:1:81][0:1:128],v[0:1:69911][0:1:35][0:1:80][0:1:129]'
data = netCDF4.Dataset(url)
lons, lats = data.variables['lon_rho'], data.variables['lat_rho']

lonA, latA = lons[81][0], lats[81][0] # Vertex of ROMS area.
lonB, latB = lons[81][129], lats[81][129]
lonC, latC = lons[0][129], lats[0][129]
lonD, latD = lons[0][0], lats[0][0]

obsData = pd.read_csv('ctdWithModTempByDepth.csv')
tf_index = np.where(obsData['TF'].notnull())[0]
modNearestIndex = pd.Series(str2ndlist(obsData['modNearestIndex'][tf_index], bracket=True), index=tf_index) # if str has '[' and ']', bracket should be True
modTemp = pd.Series(str2ndlist(obsData['modTempByDepth'][tf_index],bracket=True), index=tf_index)
obsLon, obsLat = obsData['LON'][tf_index], obsData['LAT'][tf_index]
obsTime = pd.Series(np_datetime(obsData['END_DATE'][tf_index]), index=tf_index)
obsTemp = pd.Series(str2ndlist(obsData['TEMP_VALS'][tf_index]), index=tf_index)
obsDepth = pd.Series(str2ndlist(obsData['TEMP_DBAR'][tf_index]), index=tf_index)
modLayer = pd.Series(str2ndlist(obsData['modDepthLayer'][tf_index], bracket=True), index=tf_index)
data = pd.DataFrame({'lon': obsLon, 'lat': obsLat,
                     'obstemp': obsTemp.values,'modtemp':modTemp,
                     'time': obsTime.values, 'nearestIndex': modNearestIndex.values,
                     'depth':obsDepth,'layer':modLayer},index=tf_index)

lonsize = [np.amin(lons), np.amax(lons)]
latsize = [np.amin(lats), np.amax(lats)]
errorNum = []
for i in range(9):     # just create a list with all zero to calculate error number 
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    errorNum.append(j)
fig = plt.figure()
ax = fig.add_subplot(111)
draw_basemap(fig, ax, lonsize, latsize)
plt.plot([lonA, lonB, lonC, lonD, lonA], [latA, latB, latC, latD, latA], 'b-')
for i in range(0, 75, 10):      # Here use num smller than 81 because the last grid is too small
    plt.plot([lons[i][0], lons[i][129]], [lats[i][0], lats[i][129]], 'b--')
for i in range(0, 129, 10):
    plt.plot([lons[0][i], lons[81][i]], [lats[0][i], lats[81][i]], 'b--')   # plot the box
r1 = range(0, 81, 10)
r2 = range(0, 129, 10)
nearestIndex = []
'''
for i in data.index:
    diff = np.array(data['obstemp'][i]) - np.array(data['modtemp'][i])
    indx = np.where(abs(diff)>criteria)[0]
    if not indx.size: continue
    nearestIndex.extend([modNearestIndex[i]] * indx.size)  # calculate all error data
'''
for i in data.index:
    if data['layer'][i][0]-data['layer'][i][-1]!=0:
        d_each=(data['depth'][i][-1]-data['depth'][i][0]) *1.0/(data['layer'][i][0]-data['layer'][i][-1])   
        if 36*d_each-data['depth'][i][-1]<10:
            diff = np.array(data['obstemp'][i][-1]) - np.array(data['modtemp'][i][-1])
            indx = np.where(abs(diff)>criteria)[0]
            if not indx.size: continue
            nearestIndex.extend([modNearestIndex[i]] * indx.size)       #calculate error data in bottom
for i in nearestIndex:
    m = whichArea(i[0], r1)
    n = whichArea(i[1], r2)
    errorNum[m][n] += 1
m1, m2 = 34.05, 39.84           # m1, m2 are the location to put Text.
n1, n2 = -75.83, -67.72         # n1, n2 are the location to put Text.
for s in range(8):
# a = np.arange(-75.83, -67.72, 0.631)
# b = np.arange(34.05, 39.84, 0.47)
    a = np.arange(n1, n2, 0.631)
    b = np.arange(m1, m2, 0.47)
    for i, j, k in zip(a, b, errorNum[s]):
        if k>0:
            print(i, j, k)
            plt.text(i, j, str(round(k,1)), color='r',multialignment='center')
    m1 = m1 + 0.408
    m2 = m2 + 0.408
    n1 = n1 - 0.45
    n2 = n2 - 0.45
plt.title('Distribution of Error,criteria='+str(criteria), fontsize=16)
#plt.savefig('gridOfError1.png')
##########################Plot whole data distribution##########################
dataNum = []
for i in range(9):
    j = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    dataNum.append(j)
fig = plt.figure()
ax = fig.add_subplot(111)
draw_basemap(fig, ax, lonsize, latsize)
plt.plot([lonA, lonB, lonC, lonD, lonA], [latA, latB, latC, latD, latA], 'b-')
for i in range(0, 75, 10):      # Here use num smller than 81 because the last grid is too small
    plt.plot([lons[i][0], lons[i][129]], [lats[i][0], lats[i][129]], 'b--')
for i in range(0, 129, 10):
    plt.plot([lons[0][i], lons[81][i]], [lats[0][i], lats[81][i]], 'b--')
r1 = range(0, 81, 10)
r2 = range(0, 129, 10)
nearestIndex = []
'''
for i in data.index:
    m = len(data['obstemp'][i])
    nearestIndex.extend([modNearestIndex[i]] * m)  # calculate all data 
'''
for i in data.index:
    if data['layer'][i][0]-data['layer'][i][-1]!=0:
        d_each=(data['depth'][i][-1]-data['depth'][i][0]) *1.0/(data['layer'][i][0]-data['layer'][i][-1])   
        if 36*d_each-data['depth'][i][-1]<10:
            m = len([data['obstemp'][i][-1]])
            nearestIndex.extend([modNearestIndex[i]] * m)   #calculate all data in bottom
for i in nearestIndex:
    m = whichArea(i[0], r1)
    n = whichArea(i[1], r2)
    dataNum[m][n] += 1
m1, m2 = 34.05, 39.84
n1, n2 = -75.83, -67.72
for s in range(8):
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