from analysis_functions import *
import pickle
import os
import numpy as np

#-------------------------
# Gabin L.
# gabin.laurent@u-psud.fr
#-------------------------



def process_variable_mean_test():
    """	Process analysis for different models
	You can choose differents models or different
	ensemble_elements. This code just return the
	analysed data with the mean for the trend and cml, and
	some values for other data (average, gradient,...)
	that are meaningless, don't use them.
	To plot the mean trend, go to plotting.py from Alex Khun Regnier's code
    and in plot_all, comments command lines where the plotting of average,
    gradient, trend gradient are done because they are
    meaningless here. """


    """Parameters/input options of all models"""
    season = 'ANN'
    region = 'GLO'
    product='output1'
    model=['GFDL-ESM2M']
    ensemble_element=['r1i1p3','r2i1p3','r3i1p3','r4i1p3','r5i1p3']
    experiment='historicalNat'
    realm='atmos'
    frequency='mon'
    variable='ua'
    io=[]

    p0 = None
    p1 = None

    L=('GLO','NAT','SAT','NPA','SPA')

    N=len(model)

    model1='&'.join(model)
    ensemble_element1='&'.join(ensemble_element)

    if len(model)==len(ensemble_element):
        for i in range(0,len(model)):
            io.append({'product': product,
                             'model': model[i],
                             'experiment': experiment,
                             'realm': realm,
                             'frequency': frequency,
                             'variable': variable,
                             'ensemble_element': ensemble_element[i]
                             })

    else:
        print('Length problem between models and ensemble_elements lists')

    """get the .pickle files for each model"""
    for i in range(0,N):
        process_variable(io[i], region, season, p0, p1)


    if p0==None:
	p0='p0'
	p1='p0'

    mean_cml_list = []
    stand_dev_list = []

    for q in range(0,5):
        filename=[]
        files=[]
        meanfile=[]
        for i in range(0,N):
            #We load for each season the two set of data we want to average
            filename.append("../analysed/{}_{}_{}_{}_T0_{}_{}_{}_all_{}_{}.pickle".format(io[i]['model']
            ,experiment,frequency,io[i]['ensemble_element'],variable,L[q],season,p0,p1))

            files.append(pickle.load(file(filename[i])))

        for j in range(0,len(files[1])):
            if j!=1 and j!=4:
                meanfile.append(files[1][j])
            else:
                meanfile.append([])

    	T=[0 for i in range(0,N-1)]

        #Computation of the mean of the trend :
        M1, D1 = [], []
        for j in range(0, len(files[1][1][0])):
            M2, D2 = [], []
            for k in range(0, len(files[1][1][0][0])):
                F=[]
                S=0
                for m in range(0,N-1):
                    if files[m][1][0][j].mask[k] == False and files[m+1][1][0][j].mask[k] == False:
                        F+=[0]
                if F==T:
                    M2.append(0)
                    for p in range(0,N):
                        S+=files[p][1][0][j][k]
                    D2.append(S/N)
                else:
                    M2.append(1)
                    D2.append(0)
            M1.append(M2)
            D1.append(D2)
        meanfile[1].append(ma.masked_array(D1,M1))


        #Computation of the standard deviation for the mean trend :
        M1, D1 = [], []
        for j in range(0, len(files[1][1][1])):
            M2, D2 = [], []
            for k in range(0, len(files[1][1][1][0])):
                F=[]
                S=0
                for m in range(0,N-1):
                    if files[m][1][1][j].mask[k] == False and files[m+1][1][1][j].mask[k] == False:
                        F.append(0)
                if F==T:
                    M2.append(0)
                    for p in range(0,N):
                        S+=(files[p][1][0][j][k]-meanfile[1][0][j][k])**2
                    D2.append(np.sqrt((1./(N-1))*S))
                else:
                    M2.append(1)
                    D2.append(0)
            M1.append(M2)
            D1.append(D2)
        meanfile[1].append(ma.masked_array(D1,M1))

        #Computation of the mean of central_mean_latitude :
        gradient_total=0

        for j in range(0,N):

            start_year = files[j][7]
            years = np.arange(start_year, start_year+len(files[j][4]))
            p, V = np.polyfit(years, files[j][4],1,cov=True)
            slope = p[0]
            origin_ordinate = p[1]

            gradient_total += slope

        mean_cml = gradient_total/N
        mean_cml_list += [str(mean_cml)]

        # Computation of the standard deviaation of cml :
        Sum=0

        for j in range(0,N):

            start_year = files[j][7]
            years = np.arange(start_year, start_year+len(files[j][4]))
            p, V = np.polyfit(years, files[j][4],1,cov=True)
            slope = p[0]
            origin_ordinate = p[1]

            Sum+=(p[0]-mean_cml)**2

        stand_dev = np.sqrt((1./(N-1))*Sum)
        stand_dev_list += [str(stand_dev)]

        #fit_object = np.poly1d(p)
        #fit = np.array([fit_object(y) for y in years])

        for i in range(0,N):
            os.remove(filename[i])

        meanfile=tuple(meanfile)

        #Save the new data set into pickle file
        filename1 = '../analysed/{}_{}_{}_{}_T0_{}_{}_{}_all_{}_{}.pickle'.format(model1,
        experiment, frequency, ensemble_element1,
        variable,L[q], season, p0, p1)

        pickle.dump(meanfile, file(filename1, 'w'))

    """ Create and write in the file of mean cml values """
    mon_fichier = open("../output/mean_cml_{}.txt".format(variable),'w')

    for j in range(0,N):
        mon_fichier.write("{} {} {}\n".format(L[j], mean_cml_list[j], stand_dev_list[j]))

    mon_fichier.close()

process_variable_mean_test()
