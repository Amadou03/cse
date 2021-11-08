import src.processes as prc
from math import sqrt
import pandas as pd
import os
#import openpyxl
from datetime import datetime


        #Environmental Inputs


#we define directory path for faster path indexing
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_data=dir_path+"/data"
dir_condit=dir_data+"/conditions"

# we transform the input data into dataframe
df=pd.read_csv(dir_condit+'/33013.csv')
current_date_time = datetime.now()

#df.to_excel("%soutput.xlsx"%current_date_time)

#we remove colums we don't need
df.drop({"daily_rain_source","max_temp_source",	"min_temp_source", "vp_source", "evap_pan_source", "evap_syn_source",	"evap_comb"}, inplace=True, axis=1)

#we create mean temperature column and calculate its values from 'max temperature' and 'min temperature'
df["mean_temp"]=(df["max_temp"]+df["min_temp"])/2
df=df[["station",	"YYYY-MM-DD",	"daily_rain",	"max_temp",	"min_temp",	"mean_temp",
       "evap_pan",	"evap_syn",	"evap_comb_source",	"radiation",	"radiation_source",	"rh_tmax",	"rh_tmax_source",
       "rh_tmin",	"rh_tmin_source",	"et_short_crop",	"et_short_crop_source",	"et_tall_crop",	"et_tall_crop_source",
       "et_morton_wet",  "et_morton_wet_source",	"metadata"]]

#df.to_excel("%s.xlsx"%current_date_time)

#we locate columns of interest
daily_rain_loc=df.columns.get_loc('daily_rain')
mean_temp_loc=df.columns.get_loc('mean_temp')
evap_pan_loc=df.columns.get_loc("evap_pan")
radiation_loc=df.columns.get_loc('radiation')

#we create a new data set of weekly value for the columns of interest
data_set = {"daily_rain": [], "mean_temp": [], "evap_pan":[], "radiation":[]}

i=0
j=7
while j< (len(df)+7):

    data_set["daily_rain"].append(df.iloc[i:j,daily_rain_loc].mean())
    data_set["mean_temp"].append(df.iloc[i:j,mean_temp_loc].mean())
    data_set["evap_pan"].append(df.iloc[i:j, evap_pan_loc].mean())
    data_set["radiation"].append(df.iloc[i:j, radiation_loc].mean())

    i+=7
    j+=7
    #end while

data_set=pd.DataFrame(data_set)
#print(data_set)



    #temperature sets


#we locate columns of interests
daily_rain_loc=data_set.columns.get_loc('daily_rain')
mean_temp_loc=data_set.columns.get_loc('mean_temp')
evap_pan_loc=data_set.columns.get_loc("evap_pan")
radiation_loc=data_set.columns.get_loc('radiation')

i=0
week=0
heat_sum=0
while heat_sum <= 16.7:

    # T='temperature values'
    T=data_set.iloc[i,mean_temp_loc]
    heat_sum=heat_sum+sqrt(T-16)
    week+=1
    i+=1

    #end while

print(week)
print(data_set)
lai=0.5
stem=7
petiole=5
lamina=20
tuber=0
planting_piece=37
total_dry_matter=69
SI=0

#   MAIN LOOP

while week<=52:
    #Defining Variable Values
    #Let's calculate LAI on a weekly basis. (We need to consider the option of calculating it on a daily basis

    T = data_set.iloc[week, mean_temp_loc]
    lai=prc.leaf_area_index(lai,lamina,T)

    #we calculate crop growth rate
    #we initialize solar radiation sr first
    sr=data_set.iloc[week,radiation_loc]
    pcgr,cgr=prc.cgr(T,sr,lai,SI)
    print(pcgr,cgr)
    week+=1
