import sys
from pyaria2 import Xmlrpc
rpc = Xmlrpc('localhost', 6800)

resp = rpc.getGlobalStat()
print resp

if( int(resp["numActive"]) > 0 ):
    resp2 = rpc.tellActive()
    print resp2
    for i in resp2:
        rpc.remove(i["gid"])
        rpc.removeDownloadResult(i["gid"])
    	

if( int(resp["numWaiting"]) > 0):
    offset = 0
    num = int(resp["numWaiting"]) 
    resp2 = rpc.tellWaiting(offset,num)
    print resp2
    for i in resp2:
       rpc.remove(i["gid"])
       rpc.removeDownloadResult(i["gid"])

if( int(resp["numStopped"]) > 0):
    offset = 0
    num = int(resp["numStopped"])
    print num 
    print "numStopped"
    resp2 = rpc.tellStopped(offset,num)
    print resp2[0]["files"][0]["uris"]
    for i in resp2:
       rpc.remove(i["gid"])#may occurs errors like: <Fault 1: Active Download not found for GID#3c9df48c8ff636e6>...
       rpc.removeDownloadResult(i["gid"]) #clear the records 

