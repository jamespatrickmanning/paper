# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 01:18:54 2020
Draw map of observation's temperature minus models' temperature.
@author: Mingchao & JiM
Modifications by JiM in Mid-April 2020 
- assumes input and output files are in the same directory as the code
- ignores values greater than a user-specified "maxdiff_ignore"
- had to add a pointer to the "PROJ" package after installing basemap
- added 200m isobath to define shelfedge
- added option to bin anomalies (old version without in "mod_obs_mapscatter.py")
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
import os
import datetime
from scipy.interpolate import griddata

####### Hardcodes
# the following line points to where the proj4 is located on JiM's Toshiba laptop
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
maxdiff_ignore=6 # ignore when difference is greater than this number
data_list = 'vessel_dfs_C.csv'
which_method='binned'      # 'scatter' or 'binned'
gridsize=0.5 # needed when which_method is binned in units of lat/lon
which_mode='models' # 'models' or 'season'
which_model=4 # 0-4 depends on options below used when which_mode= "season"     
options=['CLIMATOLOGY','DOPPIO','FVCOM','GOMOFS','MODELS']
models=[ 'Clim_T','Doppio_T','FVCOM_T','GoMOLFs_T','MODELS']
seasons = ['WINTER', 'SPRING', 'SUMMER', 'FALL']
option=options[which_model]    
save_path = option+'_'+which_method+'_obs_mod_map.png'
start_time = datetime.datetime(2019,1,1,0,0,0)
end_time = datetime.datetime(2020,1,1,0,0,0)
time_period=str(start_time.year)
bathy=True
gs=50      # number of bins in the x and y direction so,  if you want more detail, make it bigger
ss=100     # subsample input data so, if you want more detail, make it smaller
cont=[-200]    # contour level
mila=36.;mala=44.5;milo=-76.;malo=-66.#min & max lat and lo
#########  END HARDCODES ######################
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

def draw_basemap(fig, ax, df_lon, df_lat, list_season, seasons,bathy,gs,ss,milo,malo,mila,mala,cont,which_method,gridsize):
    # if bathy=True, plot bathy
    ax = fig.sca(ax)
    m = Basemap(projection='stere',lon_0=(milo+malo)/2,lat_0=(mila+mala)/2,lat_ts=0,llcrnrlat=mila,urcrnrlat=mala,\
                llcrnrlon=milo,urcrnrlon=malo,rsphere=6371200.,resolution='l',area_thresh=100)
    #m.drawcoastlines()
    m.fillcontinents(color='grey',lake_color='grey')
    if (ax == ax1) or (ax == ax3): #draw parallels
        parallels = np.arange(mila,mala,3)
        m.drawparallels(parallels, labels=[1,0,0,0], fontsize=10, linewidth=0.0)
    if (ax == ax3) or (ax==ax4):# draw meridians
        meridians = np.arange(milo+2,malo,4)
        m.drawmeridians(meridians, labels=[0,0,0,1], fontsize=10, linewidth=0.0)
    if which_method=='scatter':
        a=m.scatter(df_lon, df_lat, c=list_season, cmap='coolwarm',marker='o', linewidths=0.01, latlon=True)
    else: 
        print('binning data')
        xi = np.arange(milo,malo,gridsize)# longitude grid
        yi = np.arange(mila,mala,gridsize)# latitude grid
        X,Y,Z = sh_bindata(df_lon, df_lat,list_season,xi,yi)
        X,Y = m(X.flatten(),Y.flatten())
        print('finally adding scatter plot ')
        a=m.scatter(X, Y, c=Z, cmap='coolwarm',marker='o', linewidths=0.01)
        a.set_clim(-1*maxdiff_ignore,maxdiff_ignore)        
    if bathy==True: # get some detail bathymetry from USGS
        add_isobath(m,gs,ss,cont)
    mx,my=m(milo+.2,mala-.5)
    #plt.text(mx+50000,my-110000,seasons,color='w',fontsize=18,fontweight='bold')
    plt.text(mx,my,seasons,color='w',fontsize=18,fontweight='bold')
    plt.text(mx,my-100000,'mean=' +str(np.format_float_positional(np.mean(list_season), precision=2, unique=False, fractional=False)),color='w',fontsize=14,fontweight='bold')
    plt.text(mx,my-180000,'RMS = '+str(np.format_float_positional(np.sqrt(np.mean(np.square(list_season))), precision=2, unique=False, fractional=False)),color='w',fontsize=14,fontweight='bold')
    return a
##### MAIN CODE ######
DF=pd.read_csv(data_list, index_col=0)    # reads input file with obs & models
DF=DF.loc[DF['difference']<maxdiff_ignore]# gets rid of outlyers
DF['time'] = pd.to_datetime(DF['time'])   # converts date time
DF.index=DF['time']                       # makes time index
DF['month']=DF.index.month
season = ((DF.month % 12 + 3) // 3).map({1:'WINTER', 2: 'SPRING', 3:'SUMMER', 4:'FALL'})
DF['season']=season.values                # adds a "season" column
fig = plt.figure(figsize=(10,10))
size=min(fig.get_size_inches())
gsc = gridspec.GridSpec(2, 2,wspace=0.0, hspace=0.0,width_ratios=[1, 1], 
         top=1.-0.3/(2+1), bottom=0.3/(2+1), 
         left=0.3/(2+1), right=1-0.3/(2+1)) 
ax1 = fig.add_subplot(gsc[0,0])
ax1.axes.get_yaxis().set_visible(False)
ax2 = fig.add_subplot(gsc[0,1])
ax2.axes.get_yaxis().set_visible(False)
ax3 = fig.add_subplot(gsc[1,0])
ax4 = fig.add_subplot(gsc[1,1])
ax_list = [ax1, ax2, ax3, ax4]
# Now, loop through the 4 season
for i in range(4):# this runs the other three
    if which_mode=='season':
        this_season=DF.loc[DF['season']==seasons[i]]
        a=draw_basemap(fig, ax=ax_list[i], df_lon=this_season['lon'].values, df_lat=this_season['lat'].values,\
            list_season=this_season['difference'].values, seasons=seasons[i],bathy=True,gs=gs,ss=ss,milo=milo,malo=malo,mila=mila,mala=mala,cont=cont,which_method=which_method,gridsize=gridsize)
    else: # which_mode= 'models'
        diff=(DF['observation_T']-DF[models[i]]).values
        id=np.where(abs(diff)<maxdiff_ignore)
        a=draw_basemap(fig, ax=ax_list[i], df_lon=DF['lon'].values[id], df_lat=DF['lat'].values[id],\
            list_season=diff[id], seasons=options[i],bathy=True,gs=gs,ss=ss,milo=milo,malo=malo,mila=mila,mala=mala,cont=cont,which_method=which_method,gridsize=gridsize)
c3 = fig.colorbar(a, ax=[ax1, ax2, ax3, ax4])
c3.set_ticks(np.arange(-1*maxdiff_ignore,maxdiff_ignore))
c3.set_ticklabels(np.arange(-maxdiff_ignore,maxdiff_ignore))
fig.text(0.5, 0.93, time_period, ha='center', va='center', fontsize=2.0*size)
plt.suptitle('Observed bottom temperature minus '+option, va='center_baseline', fontsize=2.5*size)
plt.savefig(save_path)
plt.show()
