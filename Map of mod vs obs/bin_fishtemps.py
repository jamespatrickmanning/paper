# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 16:21:23 2020

@author: JiM  in April 2020 for Mingchao's Map_mod_vs_obs project
"""
import numpy as np
import pandas as pd
import datetime
from matplotlib import pyplot as plt
import os
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata

##### HARDCODES ###
mila=36.;mala=44.5;milo=-76.;malo=-66. # taken from "Map_mod_vs_obsscatter.py"
gbox=[milo,malo,mila,mala]
data_list = 'vessel_dfs_C.csv'
gridsize=.5 # units of lat/lon where .05 is about 3 miles
maxdiff_ignore=6 # max temp diff accepted (to remove outliers)
option='CLIMATOLOGY'
save_path = option+'_obs_binned_map.png'
start_time_str = '2019-01-01 00:00:00'
end_time_str = '2020-01-01 00:00:00'
start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime(end_time_str,'%Y-%m-%d %H:%M:%S')
time_period=str(start_time.year)
gs=50      # number of bins in the x and y direction so,  if you want more detail, make it bigger
ss=100     # subsample input data so, if you want more detail, make it smaller
cont=[-200] 
###################

def sh_bindata(x, y, z, xbins, ybins):
    """
    Bin irregularly spaced data on a rectangular grid.
    returns X,Y,Z lists
    """
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_median=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_std=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_num=np.zeros((len(xbins)-1,len(ybins)-1),dtype=int)    
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
            zb_median[iix-1,iiy-1]=np.median(z[k])
            zb_std[iix-1,iiy-1]=np.std(z[k])
            zb_num[iix-1,iiy-1]=len(z[k])
    X,Y = np.meshgrid(xb, yb)
    Z=zb_mean.T.flatten()           
    #return xb,yb,zb_mean,zb_median,zb_std,zb_num
    return X,Y,Z

def add_isobath(m,gs,ss,cont):
    # draws an isobath on map given gridsize,subsample rate,and contour level
    # these inputs are typically 50, 100, and 200 for entire shelf low resolution
    url='http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_794e_6df2_6381.csv?b_bathy[(0000-01-01T00:00:00Z):1:(0000-01-01T00:00:00Z)][(35.0):1:(45.0)][(-76.0):1:(-66.0)]'
    df=pd.read_csv(url)
    df=df.drop('time',axis=1)
    df=df[1:].astype('float')# removes unit row and make all float          
    Xb,Yb=m.makegrid(gs,gs) # where "gs" is the gridsize specified in hardcode section
    Xb,Yb=m(Xb,Yb) # converts grid to basemap coordinates .
    xlo,yla=m(df['longitude'][0:-1:ss].values,df['latitude'][0:-1:ss].values)
    zi = griddata((xlo,yla),df['b_bathy'][0:-1:ss].values,(Xb,Yb),method='linear')
    CS=m.contour(Xb,Yb,zi,cont,zorder=0,linewidths=[1],linestyles=['dashed'])
    plt.clabel(CS, inline=1, fontsize=8,fmt='%d')

def make_basemap(milo,malo,mila,mala):
    m = Basemap(projection='stere',lon_0=(milo+malo)/2,lat_0=(mila+mala)/2,lat_ts=0,llcrnrlat=mila,urcrnrlat=mala,\
                llcrnrlon=milo,urcrnrlon=malo,rsphere=6371200.,resolution='l',area_thresh=100)
    m.fillcontinents(color='grey',lake_color='grey')
    parallels = np.arange(mila,mala,3)
    m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
    meridians = np.arange(milo+2,malo,4)
    m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    return m

### MAIN PROGRAM #####
DF=pd.read_csv(data_list, index_col=0)    # reads input file with obs & models
DF=DF.loc[DF['difference']<maxdiff_ignore]# gets rid of outlyers
DF['time'] = pd.to_datetime(DF['time'])   # converts date time
DF.index=DF['time'] 
DF=DF.loc[DF['time']>start_time]
#DF=DF.loc[DF['time'].year==start_time.year]                      # makes time index
DF['month']=DF.index.month
season = ((DF.month % 12 + 3) // 3).map({1:'WINTER', 2: 'SPRING', 3:'SUMMER', 4:'FALL'})
DF['season']=season.values
id=np.where(DF.difference<maxdiff_ignore) #index of good data
print('making basemap')
fig, ax = plt.subplots()
m=make_basemap(milo, malo, mila, mala)
print('adding isobath')
add_isobath(m,gs,ss,cont)
print('binning data')
xi = np.arange(gbox[0],gbox[1],gridsize)# longitude grid
yi = np.arange(gbox[2],gbox[3],gridsize)# latitude grid
X,Y,Z = sh_bindata(DF['lon'].values[id], DF['lat'].values[id],DF['difference'].values[id],xi,yi)
X,Y = m(X.flatten(),Y.flatten())
print('finally adding scatter plot ')
a=m.scatter(X, Y, c=Z, cmap='coolwarm',marker='o', linewidths=0.01)
a.set_clim(-1*maxdiff_ignore,maxdiff_ignore) # forces colorbar to be consistent scale
print('add colorbar')
c3 = fig.colorbar(a, ax=ax)
c3.set_ticks(np.arange(-1*maxdiff_ignore,maxdiff_ignore))
c3.set_ticklabels(np.arange(-maxdiff_ignore,maxdiff_ignore))
fig.text(0.5, 0.93, time_period, ha='center', va='center', fontsize=14)
plt.suptitle('Observed bottom temperature minus '+option, va='center_baseline', fontsize=12)
plt.savefig(save_path)
plt.show()
