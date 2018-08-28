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


# This code helps to locate polar and subtropical jet streams, with a method
# proposed by Tim Woollings in 2010.
# It only works if the variable used is 'ua' (see line number 89 of the code),
# which is the eastward wind componant value.
# Plus, you need to specify the properties of the analysed model.


# Parameters of the model used
product='output1'
model='GFDL-ESM2M'
ensemble_element='r1i1p5'
experiment='historicalMisc'
realm='atmos'
frequency='day'
variable='ua'
pressure=25000

# This is the degrees of latitude that should separate polar and subtropical
# jet streams. It is up to you to choose the value of this variable.
error_lat=10

input_options={'product': product,
                 'model': model,
                 'experiment': experiment,
                 'realm': realm,
                 'frequency': frequency,
                 'variable': variable,
                 'ensemble_element': ensemble_element
                 }


# Two pressure levels are already registered, you can choose to work at
# 850 hPa to seek polar jets, or at 250 hPa for both of them.
# If you want to study another pressure level, be sure to adjust the "plev"
# variable to have the right data in the pickle file.
if pressure == 85000:
    plev = 1
if pressure == 25000:
    plev = 4

analysis=Analysis(input_options)
analysis.get_files(only_files=True)

print len(analysis.files), "files will be analyzed"

data_list=[]


# Files are loaded here...

for fichier in range(0,len(analysis.files)) : #Loop over all the data files available

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


# Woollings method to seek jet streams
if variable == 'ua' :
    if pressure == 85000 :
        reg = ['NAT','NPA','SAT','SPA']

        jet_stream = [my_functions.find_jet_stream(data_list, analysis.lons, analysis.lats, region = reg[i]) for i in range(len(reg))]

        jet_stream = np.array(jet_stream, dtype = np.float32)

        pickle.dump(jet_stream, file('../analysed/woollings_{}_{}_{}.pickle'.format(variable,experiment,pressure), 'w'))

        print "Jet stream located at 850hPa"

    if pressure == 25000 :
        reg = ['NAT','NPA','SAT','SPA']

        jet_stream = [my_functions.find_jet_stream_sub(data_list, analysis.lons, analysis.lats,experiment, region = reg[i], error=error_lat) for i in range(len(reg))]

        jet_stream = np.array(jet_stream, dtype = np.float32)

        pickle.dump(jet_stream, file('../analysed/woollings_{}_{}_{}.pickle'.format(variable,experiment,pressure), 'w'))

        print "Jet stream located at 250hPa"

#    assert variable_data.shape[0] == wind_list.shape, ('Problem in the computation'
#                                        'of the wind speed')

"""
if __name__ == '__main__':
    log_format = ""%(levelname)s:%(name)s:%(lineno)s:%(funcName)s:%(message)s"
    logging.basicConfig(level=logging.DEBUG, format=log_format)
"""
