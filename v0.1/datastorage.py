from enum import Enum
import datetime, time
import struct
import os 



def test_fread(cp, len):
    with open("dst.bin", 'rb') as f:
        f.seek(cp,0)
        return f.read(len)
 

''' 
    protocol identifiers
    (to be declared in project property)
'''  
class Comm_Protocol(Enum):
    PSA_EXT_CAN_PROTO = 0
    JKE_INT_CAN_PROTO = 1


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
            self.proto: int = 0x0000 # protocols of channel, byte-0 for chn0, and byte-1 for chn1 
            self.nob: int = 0  # number of data blocks
            self.lof: int = 12  # length of per frame in bytes, e.g 12 (bytes) incl. fid, time 
            self.ldh: int = 64 # length of data block header, e.g 64 (bytes)
            self.dap: int = self.loh  # position of data (the first of data block)
            self.cdap: int = self.loh  # position of new data block (to write new data here) 
            
        else:
            self.init_from_bytes(data=data)

    def to_bytes(self):
        
        ds_header = bytearray(self.loh.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.ver.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.pid.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.noc.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.proto.to_bytes(4, byteorder = 'big')) \
                  + bytearray(self.nob.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.lof.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.ldh.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.dap.to_bytes(2, byteorder = 'big')) \
                  + bytearray(self.cdap.to_bytes(2, byteorder = 'big'))
                 
                 
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
        self.proto = int.from_bytes(ds_header[8:12], 'big') 
        self.nob = int.from_bytes(ds_header[12:14], 'big') # number of data blocks
        self.lof = int.from_bytes(ds_header[14:16], 'big') # length of frame in bytes, e.g 8 (bytes)
        self.ldh = int.from_bytes(ds_header[16:18], 'big') # length of data block header, e.g 64 (bytes)
        self.dap = int.from_bytes(ds_header[18:20], 'big') # position of data (the first of data block)
        self.cdap = int.from_bytes(ds_header[20:22], 'big') 


#
# Channel info 
#   16 bytes 
# 
class CHInfo:
    chinfo_size = 16 # class variable to declare the size of CHInfo 
    def __init__(self, data=None):
        if data is None:
            self.sp: int = 64 # offset of channel 0 data, = data block header length
            self.nof: int = 0 # number of frames
            self.du : int = 0 # duration in 0.1 ms (depending to the protocol), max duration < 3 days
            self.ts : int = 0 # timestamp of start  
        else:
            self.init_from_bytes(data=data)

    def to_bytes(self):
        
        ch_info = bytearray(self.sp.to_bytes(4, byteorder = 'big')) \
                + bytearray(self.nof.to_bytes(4, byteorder = 'big')) \
                + bytearray(self.du.to_bytes(4, byteorder = 'big')) \
                + bytearray(struct.pack("f", self.ts)) #  (self.ts.to_bytes(4, byteorder = 'big')) 
        
        return ch_info
    
    def init_from_bytes(self, data: bytearray = bytearray()):
        if (len(data) < 16):
            #print("len = {}".format(len(data)))
            #print(data)
            return 
        
        ch_info = data
        self.sp = int.from_bytes(ch_info[:4], 'big')
        self.nof = int.from_bytes(ch_info[4:8], 'big')
        self.du = int.from_bytes(ch_info[8:12], 'big')
        self.ts = struct.unpack("f", ch_info[12:16])[0]   # int.from_bytes(ch_info[12:], 'big')
        
#
# Data Block Header 
#   64 bytes 
#  
class DBHeader:
    def __init__(self, ldh=64, noc=2, data=None): 
        
        self.ldh = ldh  # defined in DS Header ldh 
        self.noc  = noc  # defined in DS Header noc
        
        self.cp: int  = 0 # current pointer, position of this block
        self.pp: int  = 0 # backward pointer, position of the previous block 
        self.np: int  = 0 # forward pointer, postition of the next block 
        self.info: int = 0 
        self.chns: list = []
         
        if data is not None: 
            self.init_from_bytes(data=data)

    # add channel info
    def addch(self, ch: CHInfo):
        self.chns.append(ch)
    
    def to_bytes(self):
       
        db_header = bytearray(self.cp.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.pp.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.np.to_bytes(8, byteorder = 'big')) \
                  + bytearray(self.info.to_bytes(2, byteorder = 'big')) \
        
        ch_info = bytearray()
        for ch in self.chns:
            ch_info += ch.to_bytes()
        
        db_header += bytearray(self.ldh-len(db_header)-len(ch_info))     
        db_header += ch_info
         
        return db_header
         
    def init_from_bytes(self, data: bytearray = bytearray()):
        if (len(data) < self.ldh):
            return 
      
        db_header = data
        
        self.cp = int.from_bytes(db_header[0:8], 'big')
        self.pp = int.from_bytes(db_header[8:16], 'big')
        self.np = int.from_bytes(db_header[16:24], 'big')
        self.info = int.from_bytes(db_header[24:26], 'big')
        
        chinfo_startbyte = self.ldh - (2*CHInfo.chinfo_size)  # skip reserverd bytes,  
        
        for i in range(self.noc):
            chinfo_startbyte += (i*CHInfo.chinfo_size)
            ch_info = db_header[chinfo_startbyte: chinfo_startbyte+CHInfo.chinfo_size] # CHInfo 16-byte
            self.chns.append(CHInfo(data=ch_info))
         
    
DS_VERSION = 0x0001  # v0.1 

DSM_UNKNONW = 0
DSM_FILE = 1
DSM_DATABASE = 2

