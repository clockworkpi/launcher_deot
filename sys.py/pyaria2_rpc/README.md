```python
from pyaria2 import Jsonrpc
jsonrpc = Jsonrpc('localhost', 6800)
resp = jsonrpc.addUri('https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.0/FreeBSD-122222.0-RELEASE-amd64-memstick.img', options={"out": "fbsd.img"})
print resp
# {"id":0,"jsonrpc":"2.0","result":"3f6fa9aa6428a25f"}
```
```python
from pyaria2 import Xmlrpc
rpc = Xmlrpc('localhost', 6800)
resp = rpc.addUri('https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.0/FreeBSD-122222.0-RELEASE-amd64-memstick.img', options={"out": "fbsd.img"})
print resp
# 790af4098c7a7249
```

aria2.conf  

```
max-connection-per-server=5
enable-rpc=true
rpc-allow-origin-all=true
rpc-listen-all=true      
log-level=error          
log=/tmp/aria.log       
dir=~/aria2download       
daemon=true                             
allow-overwrite=true
#jsonrpc hook 
#on-download-complete=~/pyaria2-rpc/hook.py

```

