import numpy as np
import pickle

#-------------------------
# Gabin L.
# gabin.laurent@u-psud.fr
#-------------------------


""" All functions used for the high analysis frequency process"""

""" Computes average for DAILY DATA for winter """
def winter_mean(L):

    len_lats = len(L[0])
    len_lons = len(L[0][0])

    assert len(L)%365 == 0 , ('Problem with data set, probably with leap years')

    N=len(L)/365

    day_in_months=[31,28,31,30,31,30,31,31,30,31,30,31]


    time=0

    """ Seasonal WINTER average """

    n1=day_in_months[0]+day_in_months[1] # day number between 1st june and 31 august
    n2 = day_in_months[11]

    winter_avg=[]

    for lats in range(0,len_lats):

        lons_list_m=[]

        for lons in range(0,len_lons):

            time = 0 #1st june is the 125th day of the year

            S=0

            for k in range(0,N):

                for p in range(0,n1):


                    S+=L[p+time][lats][lons]

                time += 334

                for p in range(0,n2):


                    S+=L[p+time][lats][lons]

                time += 31

            lons_list_m.append(S/float((n1+n2)*N))

        winter_avg.append(lons_list_m)

    return winter_avg

""" Computes average for DAILY DATA for summer """
def summer_mean(L):

    len_lats = len(L[0])
    len_lons = len(L[0][0])

    assert len(L)%365 == 0 , ('Problem with data set, probably with leap years')

    N=len(L)/365

    day_in_months=[31,28,31,30,31,30,31,31,30,31,30,31]


    time=0

    """ Seasonal SUMMER average """

    n=day_in_months[5]+day_in_months[6]+day_in_months[7] # day number between 1st june and 31 august

    summer_avg=[]

    for lats in range(0,len_lats):

        lons_list_m=[]

        for lons in range(0,len_lons):

            time = 124 #1st june is the 125th day of the year

            S=0

            for k in range(0,N):

                for p in range(0,n):


                    S+=L[p+time][lats][lons]

                time += 365

            lons_list_m.append(S/float(n*N))

        summer_avg.append(lons_list_m)

    return summer_avg


# Definition :  Function that find the maximum jet stream speed with respect to
#               the method used by Woollings : at each time step, average all
#               longitude for each latitude, and then pick the latitude with the
#               highest average value. You can precise edges of used regions.
#               This code is used to find the polar jet at 850 hPa.
def find_jet_stream(data,lons,lats,region='NAT'):

    if region == 'NAT' :

        low_lon = 300
        up_lon = 0
        low_lat = 25
        up_lat = 75

    if region == 'NPA':

        low_lon = 150
        up_lon = 210
        low_lat = 25
        up_lat = 75

    if region == 'SAT':

        low_lon = 310
        up_lon = 10
        low_lat = -75
        up_lat = -25

    if region == 'SPA':

        low_lon = 190
        up_lon = 290
        low_lat = -75
        up_lat = -25


    # Selection of the longitude and latitude, taken into account the
    # precision of the model selected (here GFDL-ESM2M)
    pos_low_lon = np.where((abs(lons-low_lon) < 2.5) & (lons <= low_lon))[0][0]
    pos_up_lon = np.where((abs(lons-up_lon) < 2.5) & (lons >= up_lon))[0][0]
    pos_low_lat = np.where((abs(lats-low_lat) < 2.04) & (lats <= low_lat))[0][0]
    pos_up_lat = np.where((abs(lats-up_lat)<2.04) & (lats >= up_lat))[0][0]

    len_time = len(data)
    len_lats = len(data[0])
    len_lons=len(data[0][0])

    jet_stream = []

    if region == 'NAT':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon - len_lons , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]

    if region == 'NPA':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]

    if region == 'SAT':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon - len_lons , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]


    if region == 'SPA':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon, pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]


    return jet_stream



