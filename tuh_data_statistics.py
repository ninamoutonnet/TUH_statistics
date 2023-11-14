'''

THIS SCRIPT IS USED TO EXTRACT INFORMATION FROM THE TUH DATA CORPUS. 
THE RAW EDF FILES ARE AUTOMATICALLY LOADED, BUT NOT THE TIME SERIES THEMSELVES, SO AS TO SAVE MEMORY.
THEN, THE RAW.INFO ATTRIBUTE IS USED TO EXAMINE WHAT CHANNEL NAMES ARE PRESENT IN THE CORPUS, AND AT WHAT FREQUENCY.

AGE AND SEX ARE EXTRACTED FROM THE EDF HEADER.

'''

import os
import glob 
import mne
import re

TUH_EEG = ('/rds/general/user/nm2318/home/projects/scott_data_tuh/live/tuh_eeg')
file_paths = glob.glob(os.path.join(TUH_EEG, '**/*.edf'), recursive=True)
channel_names = {}
age_dict = {}
sex_dict = {}

debug = False 
if (debug and len(file_paths)>50):
        file_paths = file_paths[0:5]


for file_path in file_paths:
    
    # read EDF file
    raw = mne.io.read_raw_edf(file_path, preload=False, verbose='WARNING')
    for chname in raw.info['ch_names']:
        if chname not in channel_names.keys():
            channel_names[chname] = 1
        else: 
            channel_names[chname] = channel_names[chname] + 1
            
    # Read header file, extract age and sex from it
    f = open(file_path, "rb")
    header = f.read(88)
    f.close()
    # bytes 8 to 88 contain ascii local patient identification
    # see https://www.teuniz.net/edfbrowser/edf%20format%20description.html
    patient_id = header[8:].decode("ascii")
    
    # extract age
    found_age = re.findall(r"Age:(\d+)", patient_id)
    if len(found_age) == 1:
        age = int(found_age[0])
    # populate the age dictionnary
    if age not in age_dict.keys():
        age_dict[age] = 1
    else: 
        age_dict[age] = age_dict[age] + 1
    
    # extract gender  
    found_gender = re.findall(r"\s([F|M])\s", patient_id)
    if len(found_gender) == 1:
        gender = found_gender[0]
    # populate the age dictionnary
    if gender not in sex_dict.keys():
        sex_dict[gender] = 1
    else: 
        sex_dict[gender] = sex_dict[gender] + 1
        
print('#################################################################################################')
print('EEG_channels present in: ', TUH_EEG)
print(channel_names)
print()
print()
print('Sex: ')
print(sex_dict)
print()
print()
print('Age: ')
print(age_dict)
print()
print('Number of files: ', len(file_paths))
print('#################################################################################################')
