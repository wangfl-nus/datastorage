import os

'''
    Raw Data
        - representive of raw data
        - APIs to access the physical text-based raw data file  
'''
class RawData:
    def __init__(self, filename=None):
        self.filename = filename
        if self.filename is not None:
            with open(self.filename, 'r') as f:
                self.lines = f.readlines()   # lines
    
    def getRawData(self):
        return self.lines


'''
    DataSet
        - A group of data, with start time(date/time) and duration 
        - Subset of the whole data in the data storage
        - Used for data handling and analyzing and visulizing  
'''
class DataSet:
    def __init__(self, ds = None): 
        self.ds = None

    def getDataSet(self):
        return self.ds
  
'''
    DataStorage
        - Representive of physical data storage, either local file or remote database
        - APIs to upload raw data to the storage
        - APIs to access and parse data in the storage 
'''

def GetValueDict(o):
    return dict(o.__dict__)
 
def GetValueList(o):
    return list(o.__dict__.values())

def GetValueByteArray(o):
    return bytearray(list(o.__dict__.values())) 

#
# Data Storeage Header 
#
class DSHeader:
    def __init__(self, data = None, ver=0, pid=0, noc=2):
        if data is None:
            self.loh : int = 128 # length of data storage header  
            self.ver: int = ver  # version no, e.g 0x0001: 0.1, 0x0105:1.5
            self.pid: int = pid  # projec id
            self.noc: int = 2  # number of channcels, 
            # self.prot: tuple = ('JKE-INT-CAN-PROTO', 'JKE-INT-CAN-PROTO') # protocols of channel
            self.nob: int = 0  # number of data blocks
            self.lof: int = 8  # length of frame in bytes, e.g 8 (bytes)
            self.ldh: int = 64 # length of data block header, e.g 64 (bytes)
            self.dap: int = 0 # position of data (the first of data block)
        else:
            self.init_from_bytes(data=data)

    def to_bytes(self):
        
        ds_header = bytearray(self.loh.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.ver.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.pid.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.noc.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.nob.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.lof.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.ldh.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.dap.to_bytes(2, byteorder = 'big'))
                 
        # generate 128-byte header, defined in self.loh
        ds_header += bytearray(self.loh-len(ds_header))     
 
        return ds_header

    def init_from_bytes(self, data: bytearray = bytearray()):
        if (len(data) < 128):
            return 
        
        # initialize the variables from bytearray 'data' 
        ds_header = data
        
        self.loh = int.from_bytes(ds_header[:2], 'big')  # length of data storage header  
        self.ver = int.from_bytes(ds_header[2:4], 'big') # version no, e.g 0x0001: 0.1, 0x0105:1.5
        self.pid = int.from_bytes(ds_header[4:6], 'big') # projec id
        self.noc = int.from_bytes(ds_header[6:8], 'big') # number of channcels,  
        self.nob = int.from_bytes(ds_header[8:10], 'big') # number of data blocks
        self.lof = int.from_bytes(ds_header[10:12], 'big') # length of frame in bytes, e.g 8 (bytes)
        self.ldh = int.from_bytes(ds_header[12:14], 'big') # length of data block header, e.g 64 (bytes)
        self.dap = int.from_bytes(ds_header[14:16], 'big') # position of data (the first of data block)


#
# Channel info 
#   16 bytes 
# 
class CHInfo:
    def __init__(self):
        self.sp: int = 64 # offset of channel 0 data, = data block header length
        self.nof: int = 0 # number of frames
        self.du : int = 0 # duration in 0.1 ms (depending to the protocol), max duration < 3 days
        self.ts : int = 0 # timestamp of satrt  
    
    def to_bytes(self):
        
        ch_info = bytearray(self.sp.to_bytes(4, byteorder = 'big')) \
                + bytearray(self.nof.to_bytes(4, byteorder = 'big')) \
                + bytearray(self.du.to_bytes(4, byteorder = 'big')) \
                + bytearray(self.ts.to_bytes(4, byteorder = 'big')) 
        
        return ch_info
        
