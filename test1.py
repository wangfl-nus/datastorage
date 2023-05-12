from datastorage import *

def test_1():
    # create new data storage 
    dstorage = DataStorage(filename="dst") 

    # set profile 
    dstorage.setprofile(profile={'pid':0xBABA})
    dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.lockprofile()

    dstorage.settimestamp()

    print(vars(dstorage)) 
    print(vars(dstorage.dsheader))
    print(vars(dstorage.dbh))
    print(vars(dstorage.dbh.chns[0]))
    print(vars(dstorage.dbh.chns[1]))

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-01.txt")

    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)

    print(vars(dstorage))
    print(vars(dstorage.dbh))
    print(vars(dstorage.dbh.chns[0]))
    print(vars(dstorage.dbh.chns[1]))

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-02.txt")

    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)
    print(vars(dstorage))
    print(vars(dstorage.dbh))
    print(vars(dstorage.dbh.chns[0]))
    print(vars(dstorage.dbh.chns[1]))

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-03.txt")

    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)
    print(vars(dstorage))
    print(vars(dstorage.dbh))
    print(vars(dstorage.dbh.chns[0]))
    print(vars(dstorage.dbh.chns[1]))

    # instanciat raw data
    rd = RawData(filename="data\\icanbus\\00-04.txt")

    # upload raw data to the storage 
    dstorage.upload(rawdata=rd, size=10)
    print(vars(dstorage))
    print(vars(dstorage.dbh))
    print(vars(dstorage.dbh.chns[0]))
    print(vars(dstorage.dbh.chns[1]))

    dstorage.flush()
    
def test_2():
    dstorage = DataStorage(filename="dst1") 

    # set profile 
    dstorage.setprofile(profile={'pid':0xCDCD})
    dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.lockprofile()

    # set timestamp
    dstorage.settimestamp()

    rd = RawData(filename="data\\icanbus\\00-01.txt")

    # upload raw data to the storage 
    dstorage.upload(rawdata=rd)
    dstorage.flush()


def test_3():
    dstorage = DataStorage(filename="dst2")

    # set profile 
    dstorage.setprofile(profile={'pid':0x8686})
    dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.lockprofile()

    dstorage.settimestamp()


    fl = ["data\\icanbus\\00-01.txt", "data\\icanbus\\00-02.txt", "data\\icanbus\\00-03.txt"]

    for f in fl:
        rd = RawData(filename=f) 
        dstorage.upload(rawdata=rd)

    dstorage.flush()
