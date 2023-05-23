import sys
from datastorage import *

def timestamp_add(ts, du):
    _dt = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(milliseconds=(du/10)) #
    return time.mktime(_dt.timetuple())
     
def create_datastorage(dsname="dst", rawfiles=[]):
    
    # generate datastorage
    dstorage = DataStorage(filename=dsname)
     
    # set profile 
    #dstorage.setprofile(profile={'pid':0xBABA})
    #dstorage.setprofile(profile={'proto':0x0000}) 
    dstorage.setprofile(profile=datastorage_profile)
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


def fix_timestamp(dstorage):

    blkinfo = dstorage.d['datablock-info']

    _sts =  [ blkinfo.d['blt'][0]['chns'][0]['ts'], blkinfo.d['blt'][0]['chns'][1]['ts'] ]

    for blk in blkinfo.d['blt']:
        for i in range(2):
            oldst = blk['chns'][i]['ts']
            blk['chns'][i]['ts'] = _sts[i]
            _sts[i] = timestamp_add( _sts[i],  blk['chns'][i]['du'])
            newst =  blk['chns'][i]['ts']
            '''
            if i%2 ==0 :
                print("chn:{}, old-ts:{}({}), new-ts:{}({}), du:{}({}s)".format(i, oldst, datetime.datetime.fromtimestamp(oldst), newst, datetime.datetime.fromtimestamp(newst), blk['chns'][i]['du'], int(blk['chns'][i]['du']/10000)))
            '''
    blkinfo.save()


    
def check_blockinfo(dstorage):
    
    blki = dstorage.d['datablock-info']

    nob=blki.d['nob']
    blt=blki.d['blt'] 
    
    if nob != len(blt):
        print("nob error nob={}, blt len={}".format(nob, len(blt)))
        return

    # print(blt[0])

    last_sp = 0
    last_len = 0
    last_chn_ts = [0.0,0.0]
    last_chn_du = [0,0]

    # adress verify 
    for blk in blt:

        # the sp = last_sp + last_len 
        if last_len > 0:
            if blk['sp'] != (last_sp + last_len):
                print("failed to verify address at {}".format(blk))
                print("last sp {} and len {}")
                break

        last_sp = blk['sp']
        last_len = blk['len']

        chn0 = blk['chns'][0]
        chn1 = blk['chns'][1] 

        # chns address
        if not (chn0['sp'] == 0 and chn1['sp'] == chn0['len'] and blk['len'] == (chn0['len'] + chn1['len']) ):
            print("failed to verify chns address at blk {}".format(blk)) 
            break

         # chns ts and du, ts >= last_ts + last_du 
        if last_chn_du[0] > 0 :
            _ts = timestamp_add(last_chn_ts[0], last_chn_du[0])
            if chn0['ts'] < _ts:
                print("failed to verify chn0 ts at blk {}".format(blk)) 
                break

        #lts = datetime.datetime.fromtimestamp(last_chn_ts[0])
        #cts = datetime.datetime.fromtimestamp(chn0['ts'])
        #print("last chn0 ts: {}, du: {}s, cur ts: {}".format(lts, int(last_chn_du[0]/10000), cts))

        last_chn_ts[0] = chn0['ts']
        last_chn_du[0] = chn0['du']

        if last_chn_du[1] >0 :
            _ts = timestamp_add(last_chn_ts[1], last_chn_du[1])
            if chn1['ts'] < _ts:
                print("failed to verify chn0 ts at blk {}".format(blk)) 
                break

        last_chn_ts[1] = chn1['ts']
        last_chn_du[1] = chn1['du']

    print("verifying done")    
 
    
    
if __name__ == "__main__":
    
    arg = sys.argv[1:]
        
    if arg[0] == "--profile_0":
        from edsd import * 
        print("Generage data storage for profile 0")
     
    if arg[0] == "--profile_1":    
        from idsd import * 
        print("Generage data storage for profile 1")
     
    dstorage=create_datastorage(dsname=datastorage_name, rawfiles=rawfiles)

    fix_timestamp(dstorage=dstorage)
    
    check_blockinfo(dstorage=dstorage)

    print_dsinfo(dstorage=dstorage)
    
