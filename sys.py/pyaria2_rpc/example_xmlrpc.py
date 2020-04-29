
from pyaria2 import Xmlrpc
rpc = Xmlrpc('localhost', 6800)

#resp = rpc.aria2.addUri(['http://music.xyz.com/test.mp3'], {"out": "aa.mp3"})
#print resp
resp2 = rpc.getOption('2089b05ecca3d829')
print resp2

