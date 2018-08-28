import matplotlib.pyplot as plt
import numpy as np
import pickle
import my_functions


#-------------------------
# Gabin L.
# gabin.laurent@u-psud.fr
#-------------------------



# This code :
# 1. Plots histogramms of the distribution of jet streams latitude over a time period
#    for preindustrial and postindustrial periods on same graphs for all regions
#    and seasons
# 2. Plots the evolution + trend of wind speed, of jet stream's latitude, and
#    of standard deviation of the jet stream over time for all regions and seasons
# 3. Write a file with some metrics (data on jet streams...)

# Parameters of the analysed model.
# Choose the pressure to be 25000 to analyze subtropical jet and 85000 for polar jets.
# Variable must be 'ua', as we analyse here some data from woollings methods to find
# jet streams.
variable = 'ua'
experiment = 'historicalMisc'
pressure = '25000'
period = 'preindustrial'
region = ['NAT','NPA','SAT','SPA']
season = ['JJA', 'SON', 'DJF', 'MAM']
model = 'GFDL-ESM2M'

filename = 'woollings_{}_{}_{}'.format(variable,experiment,pressure)
A=pickle.load(file('../analysed/'+filename +'.pickle'))


assert (len(A) == 4), "Problem in the data set length"

annual_A = [my_functions.seasonal_annual_mean(A[i]) for i in range(len(region))]


print "Seasonal annual mean done"

distrib = my_functions.distribution(A)

print "Distribution data prepared"

A = 0
q=1

my_file = open("../output/metrics_{}_{}_{}_{}.txt".format(model,experiment,variable,pressure),'w')
my_file.write("Region Season Av_lat_pre Std_lat_pre Av_lat_post Std_lat_post Av_speed_pre Std_speed_pre Av_speed_post Std_speed_post Av_var_pre Std_var_pre Av_var_post Std_var_post \n")

for i in range(0,4):    # for each region
    for j in range(0,4):    # for each season

        years = range(1861 , 1861+ len(annual_A[i][j][:,0]))

        # shift of the jet stream latitude :
        s , cov = np.polyfit(years,  annual_A[i][j][:,0] , 1 , cov = True)
        a , b = s[0], s[1]
        errors = np.sqrt(np.diag(cov))
        a_error , b_error = errors[0], errors[1]

        # latitude of the jet stream
        plt.subplot(3,1,1)
        plt.plot(range(1861, 1861 + len(annual_A[i][j][:,0])) , annual_A[i][j][:,0], color='dimgray')
        plt.plot(range(1866, 1866 + len(annual_A[i][j][:,0]) - 10), my_functions.moving_average(annual_A[i][j][:,0]) , color='red')
        plt.plot(years, [(a*w) + b for w in years], '--', color = 'dodgerblue', label ='y = a*x + b' + '\n' + (r'a = $ %s \pm %s $' %(format(a,'0.2e'),format(a_error,'0.2e'))) + '\n'  + (r'b = $ %s \pm %s $' %(format(b, '0.2e') ,format(b_error, '0.2e'))))
        plt.ylabel('Latitude (deg)')
        plt.legend(loc='best')

        # speed of the jet stream

        s , cov = np.polyfit(years, annual_A[i][j][:,1], 1 , cov = True)
        a , b = s[0], s[1]
        errors = np.sqrt(np.diag(cov))
        a_error , b_error = errors[0], errors[1]

        plt.subplot(3,1,2)
        plt.plot(range(1861, 1861 + len(annual_A[i][j][:,1])) , annual_A[i][j][:,1], color = 'dimgray')
        plt.plot(range(1866, 1866 + len(annual_A[i][j][:,1]) - 10), my_functions.moving_average(annual_A[i][j][:,1]), color = 'red')
        plt.plot(years, [(a*w) + b for w in years], '--', color = 'dodgerblue', label = (r'a = $ %s \pm %s $' %(format(a,'0.2e'),format(a_error,'0.2e'))))
        plt.ylabel(r'Wind speed $(m.s^{-1})$')
        plt.legend(loc='best')

        # standard deviation of the jet stream

        s , cov = np.polyfit(years, annual_A[i][j][:,2], 1 , cov = True)
        a , b = s[0], s[1]
        errors = np.sqrt(np.diag(cov))
        a_error , b_error = errors[0], errors[1]

        plt.subplot(3,1,3)
        plt.plot(range(1861, 1861 + len(annual_A[i][j][:,2])) , annual_A[i][j][:,2], color = 'dimgray')
        plt.plot(range(1866, 1866 + len(annual_A[i][j][:,2]) - 10), my_functions.moving_average(annual_A[i][j][:,2]), color = 'red')
        plt.plot(years, [(a*w) + b for w in years], '--', color = 'dodgerblue', label = (r'a = $ %s \pm %s $' %(format(a,'0.2e'),format(a_error,'0.2e'))))
        plt.legend(loc='best')
        plt.xlabel('Time (years)')
        plt.ylabel('Latitude st_d (deg)')

        # correlation between speed and standard deviation of the wind speed
        r = np.corrcoef([annual_A[i][j][:,1],annual_A[i][j][:,2]])[0][1]

        plt.suptitle('Jet stream, {} , Region : {}, Season : {}, R = {}'.format(experiment,region[i], season[j],round(r,2)))

        plt.tight_layout(h_pad = 1)
        plt.subplots_adjust(top=0.92)

        plt.savefig('../output/'+filename + '_{}_{}.pdf'.format(region[i],season[j]),bbox_inches='tight')

        plt.close()

        """# Histogram
        if i == 0 or i == 1 :
            X = range(30,61)
        else :
            X = range(-60,-29)

        plt.hist(annual_A[i][j][:,0],X, align = 'left', color='dimgray')
        plt.xlabel('Latitude (deg)')
        plt.ylabel('Occurence')
        plt.title('Jet stream latitude distribution, Region : {}, Season : {}'.format(region[i],season[j]))

        plt.savefig('../output/'+filename + '_{}_{}_hist.pdf'.format(region[i],season[j]),bbox_inches='tight')

        plt.close()"""

        # Metrics analysis
        metrics_val = [my_functions.metrics(annual_A[i][j][:,t]) for t in range(0,3)]

        my_file.write("{} {} ".format(region[i],season[j]))

        for d in range(0,3):
            my_file.write("%s %s %s %s " %(format(metrics_val[d][0], '0.3e') ,format(metrics_val[d][1], '0.3e') ,format(metrics_val[d][2], '0.3e'), format(metrics_val[d][3], '0.3e')))

        my_file.write("\n")

        print "Plots {} / 16 done".format(q)
        q +=1


