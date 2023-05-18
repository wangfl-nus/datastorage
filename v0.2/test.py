from datastorage import *

def test_open_datastorage(filename='dst'):

    dstorage = DataStorage(filename=filename)

    # set profile 
    dstorage.setprofile(profile={'pid':0xBABA})
    dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.lockprofile()
 
    print(vars(dstorage))
    print(vars(dstorage.d['datastorage-info']))
    print(vars(dstorage.d['datablock-info']))

    return dstorage
    

def test_upload_1(dstorage):

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-01.txt")
    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)

    print(vars(dstorage))
    print(vars(dstorage.d['datastorage-info']))
    print(vars(dstorage.d['datablock-info']))

   # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-02.txt")
    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)

    print(vars(dstorage))
    print(vars(dstorage.d['datastorage-info']))
    print(vars(dstorage.d['datablock-info']))

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-03.txt")
    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)

    print(vars(dstorage))
    print(vars(dstorage.d['datastorage-info']))
    print(vars(dstorage.d['datablock-info']))

    print( "cb => {}".format(dstorage.d['cb']))
    
    dstorage.save()
    

def test_upload_2(dstorage):

    f_list = ["data\\icanbus\\00-01.txt", "data\\icanbus\\00-02.txt", "data\\icanbus\\00-03.txt", "data\\icanbus\\00-04.txt", "data\\icanbus\\00-05.txt"]
    
    for fn in f_list:
     
        # instanciat raw data
        rd = RawData(filename=fn)
        
        # upload raw data to the storage 
        dstorage.upload(rawdata=rd, size=30)
        dstorage.save()
        
    print(vars(dstorage))
    print(vars(dstorage.d['datastorage-info']))
    print(vars(dstorage.d['datablock-info']))

    #print( "cb => {}".format(dstorage.d['cb']))
    

def test_load(dstorage):
    
    #dstorage = DataStorage(filename='dst')

    print("Data Storage <dst> : \n{}\n".format(vars(dstorage)))
    print("Data Storage <dst> Info: \n{}\n".format(vars(dstorage.d['datastorage-info'])))
    print("Data Storage <dst> BlockInfo: \n{}\n".format(vars(dstorage.d['datablock-info'])))


    # makeup data
    def timestamp_add(ts, du):
        _dt = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(milliseconds=(du*1000)) #
        return time.mktime(_dt.timetuple())
 
    ts = 1684315290.0

    for blk in dstorage.d['datablock-info'].d['blt']:
        blk['chns'][0]['ts'] = ts
        ts = timestamp_add(ts, blk['chns'][0]['du'])
        #ts = blk['chns'][0]['ts']
        #print("{},  {}".format(ts, datetime.datetime.fromtimestamp(ts)))

    print(vars(dstorage.d['datablock-info']))

    bbb, bl = dstorage.load(chn=0, ts= 1684315446.0, du=2000000, oft='txt')
    print(bl)
    print("bbb:\n")
    print(bbb)
    print("bbb length: {}".format(len(bbb)))
