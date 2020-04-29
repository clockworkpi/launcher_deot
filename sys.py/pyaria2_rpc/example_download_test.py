
from time import sleep
from pyaria2 import Xmlrpc

OVER = False 

#remote_file_url = 'https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.0/FreeBSD-12.0-RELEASE-amd64-memstick.img'
remote_file_url = "https://raw.githubusercontent.com/cuu/gamestore/master/gameshell-19q3/AGENT%20OF%20SHINIGAMI/file/AGENT%20OF%20SHINIGAMI.tar.gz"
#remote_file_url = "https://raw.githubusercontent.com/cuu/gamestore/master/index.json"

rpc = Xmlrpc('localhost', 6800)
gid = None
ret = False
gid,ret = rpc.urlDownloading(remote_file_url)
print(gid,ret)
if ret  == False:
    resp = rpc.addUri(remote_file_url, options={"out": "fbsd.tar.gz"})
    print resp
    gid = resp
else:
    print "url in the queue"

while True:
    stat = rpc.tellStatus(gid)
    print(stat)
    if stat["status"]=="complete":
        print "over"
        exit()
    sleep(2)
    

