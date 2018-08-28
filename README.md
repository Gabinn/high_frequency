high_frequency description
==
This repository contains high frequency analysis codes for jet streams tracking.  
Do not hesitate to contact me if you have any queries, at gabin.laurent@u-psud.fr

IMPORTANT
-
To run these codes, they should be in the "analysis" repository of codes written By Alex Khun Regnier that are available if you have a granted acces to his GitHub repository "storm_tracks". This is crucial as the codes here imports some of his codes. You should put those files in the "analysis" repository.  
Please note that these codes were written for the GFDL-ESM2M model, then in "my_functions.py" the precision of this model is used to track jet stream. You may have to change this a little bit. You may also encounter some problems if pressure levels are not define in the same way, and if you are not using daily data (at least for the jet stream tracking).

Code description
-
Here is a description of the codes and how they should be use:

- "locate_jet.py" : This is a routine that tracks jet streams using a method proposed by Tim Woollings (2010). It consists in averaging the eastward wind component over all longitudes for each latitude for a given region at each time step (every day), and considering the latitude for which the averaged wind speed is the greater as being the latitude of the jet stream. This code tracks the polar jet at 850 hPa and the sub-tropical jet at 250 hPa.  
You need to firstly track the polar jet at 850 hPa as it location is used when you track sub-tropical jet at 250 hPa. You choose which jet you track by choosing the pressure value in the code, in Pascals (25000 or 85000). Once the polar jet is located, you can go for the subtropical one. It will look for it with a minimum degrees of latitude between the two jets. You choose the minimum degrees of latitude by giving a value to "error_lat" variable in the code.

- "season_var_avg.py" : This code average a variable for Summer and Winter season over a chosen time period. More details are given in the script.

- "avg_trend.py" : This code computes an average of the trend and the Central Mean Latitude for multiple realisation or models that have same frequency of data and same time period.

- "my_functions.py" : This code contains all the functions/sub-routines used in previous files. It contains the tracking programs using Woollings' method to find polar and subtropical jets. It also contains the ones to compute seasonnal means, and also routine used in next python files that get the distribution of jet's latitudes over time.  
This code is where you should have a look if you want to change edges of region boxes (when you are looking for jet streams location for instance). In find_jet_stream() and find_jet_stream_sub() you can change region edges.

- "plot_woollings.py" : This code has three main capacities : 1. to plot the distribution of jets latitudes for a given time period. 2. to write some metrics files about jet streams data. 3. to plot the latitude of the jet, the variability (standard deviation) of it, and the magnitude of jet speed, over time, and their trends. It also give the correlation coefficient between the variability of the jet stream and the magnitude of its speed.

- "my_plot.py" : Plots a map for an analysed variable for one model

- "my_plot_diff.py" : Plots a map with the difference (postindustrial-preindustrial) period for a variable.

The first three files are codes that analyse data and create pickle files in the "analysed" repository. "my_functions.py" just contains some sub-routines. The last three files with the keyword "plot" in the name are to be used to plot analysed data once you used one of the first three files, and create plots in the "output" repository.
The "period" variable used in those codes should be "preindustrial" or "postindustrial" and reffers to the time period of the data. Normally, the files create by the analysis codes have named that are coherent and should work with plotting codes.

Do not hesitate to contact me if you have any queries at gabin.laurent@u-psud.fr  !!

Gabin L.
