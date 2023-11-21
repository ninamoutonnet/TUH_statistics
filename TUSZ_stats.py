import os
import glob 
import mne
import re
import pandas as pd
import pickle

from channel_clustering_TUH import channels_to_remove
from montage_TUSZ import cathode, anode, bipolar_ch_names 

def remove_unknown_channels(raw, channels_to_remove):
    return raw.drop_channels(ch_names = channels_to_remove, on_missing='ignore')  
   
def set_bipolar_tcp(raw, file_path):
    # find the montage from the name of the file
    if '/01_tcp_ar/' in file_path: 
        index = 0
    elif '/02_tcp_le/' in file_path: 
        index = 1
    elif '/03_tcp_ar_a/' in file_path: 
        index = 2
    elif '/04_tcp_le_a/' in file_path: 
        index = 3
    
    sample_anode = anode[index]
    sample_cathode = cathode[index]
    sample_bipolar_ch_names = bipolar_ch_names[index]
    
    raw = mne.set_bipolar_reference(raw, anode=sample_anode, cathode=sample_cathode, ch_name=sample_bipolar_ch_names, 
                                    verbose='WARNING')
    
    return raw

def parse_term_based_annotations_from_csv_bi_file(file_path):
    csv_bi_path = file_path.replace('.edf', '.csv_bi')
    csvbi_file = pd.read_csv(csv_bi_path, header=5)   
    # at the top of every file, there is a header that should not be read, example of header below
    ###########################################################
    # version = csv_v1.0.0
    # bname = aaaaaajy_s001_t000
    # duration = 1750.00 secs
    # montage_file = $NEDC_NFC/lib/nedc_eas_default_montage.txt
    #
    ###########################################################
    csvbi_file['duration'] =  csvbi_file.stop_time - csvbi_file.start_time
    csvbi_file['description'] = csvbi_file.label + ',' + csvbi_file.confidence.astype(str) + ',' +  'TERM'

    csvbi_annotations = mne.Annotations(onset = csvbi_file['start_time'].tolist(), 
                                        duration = csvbi_file['duration'].tolist(), 
                                        description = csvbi_file['description'].tolist())  
    return csvbi_annotations


def parse_term_based_annotations_from_csv_file(file_path): 
    csv_path = file_path.replace('.edf', '.csv')
    csv_file =  pd.read_csv(csv_path, header=5) 
    # at the top of every file, there is a header that should not be read, example of header below
    ###########################################################
    # version = csv_v1.0.0
    # bname = aaaaaajy_s001_t000
    # duration = 1750.00 secs
    # montage_file = $NEDC_NFC/lib/nedc_eas_default_montage.txt
    #
    ###########################################################
    
    csv_file['duration'] =  csv_file.stop_time - csv_file.start_time
    csv_file['description'] = csv_file.label + ',' + csv_file.confidence.astype(str) + ',' +  'EVENT'
    csv_file = csv_file.sort_values(by = ['start_time', 'stop_time'], axis = 0) 
    csv_file.reset_index(inplace=True, drop=True)

    onsets = []
    durations = []
    descriptions = []
    ch_names = []

    while len(csv_file) > 0:
        temp_dataframe = pd.DataFrame()
        temp_dataframe = pd.concat([temp_dataframe, csv_file.iloc[[0]]], ignore_index=True)
        csv_file.drop([0], inplace=True)

        # get the values and check they match 
        start_time = str(temp_dataframe['start_time'][0])
        duration = str(temp_dataframe['duration'][0])

        #iterate through rows looking for identical start time and duration
        for index, row in csv_file.iterrows():        
            if( (str(row['start_time'])==start_time) and (str(row['duration'])==duration)   ):
                # if you have found a match, add it to the temporary dataframe and remove it from the csv_file dataframe 
                temp_dataframe = pd.concat([temp_dataframe, csv_file.loc[[index]]], ignore_index=True)
                csv_file.drop([index], inplace=True)

        onsets.append(temp_dataframe['start_time'][0]) 
        durations.append(temp_dataframe['duration'][0])
        descriptions.append(temp_dataframe['description'][0])
        ch_names.append(temp_dataframe['channel'].tolist())
        csv_file.reset_index(drop=True, inplace=True)
    
    csv_annotations = mne.Annotations(onset = onsets, 
                                    duration = durations, 
                                    description = descriptions,
                                    ch_names=ch_names)  
    return csv_annotations


def main():
    TUH_EEG = ('/rds/general/user/nm2318/home/projects/scott_data_tuh/live/tuh_eeg_seizure/')
    file_paths = glob.glob(os.path.join(TUH_EEG, '**/*.edf'), recursive=True)
    channel_names = {}
    age_dict = {}
    sex_dict = {}
    raw_list = []

    debug = False 
    if (debug and len(file_paths)>5):
            file_paths = file_paths[0:5]


    for file_path in file_paths:
        # read EDF file
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose='WARNING')
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
            raw.info['subject_info']['age'] = age

        # populate the age dictionnary
        if age not in age_dict.keys():
            age_dict[age] = 1
        else: 
            age_dict[age] = age_dict[age] + 1

        # extract gender  
        found_gender = re.findall(r"\s([F|M])\s", patient_id)
        if len(found_gender) == 1:
            gender = found_gender[0]
            if gender == 'F':
                raw.info['subject_info']['sex'] = 2
            elif gender == 'M': 
                raw.info['subject_info']['sex'] = 1

        # populate the age dictionnary
        if gender not in sex_dict.keys():
            sex_dict[gender] = 1
        else: 
            sex_dict[gender] = sex_dict[gender] + 1

        # re-reference and get rid of useless channels
        raw = remove_unknown_channels(raw, channels_to_remove)
        raw = set_bipolar_tcp(raw, file_path)

        #extract the annotations from both csv and csv bi files
        annotation_csvbi = parse_term_based_annotations_from_csv_bi_file(file_path)
        annotation_csv = parse_term_based_annotations_from_csv_file(file_path)
        annotations = annotation_csvbi.append(onset=annotation_csv.onset, 
                                                     duration=annotation_csv.duration, 
                                                     description=annotation_csv.description,
                                                     ch_names=annotation_csv.ch_names)
        raw = raw.set_annotations(annotations, on_missing='warn')
        
        raw.info['subject_info']['path'] = file_path

        # populate the raw list
        raw_list.append(raw)
    
    # write the output to a pickle file: 
    with open('results/tuh_eeg_seizure__debug_true__raw_list.pickle', 'wb') as handle:
        pickle.dump(raw_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    with open('results/tuh_eeg_seizure__debug_true__ch_names.pickle', 'wb') as handle:
        pickle.dump(channel_names, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('results/tuh_eeg_seizure__debug_true__age_dict.pickle', 'wb') as handle:
        pickle.dump(age_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    with open('results/tuh_eeg_seizure__debug_true__sex_dict.pickle', 'wb') as handle:
        pickle.dump(sex_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

if __name__ == "__main__":
    main()
