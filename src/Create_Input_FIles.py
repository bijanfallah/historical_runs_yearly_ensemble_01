'''
This is the Program to create the INPUT files for the IO Program

Step 1 :  create the f (difference between background and the observation):
d=y^o - Hx^b

Step 2 : calculate the error variance of the observations divided by the
error variance of the background field

'''

#Step 1:
flag1=True
NN=200      #number of observations
COR_LEN=2   #correlation length
N=30        #number of influential points
import pandas as pd
from make_pseudo_obs import extract_pseudo
Obs = pd.read_csv('Stations_DATA.csv')
Obs.columns=['lon','lat','Vals','Vals_dirty','Time']
if flag1==True :
    NN=200
    First_Guess_dirty, First_Guess, rlon_s, rlat_s, t_o , rlon_o, rlat_o=extract_pseudo(NN,
                                                                                dir='/work/bb0962/work3/member04_relax_3_big/post/',
                                                                                name='member04_relax_3_T_2M_ts_monmean_1995.nc',
                                                                                var='T_2M')
    import csv
    from itertools import izip
    from itertools import repeat
    with open('First_Guess_DATA.csv', 'wb') as f:
        writer = csv.writer(f)
        for i in range(0,12):
            writer.writerows(izip(rlon_s,rlat_s,First_Guess[:,i],First_Guess_dirty[:,i],list(repeat(i,NN))))



import pandas as pd
FG = pd.read_csv('First_Guess_DATA.csv')
FG.columns=['lon','lat','Vals','Vals_dirty','Time']
#### STEP  1

f = Obs - Obs
f.Vals = Obs.Vals_dirty - FG.Vals
f.lon = Obs.lon
f.lat = Obs.lat
f.Time = Obs.Time

#### Step  2

import numpy as np
Vari    =   np.zeros(12)
for i in range(0,12):
    ER_Obs  =   Obs.Vals_dirty[Obs.Time==i] - Obs.Vals[Obs.Time==i]
    ER_BK   =   FG.Vals[Obs.Time==i]        - Obs.Vals[Obs.Time==i]
    Vari[i]    =    np.var(ER_Obs)/np.var(ER_BK)


## Step 3 write the INPUT files:
# write the x,y,f,var to the INPUT file

import csv
from itertools import izip
from itertools import repeat
with open('INPUT.csv', 'wb') as ff:
    writer = csv.writer(ff)
    for i in range(0,12):
        writer.writerows(izip(f.lon[f.Time==i],f.lat[f.Time==i],f.Vals[f.Time==i]
                              ,f.Time[f.Time==i],list(repeat(Vari[i],NN))))

# Write the grids for forecast domain :

xv, yv = np.meshgrid(rlon_o, rlat_o, sparse=False, indexing='ij')
leng=rlon_o.__len__()*rlat_o.__len__()
lons=xv.reshape(leng,1)
lats=yv.reshape(leng,1)

with open('GRIDS.csv', 'wb') as gr:
    writer = csv.writer(gr)
    for i in range(0,leng):
        writer.writerows(izip(lons[i],lats[i]))


## TODO : 1- Write the octave code to read the GRIDS.csv and INPUT.csv and run the IO and write the OUT.csv
## TODO : 2- write the pythom code to add the OUT to the BForecast and write the Analysis NETCDF file
## TODO : 3- Plot the RMSE of this new analysis and the "TRUE" simulation

