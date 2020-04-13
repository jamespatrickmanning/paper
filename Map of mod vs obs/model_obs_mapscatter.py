# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:18:54 2020

Draw map of observation'stemperature minus models'temperature.
    (This code still needs a lot of simplifying.Because it didn't loop models,so you need to change the models'file,
    such as DF_C,DF_D,DF_F,DF_G ; save_path and subtitle.

@author: Mingchao
"""

import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import datetime

#Hardcodes
path = 'E:\\Mingchao\\paper\\'
data_list = ['vessel_dfs_C.csv', 'vessel_dfs_D.csv',\
             'vessel_dfs_F.csv', 'vessel_dfs_G.csv'
             ]
save_path = 'E:\\Mingchao\\paper\\gomofs_obs_map.png'
start_time_str = '2018-07-01 00:00:00'
end_time_str = '2019-12-18 00:00:00'
start_time = datetime.datetime.strptime(start_time_str,'%Y-%m-%d %H:%M:%S')
end_time = datetime.datetime.strptime(end_time_str,'%Y-%m-%d %H:%M:%S')

def draw_basemap(fig, ax, df_lon, df_lat, list_season, seasons):
    ax = fig.sca(ax)
    m = Basemap(projection='stere',lon_0=(-75-66)/2,lat_0=(36+45)/2,lat_ts=0,llcrnrlat=36.,urcrnrlat=45.,\
                llcrnrlon=-76.,urcrnrlon=-66.,rsphere=6371200.,resolution='f',area_thresh=100)
    # draw coastlines
    m.drawcoastlines()
    # draw parallels.
    if ax == ax3:
        parallels = np.arange(36,45,4)
        m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
    # draw meridians
        meridians = np.arange(-75,-66,4)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    elif ax == ax4:
        meridians = np.arange(-75,-66,4)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    m.scatter(df_lon, df_lat, c=list_season, cmap='coolwarm',\
              marker='o', linewidths=0.01, latlon=True)
    plt.title(seasons)

#main
DF_C = pd.read_csv(path+data_list[0], index_col=0)
DF_D = pd.read_csv(path+data_list[1], index_col=0)
DF_F = pd.read_csv(path+data_list[2], index_col=0)
DF_G = pd.read_csv(path+data_list[3], index_col=0)
for i in range(len(DF_C['difference'])):
    if abs(DF_C['difference'][i]) < 6:
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
m = Basemap(projection='stere',lon_0=(-75-66)/2,lat_0=(36+45)/2,lat_ts=0,llcrnrlat=36.,urcrnrlat=45.,\
             llcrnrlon=-76.,urcrnrlon=-66.,rsphere=6371200.,resolution='f',area_thresh=100)
    # draw coastlines
m.drawcoastlines()
    # draw parallels.
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
for i in range(1,4):
    draw_basemap(fig, ax=ax_list[i], df_lon=lon_list[i], df_lat=lat_list[i],\
             list_season=list_season[i], seasons=seasons[i])
c3 = fig.colorbar(a, ax=[ax1, ax2, ax3, ax4])
c3.set_ticks(np.arange(-6,6))
c3.set_ticklabels(np.arange(-6,6))
fig.text(0.5, 0.93, '2018.07 to 2019.12', ha='center', va='center', fontsize=2.0*size)
plt.suptitle('FISHING  minus CLIM temperature difference', va='center_baseline', fontsize=2.5*size)
plt.savefig(save_path)
plt.show()