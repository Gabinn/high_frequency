import logging
import gc
from data import files_helper, short_var, long_to_short
from calendar import monthrange
import matplotlib.pyplot as plt
from netCDF4 import Dataset, MFDataset
import numpy as np
import cPickle as pickle
import os
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
from numpy import ma
import pandas as pd
from pdb import set_trace
from datetime import datetime
from textwrap import wrap
from time import clock, strftime
from pressure_interpolation import interpolate_wrapper as pressure_interpolate
import pickle
import matplotlib


#-------------------------
# Gabin L.
# gabin.laurent@u-psud.fr
#-------------------------


# This code can plot a map with variable values
# Parameters of the analysed model.
model = 'GFDL-ESM2M'
variable='ua'
experiment='historicalMisc'
season = 'SUM'
period='preindustrial'
pressure=25000

# To be changed !!!!!!
vmin,vmax = 0,55

title = 'Pre_industrial average eastward wind speed - Historical - Annual'

filen = '{}_{}_average_{}_{}_{}_{}'.format(model,period,variable,experiment,pressure,season)

A= pickle.load(file('../analysed/'+filen+'.pickle'))

def map_plot(lons, lats, data, analysis=None, apply_cyclic_lons=True,
                name='clim_avg',
                 title='', errors=None, s=15,
                 alpha=0.7, sigma=2.):


    if variable == 'tas':
        data = data - 273.15


    if variable == 'pr':
        data = data * 1000

    logger = logging.getLogger(__name__)
    if apply_cyclic_lons:
        data, lons = add_cyclic_point(data, coord=lons)

        # rough fix to make this work for now
    rows = np.array([lats.size, data.shape[0]])
    columns = np.array([lons.size, data.shape[1]])
    if not np.diff(rows)[0] == 0:
        logger.debug('rows adjusted {:}'.format(rows))
    if not np.diff(columns)[0] == 0:
        logger.debug('columns adjusted {:}'.format(columns))
    lons = lons[:min(columns)]
    lats = lats[:min(rows)]
    data = data[:min(rows), :min(columns)]



    Liste=[]
    Liste += [abs(np.amax(data))]
    Liste += [abs(np.amin(data))]
    maximum_de_la_liste = np.amax(Liste)
    print np.amin(data)
    print Liste

    #assert vmax > maximum_de_la_liste , ("Probleme de bornes de la colorbar, vmax = {}".format(maximum_de_la_liste))

    print maximum_de_la_liste

    fig, ax = plt.subplots()
    ax = plt.axes(projection=ccrs.PlateCarree())
    #plt.contourf(lons, lats, data, np.linspace(-40,40,41), transform=ccrs.PlateCarree(),vmin=-40, vmax=40, cmap=plt.cm.get_cmap('RdBu_r'))

    plt.contourf(lons, lats, data , np.linspace(vmin,vmax,41),transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax, cmap=plt.cm.get_cmap('Reds'))

    #plt.contourf(lons, lats, data, np.linspace(vmin,vmax,41),transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax, cmap=plt.cm.get_cmap('Greys'))

    ax.coastlines(linewidth=0.5)
    #plt.pcolormesh(lons, lats, data, vmin = vmin, vmax = vmax, cmap=plt.cm.get_cmap('Reds'))
    #plt.pcolormesh(lons, lats, data, vmin = -40, vmax= 40 ,cmap=plt.cm.get_cmap('RdBu_r'))

    cbar = plt.colorbar(orientation='horizontal',ticks=np.linspace(vmin,vmax,((vmax-vmin)/10)+1))
    #plt.set_cmap('Reds')

    cbar.set_label(r'Eastward wind speed $(m.s^{-1})$',fontsize=12)
    #cbar.set_label(r'Cloud total fraction (%)',fontsize=12)
    #ax.set_title('blabla')

    #filename = '../output/avg_wind_speed_test_postindustrial'

    ax.set_yticks(np.linspace(-90,90,7))
    ax.set_xticks(np.linspace(-180,180,7))
    ax.tick_params('x',bottom='off',top='off',labelbottom='on', labeltop='on',labelsize=9)
    ax.tick_params('y',left='off',right='off',labelright='on', labelleft='on',labelsize=9)
    ax.grid(color='white',linestyle='--',linewidth=0.3)

    filename = filen
    fig.savefig('../output/'+filename+'.pdf',bbox_inches='tight')
    plt.close()

map_plot(A[1],A[2],A[0])
