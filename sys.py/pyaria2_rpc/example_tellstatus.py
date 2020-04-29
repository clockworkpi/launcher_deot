import sys

"""
from pyaria2 import Jsonrpc
jsonrpc = Jsonrpc('localhost', 6800)

if(len(sys.argv) > 1):
    print sys.argv[1]
    resp = jsonrpc.tellStatus( sys.argv[1], ["gid","status","errorCode","errorMessage"] )
    print resp
"""

from pyaria2 import Xmlrpc
rpc = Xmlrpc('localhost', 6800)

if(len(sys.argv) > 1):
    print sys.argv[1]
    resp = rpc.tellStatus( sys.argv[1], ["gid","status","errorCode","errorMessage"] )
    print resp