#
# Data Block Header 
#   64 bytes 
#  
class DBHeader:
    def __init__(self, lodh=64, noc=2): 
        
        self.lodh = lodh  # defined in DS Header lodh 
        self.noc  = noc  # defined in DS Header noc
        
        self.cp: int  = 0 # current pointer, position of this block
        self.fp: int  = 0 # backward pointer, position of the previous block 
        self.bp: int  = 0 # forward pointer, postition of the next block 
        self.info: int = 0 
        self.chns: list = []
 
    # add channel info
    def addch(self, ch: CHInfo):
        self.chns.append(ch)
    
    def to_bytes(self):
       
        db_header = bytearray(self.cp.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.fp.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.bp.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.info.to_bytes(2, byteorder = 'big')) \
        
        ch_info = bytearray()
        for ch in self.chns:
            ch_info += ch.to_bytes()
        
        db_header += bytearray(self.lodh-len(db_header)-len(ch_info))     
        db_header += ch_info
         
        return db_header
         
        
        
        
DS_VERSION = "0.1a"  
DSM_UNKNONW = 0
DSM_FILE = 1
DSM_DATABASE = 2
 
class DataStorage:
    def __init__(self, filename=None, dblink=None):
        self.version = DS_VERSION
        self.isAvailable = False
        self.profile = None
        self.profilelocked = False
        
        
        self.header = {}  # data storage header
        self.ds = []  
        
        #self._time = 0 
        #self.count = 0 
        
        if filename is not None:
            ## file mode
            self.mode =  DSM_FILE
            self.filename = filename 
            if os.path.isfile(self.filename) == True:
                self.isAvailable = True
                # TODO: - open the storage file
                #       - load profile
                #       - load data (default volume)

        elif dblink is not None:
            ## database mode
            self.mode =  DSM_DATABASE
            self.filename = filename
            # TODO: connect to database
            #       - load profile
            #       - load data (default volume)

        else:
            self.mode =  DSM_UNKNONW


    def setprofile(self, profile={}):
        
        if self.profilelocked == True:
            return
        
        ## TODO: validate the profile
        
        if self.profile is None:
            self.profile = profile
        else:
            # merge profiles
            self.profile.update(profile)
            
    def lockprofile(self):
        if self.profilelocked == False:
            self.profilelocked = True 
            for i in range(self.profile['noc']):
                #self.dp[f'chn{i}'] = []
                self.ds.append([])
    
    ''' flush/save new (uploaded) data to the storage '''
    def flush(self, zipped=False):
        
        if self.mode == DSM_FILE: 
            fn = f'{self.filename}.bin'
            with open(fn,"wb") as f: 
                
                bh = {}  # data block header 
                
                db_pos = self.header['datap'] # TODO: recalculate datablock position in __init__()
                ds_pos = db_pos + self.header['lodh']   
                
                # write data 
                f.seek(ds_pos, 0)
                for chn in range(self.profile['noc']):
                    cn = f'chn{chn}' 
                    bh[cn] = [f.tell(), len(self.ds[chn])] 
                    for d in self.ds[chn]:
                        f.write(d)
                
                # write block header
                f.seek(db_pos, 0) 
                dp_bytes = bytearray(json.dumps(bh).encode('utf-8'))
                f.write(dp_bytes)
                
                # TODO: write storage header 

    ''' Uplaod raw data to the storage '''    
    def upload(self, rawdata: RawData = None):
        
        lines = rawdata.getRawData() 
        chns = [*range(self.profile['noc'])]
        for line in lines:
            x = line.strip('\n').split(',') 
            rs = int(x[0], 16)
            chn = int(x[1], 16)
            finfo  = int(x[2], 16)
            fid    = int(x[3], 16)
            data   = [int(i,16) for i in x[4:]]

            #self._time += rs  
            info = bytearray([rs&0xff]) + bytearray(fid.to_bytes(4, byteorder = 'big')[1:]) 
            data = bytearray([int(i,16) for i in x[4:]]) 

            #self.count += 1 
            if chn in chns:
                self.ds[chn].append(info+data)

        #self.dp['chn0'] = [0, len(ds[0])]
        #self.dp['chn1'] = [0, len(ds[1])]
        #self.dp['daddr'] = 128
 
    ''' Retrive data from the storage '''    
    def retrieve(self, starttime = None, duration = None):
        # access data storage and generate corresponding dataset 
        pass
