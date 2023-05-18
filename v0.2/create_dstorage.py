''' 
 
 Generage Data Storage

'''
 
# raw data files
rawfiles = [
    "data\\icanbus\\00-01.txt",
    "data\\icanbus\\00-02.txt",
    "data\\icanbus\\00-03.txt",
    "data\\icanbus\\00-04.txt",
    "data\\icanbus\\00-05.txt",
    "data\\icanbus\\00-06.txt",
    "data\\icanbus\\00-07.txt",
    "data\\icanbus\\00-08.txt",
    "data\\icanbus\\00-09.txt",
    "data\\icanbus\\00-10.txt",
    "data\\icanbus\\00-11.txt",
    "data\\icanbus\\00-12.txt",
    "data\\icanbus\\00-13.txt",
    "data\\icanbus\\00-14.txt",
    "data\\icanbus\\00-15.txt",
    "data\\icanbus\\00-16.txt",
    "data\\icanbus\\00-17.txt",
    "data\\icanbus\\00-18.txt",
    "data\\icanbus\\00-19.txt",
    "data\\icanbus\\00-20.txt",
    "data\\icanbus\\00-21.txt",
    "data\\icanbus\\00-22.txt",
    "data\\icanbus\\00-23.txt",
    "data\\icanbus\\00-24.txt",
    "data\\icanbus\\00-25.txt",
    "data\\icanbus\\00-26.txt",
    "data\\icanbus\\00-27.txt",
    "data\\icanbus\\00-28.txt",
    "data\\icanbus\\00-29.txt",
    "data\\icanbus\\00-30.txt",
    "data\\icanbus\\00-31.txt",
    "data\\icanbus\\00-32.txt",
    "data\\icanbus\\00-33.txt",
    "data\\icanbus\\00-34.txt",
    "data\\icanbus\\00-35.txt",
    "data\\icanbus\\00-36.txt",
    "data\\icanbus\\00-37.txt",
    "data\\icanbus\\00-38.txt",
    "data\\icanbus\\00-39.txt",
    "data\\icanbus\\00-40.txt",
    "data\\icanbus\\00-41.txt",
    "data\\icanbus\\00-42.txt",
    "data\\icanbus\\00-43.txt",
    "data\\icanbus\\00-44.txt",
    "data\\icanbus\\00-45.txt",
    "data\\icanbus\\00-46.txt",
    "data\\icanbus\\00-47.txt",
    "data\\icanbus\\00-48.txt",
    "data\\icanbus\\00-49.txt",
    "data\\icanbus\\00-50.txt",
    "data\\icanbus\\00-51.txt",
    "data\\icanbus\\00-52.txt",
    "data\\icanbus\\00-53.txt",
    "data\\icanbus\\00-54.txt",
    "data\\icanbus\\00-55.txt",
    "data\\icanbus\\00-56.txt",
    "data\\icanbus\\00-57.txt",
    "data\\icanbus\\00-58.txt",
    "data\\icanbus\\00-59.txt",
    "data\\icanbus\\01-00.txt",
    "data\\icanbus\\01-01.txt",
    "data\\icanbus\\01-02.txt",
    "data\\icanbus\\01-03.txt",
    "data\\icanbus\\01-04.txt",
    "data\\icanbus\\01-05.txt",
    "data\\icanbus\\01-06.txt",
    "data\\icanbus\\01-07.txt",
    "data\\icanbus\\01-08.txt",
    "data\\icanbus\\01-09.txt",
    "data\\icanbus\\01-10.txt",
    "data\\icanbus\\01-11.txt",
    "data\\icanbus\\01-12.txt",
    "data\\icanbus\\01-13.txt",
    "data\\icanbus\\01-14.txt",
    "data\\icanbus\\01-15.txt",
    "data\\icanbus\\01-16.txt",
    "data\\icanbus\\01-17.txt",
    "data\\icanbus\\01-18.txt",
    "data\\icanbus\\01-19.txt",
    "data\\icanbus\\01-20.txt",
    "data\\icanbus\\01-21.txt",
    "data\\icanbus\\01-22.txt",
    "data\\icanbus\\01-23.txt",
    "data\\icanbus\\01-24.txt",
    "data\\icanbus\\01-25.txt",
    "data\\icanbus\\01-26.txt",
    "data\\icanbus\\01-27.txt",
    "data\\icanbus\\01-28.txt",
    "data\\icanbus\\01-29.txt",
    "data\\icanbus\\01-30.txt",
    "data\\icanbus\\01-31.txt",
    "data\\icanbus\\01-32.txt",
    "data\\icanbus\\01-33.txt",
    "data\\icanbus\\01-34.txt",
    "data\\icanbus\\01-35.txt",
    "data\\icanbus\\01-36.txt",
    "data\\icanbus\\01-37.txt",
    "data\\icanbus\\01-38.txt",
    "data\\icanbus\\01-39.txt",
    "data\\icanbus\\01-40.txt",
    "data\\icanbus\\01-41.txt",
    "data\\icanbus\\01-42.txt",
    "data\\icanbus\\01-43.txt",
    "data\\icanbus\\01-44.txt",
    "data\\icanbus\\01-45.txt",
    "data\\icanbus\\01-46.txt",
    "data\\icanbus\\01-47.txt",
    "data\\icanbus\\01-48.txt",
    "data\\icanbus\\01-49.txt",
    "data\\icanbus\\01-50.txt",
    "data\\icanbus\\01-51.txt",
    "data\\icanbus\\01-52.txt",
    "data\\icanbus\\01-53.txt",
    "data\\icanbus\\01-54.txt",
    "data\\icanbus\\01-55.txt",
    "data\\icanbus\\01-56.txt",
    "data\\icanbus\\01-57.txt",
    "data\\icanbus\\01-58.txt",
    "data\\icanbus\\01-59.txt"
]


