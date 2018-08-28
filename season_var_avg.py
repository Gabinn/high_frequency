from analysis import Analysis
from netCDF4 import Dataset
import numpy as np
from numpy import ma
from pressure_interpolation import interpolate_wrapper as pressure_interpolate
import pickle
import my_functions


#-------------------------
# Gabin L.
# gabin.laurent@u-psud.fr
#-------------------------



# This code computes average for Summer (JJA) and Winter (DJF) season over a specified
# time period. An annual average is also computed. You need to specify the time scale,
# and precise the number of files that correspond to this time scale.
# For example the GFDL-ESM2M model starts from 1860 to 2005 and data is
# separated in files of 5 years of data. If you want to study the period from 1860 to 1890
# the line 58 must be written as for fichier in range(0,6) to study the 30 first years
# written in the first 6 files. Don't forget to name the time period variable (line 57) as
# "preindustrial" for example. The file with the averaged data will depend on this
# variable name
# You need to specify the properties of the analysed model.
# The code works at 250 hPa and 850 hPa for a pressure dependent variable.
# For not pressure dependant variable the code works as well.

# Parameters of the model used
product='output1'
model='GFDL-ESM2M'
ensemble_element='r1i1p1'
experiment='historicalNat'
realm='atmos'
frequency='day'
variable='ua'
pressure=25000

input_options={'product': product,
                 'model': model,
                 'experiment': experiment,
                 'realm': realm,
                 'frequency': frequency,
                 'variable': variable,
                 'ensemble_element': ensemble_element
                 }


if pressure == 85000:
    plev = 1
if pressure == 25000:
    plev = 4


analysis=Analysis(input_options)
analysis.get_files(only_files=True)

print len(analysis.files), " files will be analyzed"

data_list=[]

# Choose here the time period of the analysis
# The 'period' variable is just a label for the files created.
period = 'preindustrial'
for fichier in range(0,6) : #Loop over all the data files available


    analysis.mf = Dataset(analysis.files[fichier])
    variable_data = np.asarray(analysis.mf.variables[analysis.variable][:],
                                dtype = np.float32)

    len_time = len(variable_data)

    final_variable_data = []

    if len(variable_data.shape) == 4 :

        for time in range(0,len_time):

            final_variable_data.append(variable_data[time][plev])

        data_list += list(final_variable_data)

    if len(variable_data.shape) == 3 :

        data_list += list(variable_data)


    analysis.lons = np.asarray(analysis.mf.variables['lon'][:], dtype=np.float32)
    analysis.lats = np.asarray(analysis.mf.variables['lat'][:], dtype=np.float32)

    print "files {} are loaded".format(fichier+1)


final_variable_data = 0
variable_data = 0


# Average computation

len_time = len(data_list)
len_lats = len(data_list[0])
len_lons = len(data_list[0][0])

avg_list = []


for lats in range(0,len_lats):
    lons_avg = []
    print lats
    for lons in range(0,len_lons):
        S=0
        for time in range(0,len_time):
            S += data_list[time][lats][lons]
        lons_avg.append(S/float(len_time))
    avg_list.append(lons_avg)

avg_list = np.array(avg_list, dtype=np.float32)

invalid_mask = ((avg_list < 1e20*1.01) & (avg_list > 1e20*0.99))

avg_list = ma.array(avg_list, mask = invalid_mask, fill_value = 1e20, dtype = np.float32)

final = (avg_list, analysis.mf.variables['lon'][:], analysis.mf.variables['lat'][:])

# Saving of the file

pickle.dump(final, file('../analysed/{}_{}_average_{}_{}_{}_ANN.pickle'.format(model,period,variable,experiment,pressure),'w'))


# SUMMER average

summer=my_functions.summer_mean(data_list)

summer = np.array(summer, dtype=np.float32)

invalid_mask1 = ((summer < 1e20*1.01) & (summer > 1e20*0.99))

summer = ma.array(summer, mask = invalid_mask1, fill_value = 1e20, dtype = np.float32)

final1 = (summer, analysis.mf.variables['lon'][:], analysis.mf.variables['lat'][:])

# Saving of the file

pickle.dump(final1, file('../analysed/{}_{}_average_{}_{}_{}_SUM.pickle'.format(model,period,variable,experiment,pressure),'w'))

# WINTER average

winter=my_functions.winter_mean(data_list)

winter = np.array(winter, dtype=np.float32)

invalid_mask2 = ((winter < 1e20*1.01) & (winter > 1e20*0.99))

winter = ma.array(winter, mask = invalid_mask2, fill_value = 1e20, dtype = np.float32)

final2 = (winter, analysis.mf.variables['lon'][:], analysis.mf.variables['lat'][:])

# Saving of the file

pickle.dump(final2, file('../analysed/{}_{}_average_{}_{}_{}_WIN.pickle'.format(model,period,variable,experiment,pressure),'w'))



"""
"""
if __name__ == '__main__':
    log_format = ""%(levelname)s:%(name)s:%(lineno)s:%(funcName)s:%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
"""
