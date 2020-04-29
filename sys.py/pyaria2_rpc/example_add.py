"""
from pyaria2 import Jsonrpc
jsonrpc = Jsonrpc('localhost', 6800)
resp = jsonrpc.addUri('https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.0/FreeBSD-122222.0-RELEASE-amd64-memstick.img', options={"out": "fbsd.img"})
print resp
"""

from pyaria2 import Xmlrpc
rpc = Xmlrpc('localhost', 6800)
resp = rpc.addUri('https://download.freebsd.org/ftp/releases/ISO-IMAGES/12.0/FreeBSD-122222.0-RELEASE-amd64-memstick.img', options={"out": "fbsd.img"})
print resp

