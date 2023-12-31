############################################################################################################################
# This files contains an exhaustive list of the channel names present in the TUH EEG corpus. This is extracted using the appendix of the following document https://isip.piconepress.com/publications/reports/2020/tuh_eeg/electrodes/, and it is done on November 16th 2023. 
############################################################################################################################


############################################################################################################################
# CHANNELS TO REMOVE

unknown = ['BURSTS','EEG PG1-LE','EEG PG1-REF','EEG PG2-LE','EEG PG2-REF','EEG RLC-LE','EEG RLC-REF','EEG ROC-REF','EEG LOC-REF','EEG LUC-LE','EEG LUC-REF','SUPPR','EEG C3P-REF','EEG C4P-REF']

DC_voltage = ['DC1-DC','DC2-DC','DC3-DC','DC4-DC','DC5-DC','DC6-DC','DC7-DC','DC8-DC']

no_signal = ['EEG 100-REF','EEG 101-REF','EEG 102-REF','EEG 103-REF','EEG 104-REF','EEG 105-REF','EEG 106-REF','EEG 107-REF','EEG 108-REF','EEG 109-REF','EEG 110-REF','EEG 111-REF','EEG 112-REF','EEG 113-REF','EEG 114-REF','EEG 115-REF','EEG 116-REF','EEG 117-REF','EEG 118-REF','EEG 119-REF','EEG 120-REF','EEG 121-REF','EEG 122-REF','EEG 123-REF','EEG 124-REF','EEG 125-REF','EEG 126-REF','EEG 127-REF','EEG 128-REF','EEG 33-REF','EEG 34-REF','EEG 35-REF','EEG 36-REF','EEG 37-REF','EEG 38-REF','EEG 39-REF','EEG 40-REF','EEG 41-REF','EEG 42-REF','EEG 43-REF','EEG 44-REF','EEG 45-REF','EEG 46-REF','EEG 47-REF','EEG 48-REF','EEG 49-REF','EEG 50-REF','EEG 51-REF','EEG 52-REF','EEG 53-REF','EEG 54-REF','EEG 55-REF','EEG 56-REF','EEG 57-REF','EEG 58-REF','EEG 59-REF','EEG 60-REF','EEG 61-REF','EEG 62-REF','EEG 63-REF','EEG 64-REF','EEG 65-REF','EEG 66-REF','EEG 67-REF','EEG 68-REF','EEG 69-REF','EEG 70-REF','EEG 71-REF','EEG 72-REF','EEG 73-REF','EEG 74-REF','EEG 75-REF','EEG 76-REF','EEG 77-REF','EEG 78-REF','EEG 79-REF','EEG 80-REF','EEG 81-REF','EEG 82-REF','EEG 83-REF','EEG 84-REF','EEG 85-REF','EEG 86-REF','EEG 87-REF','EEG 88-REF','EEG 89-REF','EEG 90-REF','EEG 91-REF','EEG 92-REF','EEG 93-REF','EEG 94-REF','EEG 95-REF','EEG 96-REF','EEG 97-REF','EEG 98-REF','EEG 99-REF']

custom_placement = ['EEG 1X10_LAT_01-','EEG 1X10_LAT_02-','EEG 1X10_LAT_03-','EEG 1X10_LAT_04-','EEG 1X10_LAT_05-','EEG 20-LE','EEG 20-REF','EEG 21-LE','EEG 21-REF','EEG 22-LE','EEG 22-REF','EEG 23-LE','EEG 23-REF','EEG 24-LE','EEG 24-REF','EEG 25-LE','EEG 25-REF','EEG 26-LE','EEG 26-REF','EEG 27-LE','EEG 27-REF','EEG 28-LE','EEG 28-REF','EEG 29-LE','EEG 29-REF','EEG 30-LE','EEG 30-REF','EEG 31-LE','EEG 31-REF','EEG 32-LE','EEG 32-REF','EEG X1-REF']

channels_to_remove = unknown + DC_voltage + no_signal + custom_placement


############################################################################################################################
# NON_EEG CHANNELS 

non_eeg = ['ECG EKG-REF','EDF ANNOTATIONS','EMG-REF','IBI','PHOTIC PH','PHOTIC-REF','PULSE RATE','RESP ABDOMEN-REF','EEG RESP1-REF','EEG RESP2-REF','EEG EKG1-REF','EEG EKG-LE','EEG EKG-REF']

############################################################################################################################
# EEG CHANNELS 

le_references = ['EEG A1-LE','EEG A2-LE','EEG C3-LE','EEG C4-LE','EEG CZ-LE','EEG F3-LE','EEG F4-LE','EEG F7-LE','EEG F8-LE','EEG FP1-LE','EEG FP2-LE','EEG FZ-LE','EEG O1-LEvEEG O2-LE','EEG OZ-LE','EEG P3-LE','EEG P4-LE','EEG PZ-LE','EEG SP1-LE','EEG SP2-LE','EEG T1-LE','EEG T2-LE','EEG T3-LE','EEG T4-LE','EEG T5-LE','EEG T6-LE']

ar_references = ['EEG A1-REF','EEG A2-REF','EEG C3-REF','EEG C4-REF','EEG CZ-REF','EEG F3-REF','EEG F4-REF','EEG F7-REF','EEG F8-REF','EEG FP1-REF','EEG FP2-REF','EEG FZ-REF','EEG O1-REF','EEG O2-REF','EEG OZ-REF','EEG P3-REF','EEG P4-REF','EEG PZ-REF','EEG SP1-REF','EEG SP2-REF','EEG T1-REF','EEG T2-REF','EEG T3-REF','EEG T4-REF','EEG T5-REF','EEG T6-REF']

bipolar = ['EEG C3-P3','EEG C3-T3','EEG C4-CZ','EEG C4-P4','EEG CZ-C3','EEG CZ-PZ','EEG F3-C3','EEG F4-C4','EEG F7-T3','EEG F8-T4','EEG FP1-F7','EEG FP2-F8','EEG FZ-CZ','EEG T1-T2','EEG T2-T4','EEG T3-T1','EEG T3-T5','EEG T4-C4','EEG T4-T6','EEG T5-O1','EEG T6-O2']