# data storage name
datastorage_name = 'dst'
 
from datastorage import *

def timestamp_add(ts, du):
    _dt = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(milliseconds=(du/10)) #
    return time.mktime(_dt.timetuple())
 
def create_datastorage(dsname="dst", rawfiles=[]):
    
    # generate datastorage
    dstorage = DataStorage(filename=dsname)
     
    # set profile 
    dstorage.setprofile(profile={'pid':0xBABA})
    dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.lockprofile()
          
    # upload data from raw files
    for fn in rawfiles:
        
        # instanciat raw data
        rd = RawData(filename=fn)
        
        # upload raw data to the storage 
        dstorage.upload(rawdata=rd)
        
        # save data 
        dstorage.save()
        
        # update _ts with the latest duration
        _du = dstorage.d['datablock-info'].d['blt']
         
    
    return dstorage
 
def print_dsinfo(dstorage):
    print("datastorage: {}".format(vars(dstorage)))
    print("datastorage info: {}".format(vars(dstorage.d["datastorage-info"])))
    print("datasblock info:  {}".format(vars(dstorage.d["datablock-info"])))
      
# makeup data


def fix_timestamp(dstorage)

    blkinfo = dstorage.d['datablock-info']

    _sts =  [ blkinfo.d['blt'][0]['chns'][0]['ts'], blkinfo.d['blt'][0]['chns'][1]['ts'] ]

    for blk in blkinfo.d['blt']:
        for i in range(2):
            oldst = blk['chns'][i]['ts']
            blk['chns'][i]['ts'] = _sts[i]
            _sts[i] = timestamp_add( _sts[i],  blk['chns'][i]['du'])
            newst =  blk['chns'][i]['ts']
            if i%2 ==0 :
                print("chn:{}, old-ts:{}({}), new-ts:{}({}), du:{}({}s)".format(i, oldst, datetime.datetime.fromtimestamp(oldst), newst, datetime.datetime.fromtimestamp(newst), blk['chns'][i]['du'], int(blk['chns'][i]['du']/10000)))
    
    blkinfo.save()
 
 if __name__ == "__main__":
    
    dstorage=create_datastorage(dsname=datastorage_name, rawfiles=rawfiles)

    fix_timestamp(dstorage=dstorage)

    print_dsinfo(dstorage=dstorage)
    