# Definition :  Function that find the maximum sub-tropical jet stream speed  almost
#               exactly as the previous one. But this one use the polar jet stream
#               at 850hPa first. The parameters "error" is the number of
#               latitude that must separate polar and subtropical jets.
#               The error variable has a default value, but should be Choose
#               in "locate_jet.py" code.
def find_jet_stream_sub(data,lons,lats,experiment,region='NAT',error=5):

    polar_jet = pickle.load(file('../analysed/woollings_ua_{}_85000.pickle'.format(experiment)))

    if region == 'NAT' :        # Box lowered a little in latitude towards equator

        low_lon = 300
        up_lon = 0
        low_lat = 2
        up_lat = 50

    if region == 'NPA':

        low_lon = 150
        up_lon = 210
        low_lat = 2
        up_lat = 50

    if region == 'SAT':

        low_lon = 310
        up_lon = 10
        low_lat = -50
        up_lat = -2

    if region == 'SPA':

        low_lon = 190
        up_lon = 290
        low_lat = -50
        up_lat = -2


    # Selection of the longitude and latitude, taken into account the
    # precision of the model selected (here GFDL-ESM2M)
    pos_low_lon = np.where((abs(lons-low_lon) < 2.5) & (lons <= low_lon))[0][0]
    pos_up_lon = np.where((abs(lons-up_lon) < 2.5) & (lons >= up_lon))[0][0]
    pos_low_lat = np.where((abs(lats-low_lat) < 2.04) & (lats <= low_lat))[0][0]
    pos_up_lat = np.where((abs(lats-up_lat)<2.04) & (lats >= up_lat))[0][0]

    len_time = len(data)
    len_lats = len(data[0])
    len_lons=len(data[0][0])

    jet_stream = []

    if region == 'NAT':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon - len_lons , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            while (max_lat >= (polar_jet[0][time][0] - error )):
                for z in range(max_lat_pos, len(lats_list)):
                    lats_list[z] = -1e20
                max_val = np.amax(lats_list)
                max_lat_pos = np.where( lats_list == max_val )[0][0]
                max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]

        print "NAT finished"

    if region == 'NPA':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            while (max_lat >= (polar_jet[1][time][0] - error )):
                for z in range(max_lat_pos, len(lats_list)):
                    lats_list[z] = -1e20
                max_val = np.amax(lats_list)
                max_lat_pos = np.where( lats_list == max_val )[0][0]
                max_lat = lats[pos_low_lat + max_lat_pos]


            jet_stream += [[max_lat,max_val]]

        print "NPA finished"
    if region == 'SAT':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon - len_lons , pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            while (max_lat <= (polar_jet[2][time][0] + error )):
                for z in range(0,max_lat_pos +1):
                    lats_list[z] = -1e20
                max_val = np.amax(lats_list)
                max_lat_pos = np.where( lats_list == max_val )[0][0]
                max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]
        print "SAT finished"

    if region == 'SPA':

        for time in range(0,len_time):

            lats_list = []

            for lat in range (pos_low_lat,pos_up_lat +1 ):
                S=0
                val=0
                for lon in range (pos_low_lon, pos_up_lon +1 ):
                    if (data[time][lat][lon] < 1e20*0.99) :
                        S+=data[time][lat][lon]
                        val += 1

                lats_list.append(S/float(val))

            max_val = np.amax(lats_list)
            max_lat_pos = np.where( lats_list == max_val )[0][0]

            max_lat = lats[pos_low_lat + max_lat_pos]

            while (max_lat <= (polar_jet[3][time][0] + error )):
                for z in range(0,max_lat_pos +1):
                    lats_list[z] = -1e20
                max_val = np.amax(lats_list)
                max_lat_pos = np.where( lats_list == max_val )[0][0]
                max_lat = lats[pos_low_lat + max_lat_pos]

            jet_stream += [[max_lat,max_val]]
        print "SPA finished"

    return jet_stream