DEFAULT_PROFILE = { 'ver': DS_VERSION, 'loh': 128, 'pid': 0, 'noc': 2, 'lof':12, 'lodh':64 }

class DataStorage:
    def __init__(self, filename=None, dblink=None):
        
        self.isAvailable = False   
        self.profile = DEFAULT_PROFILE
        self.profilelocked = False
        self.dsheader =None  # data storage header
         
        self.dbh = None  # current active data block
        self.db = [] 
        for i in range(self.profile['noc']):
            self.db.append([])
    
        #self._time = 0 
        #self.count = 0 
        
        self.cdap = 0 
        
        if filename is not None:
            ## file mode
            self.mode =  DSM_FILE
            self.filename = filename 
            if os.path.isfile(self.filename) == True:
                self.isAvailable = True
                self.__init_from_file()
                # TODO: - open the storage file
                #       - load profile
                #       - load data (default volume)
        elif dblink is not None:
            ## database mode
            self.mode =  DSM_DATABASE
            self.dblink = dblink
            # TODO: connect to database
            #       - load profile
            #       - load data (default volume) 
        else:
            self.mode =  DSM_UNKNONW
    
    
    def __init_from_file(self):
        with open(self.filename, 'rb') as f:
            dsheader = f.read(128)  # use default size of dsheader
            self.dsheader = DSHeader(data=dsheader)
            # calculate active dbp
            c_dap = self.dsheader.dap
            for i in range(self.dsheader.nob):
                f.seek(c_dap,0)
                dbhb = f.read(self.dsheader.ldh) # read block header
                dbh = DBHeader(data=dbhb)
                if dbh.np > 0:
                    c_dap = dbh.np
                    continue
                else:
                    self.dbh = dbh
                    break
                
            dbl = 0 
            #print(self.dsheader.nob)
            #print(vars(dbh))
            #print(vars(dbh.chns[0]))
            #print(vars(dbh.chns[1]))
            
            for chn in range(self.dsheader.noc):
                dbl += (dbh.chns[chn].nof * self.dsheader.lof)
             
            dbl += self.dsheader.ldh
            c_dap +=  dbl
            self.cdap = c_dap
            self.dsheader.cdap = c_dap
    
    
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
            self.__generate_dsheader()
            self.__generate_dbheader()
            self.cdap = self.dsheader.loh
     
    def __generate_dsheader(self):
        
        if self.dsheader is None:
            self.dsheader = DSHeader()
            
        # init dsheader from self.profile
        dsheader_vars = vars(self.dsheader)
        for k in self.profile.keys():
            if k in dsheader_vars:
                dsheader_vars[k] = self.profile[k] 
    
    def __generate_dbheader(self):
        if self.dbh is None:
            self.dbh = DBHeader(ldh=self.dsheader.ldh, noc=self.dsheader.noc)
            for i in range(self.dsheader.noc):
                self.dbh.addch(ch=CHInfo())
    
    ''' flush/save new (uploaded) data to the storage '''
    def flush(self, zipped=False):
        
        if self.mode == DSM_FILE: 
            with open(self.filename,"ab") as f: 
                
                # bh = {}  # data block header 
                
                #print("dsheadr.dap = {}".format(self.dsheader.dap))
                #print("dsheadr.cdap = {}".format(self.dsheader.cdap))
                db_pos = self.dsheader.cdap # recalculate datablock position in __init__()
                ds_pos = db_pos + self.dsheader.ldh   
                  
                print("dsheadr.cdap = {}".format(self.dsheader.cdap))
                print("cdap + ldh = {}".format(ds_pos))
                
                # TODO: update prev block header
                # self.dbh.np = 0 
                 
                # write data 
                f.seek(ds_pos, 0) 
                print("ftell() : {}".format(f.tell()))
                for chn in range(self.dsheader.noc): 
                    self.dbh.chns[chn].sp = ds_pos
                    for d in self.db[chn]:
                        f.write(d) 
                    print("ftell() : {}".format(f.tell())) 
                    ds_pos = f.tell() 
                
                
                print("test")
                buf = test_fread(db_pos, 200)
                print(buf)
                print("end of test")
                
                
                
                # update data block header
                self.dbh.pp = self.dbh.cp 
                self.dbh.cp = db_pos
                
                # write block header
                f.seek(db_pos,0)  
                dp_bytes = self.dbh.to_bytes()
                # print(dp_bytes)
                f.write(dp_bytes)
                
                # write storage header 
                self.dsheader.nob += 1
                f.seek(0,0)
                dh_bytes = self.dsheader.to_bytes()
                f.write(dh_bytes)
                
            self.isAvailable = True
            
            # end of flush()
            
    def settimestamp(self, ts=0): 
        if ts==0:
            now = datetime.datetime.now()
            ts =  time.mktime(now.timetuple()) 
         
        for i in range(self.dsheader.noc):
            self.dbh.chns[i].ts = ts #  struct.pack("f", ts)
     
    ''' Uplaod raw data to the storage '''    
    def upload(self, rawdata: RawData = None, size=0):
             
        lines = rawdata.getRawData() 
        chns = [*range(self.dsheader.noc)] 
        count = 0
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
                self.db[chn].append(info+data)
                self.dbh.chns[chn].nof += 1
                self.dbh.chns[chn].du += rs
                # TODO, update chn.du, ds 
                
            if size > 0:
                count += 1
                if count == size:
                    break

        #self.dph['chn0'] = [0, len(ds[0])]
        #self.dbh['chn1'] = [0, len(ds[1])]
         
    ''' Retrive data from the storage '''    
    def retrieve(self, starttime = None, duration = None):
        # access data storage and generate corresponding dataset 
        pass