for i in range(0,4):
    for j in range(0,4):

        if pressure == '85000':
            Y=np.array([23.25842697, 25.28089888, 27.30337079, 29.3258427, \
            31.34831461, 33.37078652,35.39325843, 37.41573034,39.43820225,\
            41.46067416,43.48314607,45.50561798,47.52808989,49.5505618 ,\
             51.57303371, 53.59550562,55.61797753,57.64044944,59.66292135,\
             61.68539326,63.70786517, 65.73033708, 67.75280899, 69.7752809 ,\
             71.79775281, 73.82022472, 75.84269663])

            if i ==0 or i ==1 :
                X=Y-0.1
                #X = np.linspace(25.5,75.5,26)
                ticks = [30,40,50,60,70]
            else :
                #X = np.linspace(-74.5,-24.5,51)
                X = -(Y[::-1]-0.1)
                ticks = [-70,-60,-50,-40,-30]

        if pressure == '25000' :
            Y=np.array([1.01123596,   3.03370787,   5.05617978,\
            7.07865169,   9.1011236 ,  11.12359551,  13.14606742, 15.16853933,\
            17.19101124,  19.21348315,  21.23595506, \
            23.25842697, 25.28089888, 27.30337079, 29.3258427, \
            31.34831461, 33.37078652,35.39325843, 37.41573034,39.43820225,\
            41.46067416,43.48314607,45.50561798,47.52808989,49.5505618 ,\
             51.57303371])

            if i ==0 or i ==1 :
                X=Y-0.1
                #X = np.linspace(25.5,75.5,26)
                ticks = [0,10,20,30,40,50]
            else :
                #X = np.linspace(-74.5,-24.5,51)
                X = -(Y[::-1]-0.1)
                ticks = [-50,-40,-30,-20,-10,0]

        plt.subplot(2,2,j+1)
        plt.hist( distrib[i][j][0] , X , color = 'dimgray', label='Past')
        plt.hist( distrib[i][j][1] , X , color = 'red' , histtype = 'step',label='Present')

        a = np.mean(distrib[i][j][0])
        b = np.mean(distrib[i][j][1])
        plt.axvline(x = a , color = 'black', linestyle ='--')
        plt.axvline(x = b , color = 'red', linestyle ='--')
        plt.title('{}'.format(season[j]))
        plt.xticks(ticks)

        if j == 0 or j == 2:
            plt.ylabel('Occurence')
        if j == 2 or j == 3:
            plt.xlabel('Latitude (deg)')

        if j == 0 :
            plt.legend(loc = 'best')


    plt.tight_layout(h_pad = 1)
    plt.subplots_adjust(top=0.89)

    plt.suptitle('Latitude distribution for {} region - {}'.format(region[i],experiment))
    plt.savefig('../output/' + filename + '_{}_hist.pdf'.format(region[i]))
    plt.close()

"""#### Histogram (occurencies of latitude)

if region == 'NAT':
    low_bound = 25
    up_bound = 65

X2 = range(low_bound, up_bound +1)

plt.hist(B[:,0], bins = X2, align = 'left')
plt.xlabel('Latitude (Deg)')
plt.ylabel('Occurencies')
plt.savefig('../output/'+filename + '_hist.pdf',bbox_inches = 'tight')
plt.close()


B=np.array(B)
print B.shape
if period == 'preindustrial':
    X=[i for i in range(1861,1891)]
if period == 'postindustrial':
    X=[i for i in range(1976,2006)]

else :
    X=[i for i in range (1861, 1861 + len(B))]

plt.plot(X,B[:,0])
plt.xlabel('Time')
plt.ylabel('Latitude (Deg)')
#plt.xticks(np.linspace(1861,1891,7))
plt.savefig('../output/'+filename + '_lat.pdf',bbox_inches='tight')
plt.close()

plt.plot(X,B[:,1])
plt.xlabel('Time')
plt.ylabel(r'Magnitude $(m.s^{-1})$')
#plt.xticks(np.linspace(1861,1891,7))
plt.savefig('../output/'+filename+'_mag.pdf',bbox_inches='tight')
plt.close() """
