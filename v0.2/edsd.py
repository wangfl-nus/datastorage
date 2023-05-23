
''' 
    data storage name

'''
datastorage_name = 'edst'


''' 
    date/time of data collection
    
    Remark: by default is the date/time of uploding data to the data storage
     
'''
data_collect_dt = ""


''' 
    data storage profile 
    
    Remark: JSON-formatted description of project id, protocol id ets 
    
    "pid": <>
    "proto": <>
       0x0000 -> 0x00: chn0 Internal Bus,  0x00: chn1 Internal Bus
       0x0100 -> 0x01: chn0 External Bus,  0x00: chn1 Internal Bus 
     ...
     
'''
datastorage_profile = {'pid':0xBABA, 'proto':0x0100}
  

''' 
    raw data files 

    Remark: file order must be compliant to chronological order

'''
 
rawfiles = [
    "data\\ecanbus\\11-34.txt",
    "data\\ecanbus\\11-35.txt",
    "data\\ecanbus\\11-36.txt",
    "data\\ecanbus\\11-37.txt",
    "data\\ecanbus\\11-38.txt",
    "data\\ecanbus\\11-39.txt",
    "data\\ecanbus\\11-40.txt",
    "data\\ecanbus\\11-41.txt",
    "data\\ecanbus\\11-42.txt",
    "data\\ecanbus\\11-43.txt",
    "data\\ecanbus\\11-44.txt",
    "data\\ecanbus\\11-45.txt",
    "data\\ecanbus\\11-46.txt",
    "data\\ecanbus\\11-47.txt",
    "data\\ecanbus\\11-48.txt",
    "data\\ecanbus\\11-49.txt",
    "data\\ecanbus\\11-50.txt",
    "data\\ecanbus\\11-51.txt",
    "data\\ecanbus\\11-52.txt"
]

