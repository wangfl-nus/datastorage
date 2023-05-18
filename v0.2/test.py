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
    
    