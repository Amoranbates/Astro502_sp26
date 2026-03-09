# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:43:12 2026

@author: Aidan Moran-Bates
"""

from astropy.io import fits
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
from pykoa.koa import Koa 
import os
import time
import pandas as pd
import shutil

# !pip install pandas



# Import the Target List file and extract the hostnames for each star, which will be used to get the data for each star using Koa

filename = '/Users/astro502/Chemists/ASTR502_Master_Target_List.csv'


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



# Creates directory 'output',   once directory is created code will say directory already exists.
# This directory will be where the .tbl files for each star will be downloaded (these files hold the fits files)
try:
    os.mkdir('./output')
except:
    print(" Directory exists already", flush=True)


# Code goes through each star in the target list and extracts the KOA data for it.

for j in range(len(host_name_list)):
    star = host_name_list[j]
    # f-string is used to add the ./output/ and .tbl parts so that the KoA searching code can work properly.
    correct_name = star.replace(" ", "_")
    output = f"./output/{correct_name}.tbl"
    Koa.query_object ('hires', \
                  star, \
                  output, overwrite=True,)
    
    output_dir = f"dnload_dir_hires_calib1/{correct_name}"
    rec = Table.read (output, format='ascii.ipac')
    print (rec)
    Koa.download (output, \
        'ipac', \
        output_dir, \
        lev1file=1 )
    print(output_dir)


    directory_path_folder_str = f"{output_dir}/lev1/tbl"
    folder_paths_os = []

    # Code that will get the necessary level 1 files and delete everything else that was downloaded.
    try:
   
       for filename in os.listdir(directory_path_folder_str):
            full_folder_path = os.path.join(directory_path_folder_str, filename)
            # Changed from isfile to isdir
            if os.path.isdir(full_folder_path):
                folder_paths_os.append(full_folder_path.replace("\\", "/"))
   
        # For loop for ccd#
       for h in range(len(folder_paths_os)):
           directory_path_str = f"{folder_paths_os[h]}/flux"
   
       
           
           file_paths_os = []
            # for loop to get each flux.tbl.gz file for a ccd# folder
           for filename in os.listdir(directory_path_str):
               full_path = os.path.join(directory_path_str, filename)
               if os.path.isfile(full_path):
                   file_paths_os.append(full_path)
       
           
            # Limits used to only get files that have the target wavelengths.
           min_limit = [3930, 3960, 6560, 6700]
           
           max_limit = [3940, 3970, 6570, 6710]
   
           for i in range(len(file_paths_os)):
                filename = file_paths_os[i]
               
                df = pd.read_csv(filename, sep='\s+')
           
                wavelength_full = df.iloc[:,4]
               
                # For loop that takes gets the flux and hdr files into their star folder in CHEMISTS
                for f in range(len(min_limit)):
                    for k in range(len(wavelength_full)):
                       if wavelength_full[k] > min_limit[f] and wavelength_full[k] < max_limit[f]:
                           #print(file_paths_os[i])

                      

                          # # Fixes the path for the flux.tbl.gz file
                            source_path_tbl = file_paths_os[i].replace("\\", "/") 
    
                            # Gets just the flux file from the file path to be used later
                            just_the_flux_file = file_paths_os[i].replace(f"{directory_path_str}\\", "/")
                            # Starts transforming flux.tbl.gz path file to the path file for the hdr
                            source_path_change = source_path_tbl.replace("flux.tbl.gz", "hdr.txt.gz")
                            # Gets just the hdr file from the file path to be used later
                           
                            just_the_hdr_file = source_path_change.replace(f"{directory_path_str}", "")
                            # Fixes the path for the hdr file
                            source_path_hdr = source_path_change.replace("flux", "hdr")
                           
                            destination_path = f'Chemists/{correct_name}' 
    
                            # Ensure the destination directory exists (optional, but good practice)
                            
                            if not os.path.exists(destination_path):
                                 os.makedirs(destination_path)
    
                            # Move the file
                            # print(source_path_tbl)
                            # print(source_path_hdr)
                            # print(just_the_flux_file)
                            # print(just_the_hdr_file)
    
                           
                            # if os.path.exists(f'CHEMISTS/Qatar-4{just_the_flux_file}'):
                            #     os.remove(f'CHEMISTS/Qatar-4{just_the_flux_file}')
                            # if os.path.exists(f'CHEMISTS/Qatar-4{just_the_hdr_file}'):
                            #     os.remove(f'CHEMISTS/Qatar-4{just_the_hdr_file}')
    
                            try:
                                 shutil.move(source_path_tbl, destination_path)
                            except Exception as e:
                                print("Duplicate file issue")
                           
                           
    
    
                            try:
                                shutil.move(source_path_hdr, destination_path)
                            except Exception as e:
                                print("Duplicate file issue")
                                
    # Notifies that the code didn't go through any level 1 files for a star. (The star might not have had any level 1 files)
    except Exception as e:
        print("zzzzzz")

    print(correct_name)
    try:
        shutil.rmtree(f"dnload_dir_hires_calib1/{correct_name}")
    except Exception as e:
        print('FOLDER DOES NOT EXIST')
        
    
    #dnload_dir_hires_calib1/WASP-136
    
    # Says what number star was completed.
    print('Just completed star j =', j)
    
    
    
    