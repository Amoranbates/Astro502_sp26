from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
from pykoa.koa import Koa 
import os
import time
import pandas as pd




# Import the Target List file and extract the hostnames for each star, which will be used to get the data for each star using Koa

filename = 'C:/Users/Aidan Moran-Bates/Downloads/ASTR502_Master_Target_List.csv'


#### Checks to see if the Target List was imported successfully
#df = pd.read_csv(filename)
#print(df)

# Extracts the 2nd column of the Target List which has the host names for each star
df_column_2 = pd.read_csv(filename, usecols=[1])

# Checks to see if the host names were extracted successfully.
print(df_column_2)

print(df_column_2[:20])



# Turns the column of star host names into an array which
# will then be turned into a list that can be easily used in an iterable function

host_name_array = np.array(df_column_2)
host_name_list = [item[0] for item in host_name_array]

### Testing that an iterable function can access each part of the list.
# for i in range(len(host_name_list)):
#     dd = (host_name_list[i])
#     print((dd))


##  Iterable Function Works!!



# Creates directory 'output',   once directory is created code will say directory already exists.
# This directory will be where the .tbl files for each star will be downloaded (these files hold the fits files)
try:
    os.mkdir('./output')
except:
    print(" Directory exists already", flush=True)


# Full iterable function combining the code of the two cells above with the iterable function of "host_name_list".
# Code is deigned to get the .tbl file for each star and then extract the level 1 data from each .tbl file

# Variable that I will manually change whenever I take breaks from downloading star data so code doesn't start back from beginning
# Just completed star i = 16

# i = 0 was really long and I got some level 1 files for it so I decided to skip ahead.

progress_jump = 0 # If running code for first time this should be zero

for i in range(len(host_name_list)):
    j = i + progress_jump
    star = host_name_list[j]
    # f-string is used to add the ./output/ and .tbl parts so that the KoA searching code can work properly.
    output = f"./output/{host_name_list[j]}.tbl"
    output_file = output.replace(" ", "_")
    Koa.query_object ('hires', \
                  star, \
                  output_file, overwrite=True,)
    
    output_dir = f"dnload_dir_hires_calib1/{host_name_list[j]}"
    output_dir_no_space = output_dir.replace(" ", "_")
    rec = Table.read (output_file, format='ascii.ipac')
    print (rec)
    Koa.download (output_file, \
        'ipac', \
        output_dir_no_space, \
        lev1file=1 )
    # Lets me know how many stars I have gotten through 
    print('Just completed star i =', j)

#print(f"'{host_name_list[0]}'")

# for i in range(len(host_name_list)):
#     dd = (host_name_list[i])
#     bb = dd.replace(" ", "_")
#     cc = f''./output/
#     print(bb)