# Definition :  This code compute the seasonal annual mean from a given data set.
#               This code is specifically written for the woollings method.
#               Doesn't compute the first year of winter
# Input :   A regional list
# Output :  Summer, autumn, winter, spring list set up as :
#           - mean_lat / mean_val / std_lat
def seasonal_annual_mean(data):
    len_time = len(data)


    assert (len_time % 365 == 0), "problem length data set"

    N = len_time / 365

    winter, summer, spring, autumn = [],[],[],[]

    # Spring, Summer, Autumn
    time = 0
    for i in range(0 , N):
        spring.append([np.mean(data[:,0][time + 59 : time + 151]),np.mean(data[:,1][time + 59 : time + 151]), np.std(data[:,0][time + 59 : time + 151])])
        summer.append([np.mean(data[:,0][time + 151 : time + 243]),np.mean(data[:,1][time + 151 : time + 243]), np.std(data[:,0][time + 151 : time + 243])])
        autumn.append([np.mean(data[:,0][time + 243 : time + 334]),np.mean(data[:,1][time + 243 : time + 334]), np.std(data[:,0][time + 243 : time + 334])])
        time += 365

    # Winter
    time = 0

    a0 = data[:,0][time : time +59]
    a1 = data[:,1][time : time +59]

    time = 365

    b0 = data[:,0][time -31 : time]
    b1 = data[:,1][time -31 : time]


    winter.append([np.mean( np.append(a0,b0)) , np.mean(np.append(a1,b1)), np.std(np.append(a0,b0))])

    for i in range(1,N) :
        winter.append([np.mean(data[:,0][time - 31 : time + 59]),np.mean(data[:,1][time - 31 : time + 59]), np.std(data[:,0][time -31 : time + 59])])
        time += 365

    spring = np.array(spring , dtype = np.float32)
    summer = np.array(summer , dtype = np.float32)
    autumn = np.array(autumn , dtype = np.float32)
    winter = np.array(winter , dtype = np.float32)

    return summer, autumn, winter, spring


# Definition :  Compute a moving average over a data set, with the moving Parameters
#               W (W point before and W point after)
# Input :   - data : data set
#           - W : moving parameter (W before and W after)
# Output :  - the moving averaged data set, but without first 5 and last 5 lines
#               (len(output) == len(input) - 10)
def moving_average(data, W = 5) :

    len_data = len(data)

    averaged_data = [np.mean( data[i - W : i + W +1] ) for i in range(W , len_data -W)]

    return averaged_data


# Definition :  return the metrics of metrics, that is to say, the average value
#               for a variable (mean latitude of the jet stream, mean jet speed,
#               and mean variability), for pre and for post indutrial periods.
# Input :   - data : yearly data averaged from daily dataset for example
#           - period : number of years in the period (default value = 30 years)
# Output :  - list : pre-average, pre-std, post-average, post-std
def metrics(data, period = 30) :

    mean_pre = np.mean(data[:period])
    sd_pre = np.std(data[:period]) / np.sqrt(period)

    mean_post = np.mean(data[-period:])
    sd_post = np.std(data[-period:]) / np.sqrt(period)

    return [mean_pre, sd_pre, mean_post, sd_post]

# Definition :  this function return the list of all daily latitude for the jet
#               stream, for pre and post industrial period, in seasonal list,
#               based on regional data.
# Input :   - data : regional daily data of the latitude for the jet stream
#           - period (30 years by default)
# Output :  - distrib list : 4 region * 4 season * 2 period
def distribution(data, period = 30):

    assert len(data) == 4, ('Size problem with data list in distribution')
    assert len(data[0])%365 == 0, ('time problem')



    distrib_data =[]

    for i in range(0,4):


        pre_winter, pre_summer, pre_spring, pre_autumn = [],[],[],[]
        post_winter, post_summer, post_spring, post_autumn = [],[],[],[]

        time_pre = 0

        time_post = len(data[0]) - 30*365

        for j in range(0, period):
            pre_spring += list(data[i][:,0][time_pre + 59 : time_pre + 151 ])
            pre_summer += list(data[i][:,0][time_pre + 151 : time_pre + 243 ])
            pre_autumn += list(data[i][:,0][time_pre + 243 : time_pre + 334 ])
            time_pre += 365

            post_spring += list(data[i][:,0][time_post + 59 : time_post + 151 ])
            post_summer += list(data[i][:,0][time_post + 151 : time_post + 243 ])
            post_autumn += list(data[i][:,0][time_post + 243 : time_post + 334 ])
            post_winter += list(data[i][:,0][time_post - 31 : time_post + 59])
            time_post += 365

        time_pre = 0

        pre_winter += list(data[i][:,0][time_pre : time_pre + 59 ])

        time_pre = 365

        pre_winter += list(data[i][:,0][time_pre - 31: time_pre ])

        for j in range(1,period):
            pre_winter += list(data[i][:,0][time_pre - 31: time_pre + 59])
            time_pre += 365

        distrib_data.append([[pre_summer, post_summer],[pre_autumn, post_autumn],[pre_winter,post_winter],[pre_spring,post_spring]])

    return distrib_data
