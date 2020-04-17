# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:18:54 2020

Draw map of observation'stemperature minus models'temperature.
    (This code still needs a lot of simplifying.Because it didn't loop models,so you need to change the models'file,
    such as DF_C,DF_D,DF_F,DF_G ; save_path and subtitle.

@author: Mingchao
Modifications by JiM in Mid-April 2020 - minor suggestions and documentation
- assumes input and output files are in the same directory as the code
- ignores values greater than a user-specified "maxdiff_ignore"
- had to add a pointer to the "PROJ" package after installing basemap
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
from scipy.interpolate import griddata

#Hardcodes
# the following line points to where the proj4 is located on JiM's Toshiba laptop
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
maxdiff_ignore=6 # ignore when difference is greater than this number
time_period='July 2018 through December 2019' # time period of data
data_list = ['vessel_dfs_C.csv', 'vessel_dfs_D.csv',\
             'vessel_dfs_F.csv', 'vessel_dfs_G.csv'
             ]
which=2 # 0-3 depending on which of the datalist you want    
options=['CLIMATOLOGY','DOPPIO','FVCOM','GOMOFS']
option=options[which]    
save_path = option+'_obs_map.png'
start_time_str = '2018-07-01 00:00:00'
end_time_str = '2019-12-18 00:00:00'
start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime(end_time_str,'%Y-%m-%d %H:%M:%S')
bathy=False
gs=10      # number of bins in the x and y direction so,  if you want more detail, make it bigger
ss=500     # subsample input data so, if you want more detail, make it smaller
cont=[-70]    # contour level
mila=35.;mala=45.;milo=-76.;malo=-66.#min & max lat and lo
#########  END HARDCODES ######################

def draw_basemap(fig, ax, df_lon, df_lat, list_season, seasons,bathy,gs,ss,milo,malo,mila,mala,cont):
    # if bathy=True, plot bathy
    ax = fig.sca(ax)
    m = Basemap(projection='stere',lon_0=(milo+malo)/2,lat_0=(mila+mala)/2,lat_ts=0,llcrnrlat=mila,urcrnrlat=mala,\
                llcrnrlon=milo,urcrnrlon=malo,rsphere=6371200.,resolution='l',area_thresh=100)
    # draw coastlines
    m.drawcoastlines()
    # draw parallels.
    if ax == ax3:
        parallels = np.arange(mila,mala,4)
        m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
    # draw meridians
        meridians = np.arange(milo,malo,4)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    elif ax == ax4:
        meridians = np.arange(milo,malo,4)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    m.scatter(df_lon, df_lat, c=list_season, cmap='coolwarm',\
              marker='o', linewidths=0.01, latlon=True)
    if bathy==True: # get some detail bathymetry from USGS
      url='https://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeCrm1.csv?topo[('+str(mala)+'):100:('+str(mila)+')][('+str(milo)+'):100:('+str(malo)+')]'
      df=pd.read_csv(url)
      df=df[1:].astype('float')# removes unit row and make all float          
      #X,Y=np.meshgrid(np.linspace(min(df['longitude']),max(df['longitude']),25),np.linspace(min(df['latitude']),max(df['latitude']),25))
      print('making a grid field based on this basemap ...')   
      X,Y=m.makegrid(gs,gs) # where "gs" is the gridsize specified in hardcode section
      X,Y=m(X,Y)
      print('converting data to basemap coordinates ...')
      xlo,yla=m(df['longitude'][0:-1:ss].values,df['latitude'][0:-1:ss].values)
      print('gridding bathymetry ...')
      zi = griddata((xlo,yla),df['topo'][0:-1:ss].values,(X,Y),method='linear')
      print('contouring bathymetry ...')
      m.contour(X,Y,zi,cont,zorder=4)
      #  plt.contourf(X,Y,basemap_topo[min_index_lat:max_index_lat:ss,min_index_lon:max_index_lon:ss],[-100,-50,-20,0])#color='red')
    plt.title(seasons)

#main
DF_C = pd.read_csv(data_list[1], index_col=0)
#DF_D = pd.read_csv(data_list[1], index_col=0)
#DF_F = pd.read_csv(data_list[2], index_col=0)
#DF_G = pd.read_csv(data_list[3], index_col=0)
# here's the section that ignores wild outliers
for i in range(len(DF_C['difference'])):
    if abs(DF_C['difference'][i]) < maxdiff_ignore:
        continue
    else:
        DF_C = DF_C.drop(i)
DF_C.index = range(len(DF_C))
DF_C['time'] = pd.to_datetime(DF_C['time'])
seasons = ['SPRING', 'SUMMER', 'FALL', 'WINTER']
spring_list = []
summer_list = []
fall_list = []
winter_list = []
spring_df = pd.DataFrame(data=None,\
                         columns=['time','lat','lon','observation_T','Doppio_T','GoMOLFs_T','FVCOM_T','Clim_T','difference'])
summer_df = spring_df
fall_df = spring_df
winter_df = spring_df
for i in range(len(DF_C['time'])):
    if 3<=DF_C['time'][i].month<=5:
        spring_list.append(DF_C['difference'][i])
        spring_df = spring_df.append(DF_C.iloc[i], ignore_index=True)
    elif 6<=DF_C['time'][i].month<=8:
        summer_list.append(DF_C['difference'][i])
        summer_df = summer_df.append(DF_C.iloc[i], ignore_index=True)
    elif 9<=DF_C['time'][i].month<=11:
        fall_list.append(DF_C['difference'][i])
        fall_df = fall_df.append(DF_C.iloc[i], ignore_index=True)
    elif 11<DF_C['time'][i].month<=12 or 1<=DF_C['time'][i].month<=2:
        winter_list.append(DF_C['difference'][i])
        winter_df = winter_df.append(DF_C.iloc[i], ignore_index=True)
spring_df.index = range(len(spring_df))
summer_df.index = range(len(summer_df))
fall_df.index = range(len(fall_df))
winter_df.index = range(len(winter_df))
fig = plt.figure(figsize=(7,7))
size=min(fig.get_size_inches())
lon_list = [spring_df['lon'].values, summer_df['lon'].values,\
            fall_df['lon'].values, winter_df['lon'].values]
lat_list = [spring_df['lat'].values, summer_df['lat'].values,\
            fall_df['lat'].values, winter_df['lat'].values]
list_season = [spring_list, summer_list, fall_list, winter_list]
ax1 = fig.add_subplot(221)
m = Basemap(projection='stere',lon_0=(milo+malo)/2,lat_0=(mila+mala)/2,lat_ts=0,llcrnrlat=mila,urcrnrlat=mala,\
             llcrnrlon=milo,urcrnrlon=malo,rsphere=6371200.,resolution='l',area_thresh=100)
m.drawcoastlines()
if bathy==True:
    url='https://coastwatch.pfeg.noaa.gov/erddap/griddap/usgsCeCrm1.csv?topo[('+str(mala)+'):100:('+str(mila)+')][('+str(milo)+'):100:('+str(malo)+')]'
    df=pd.read_csv(url)
    df=df[1:].astype('float')# removes unit row and make all float          
    X,Y=m.makegrid(gs,gs) # where "gs" is the gridsize specified in hardcode section
    X,Y=m(X,Y)
    xlo,yla=m(df['longitude'][0:-1:ss].values,df['latitude'][0:-1:ss].values)
    zi = griddata((xlo,yla),df['topo'][0:-1:ss].values,(X,Y),method='linear')
    m.contour(X,Y,zi,cont,zorder=4)# draw parallels.
parallels = np.arange(36,45,4)
m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
#close draw meridians for not showing xaxis
#meridians = np.arange(-75,-66,4)
#m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
a = m.scatter(lon_list[0], lat_list[0], c=list_season[0], cmap='coolwarm',\
              marker='o', linewidths=0.01, latlon=True)
#ax1.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)
#plt.xticks([])
ax1.set_title(seasons[0])
ax2 = fig.add_subplot(222)
#ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
#ax4.axes.get_yaxis().set_visible(False)
ax_list = [ax1, ax2, ax3, ax4]
for i in range(1,4):# this runs the other three panels
    draw_basemap(fig, ax=ax_list[i], df_lon=lon_list[i], df_lat=lat_list[i],\
      list_season=list_season[i], seasons=seasons[i],bathy=False,gs=gs,ss=ss,milo=milo,malo=malo,mila=mila,mala=mala,cont=cont)
c3 = fig.colorbar(a, ax=[ax1, ax2, ax3, ax4])
c3.set_ticks(np.arange(-1*maxdiff_ignore,maxdiff_ignore))
c3.set_ticklabels(np.arange(-maxdiff_ignore,maxdiff_ignore))
fig.text(0.45, 0.93, time_period, ha='center', va='center', fontsize=2.0*size)
#plt.title(time_period)
plt.suptitle('FISHING VESSEL TEMPS  minus '+option, va='center_baseline', fontsize=2.5*size)
plt.savefig(save_path)
plt.show()
