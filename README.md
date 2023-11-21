# TUH_statistics
Extraction of statistics regarding the TUH EEG corpus

TUH_statistics extracts the age/gender/channel names of the corpus whose path is given. 
Results contains files created on 14/11/2023 using version 2.0.0 of TUH dataset. Precisely, tuh_eeg V2.0.0, tuh_eeg_abnormal V3.0.0 and tuh_eeg_seizure V2.0.0.

TUSZ_stats.py extracts informations specifically from the seizure corpus. In addition to gathering the age/gender/channel, it reads the csv and csv files and populates the mne.raw objects with the corresponding annotations. There is an automatic channel discarding + re-referencing. Results are stored in piclke files for quicker analysis of the data. 
