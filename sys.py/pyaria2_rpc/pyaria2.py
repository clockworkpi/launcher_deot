# -*- coding: utf-8 -*-

import sys
import time
import urllib2
import json
import xmlrpclib
import random
import requests

class Xmlrpc(object):
    def __init__(self, host, port, token=None):
        self._idCount = 0
        self.host = host
        self.port = port
        self.serverUrl = "http://{host}:{port}/rpc".format(**locals())
	self.s = xmlrpclib.ServerProxy(self.serverUrl,allow_none=True)
	self.aria2 = self.s.aria2

    def getOption(self,gid):
	try:
	    return self.aria2.getOption(gid)
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def addUri(self,uris, options=None):#aria2.addUri(['http://example.org/file'], {})
        try:
	    if isinstance(uris, basestring):
                return self.aria2.addUri([uris],options)
	    else:
                return self.aria2.addUri(uris,options)

        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def tellStatus(self,gid,keys=None):#aria2.tellStatus("2089b05ecca3d829", ["gid", "status"])
	try:
	    return self.aria2.tellStatus(gid,keys)
        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def tellActive(self,keys=None):
	try:
	    return self.aria2.tellActive(keys)
        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def tellWaiting(self,offset=0,num=0,keys=None):
	try:
	    return self.aria2.tellWaiting(offet,num,keys)
        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def tellStopped(self,offset=0,num=0,keys=None):
	try:
	    return self.aria2.tellStopped(offset,num,keys)
        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def remove(self,gid):
	try:
	    return self.aria2.remove(gid)
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def forceRemove(self,gid):
	try:
	    return self.aria2.forceRemove(gid)
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def getGlobalStat(self):
	try:
	    return self.aria2.getGlobalStat()
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def purgeDownloadResult(self):
	try:
	    return self.aria2.purgeDownloadResult()
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def removeDownloadResult(self,gid):
	try:
	    return self.aria2.removeDownloadResult(gid)
	except xmlrpclib.Fault as ex:
	    print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
	    return None

    def getUris(self,gid):
        try:
	    return self.aria2.getUris(gid)
        except xmlrpclib.Fault as ex:
            print "<Fault %s: %s>" % (ex.faultCode, ex.faultString)
            return None

    def urlDownloading(self,url):
        ret = False
        try:
            resp = self.tellActive()
            for i in resp:
                uris = self.aria2.getUris(i["gid"])
                for x in uris:
                    if x["uri"] == url:
                        return i["gid"],True
        except:
            return None,False
        return None,False
    
    def urlWaiting(self,url):
        try:
            _g = self.getGlobalStat()
            num = _g["numWaiting"]
            if num > 0:
                resp = self.tellWaiting(0,num)
                for i in resp:
                    uris = self.aria2.getUris(i["gid"])
                    for x in uris:
                        if x["uri"] == url:
                            return i["gid"],True
        except:
            return None,False
          
        return None,False

    def getPercent(self,url):
        try:
            resp = self.tellActive()
            for i in resp:
                uris = self.aria2.getUris(i["gid"])
                for x in uris:
                    if x["uri"] == url:
                        pct = float(i["completedLength"]) / float( i["totalLength"])
                        pct = pct * 100.0
                        return int(pct)
        except:
            return None
        return None

class Wsrpc(object):

    MUTI_METHOD = "system.multicall"
    ADDURI_METHOD = "aria2.addUri"
    TELLSTATUS_METHOD= "aria2.tellStatus"
    TELLACTIVE_METHOD="aria2.tellActive"
    TELLWAITING_METHOD="aria2.tellWaiting"
    TELLSTOPPED_METHOD="aria2.tellStopped"
    REMOVE_METHOD="aria2.remove"
    FORCEREMOVE_METHOD="aria2.forceRemove"
    GETGLOBALSTAT_METHOD="aria2.getGlobalStat"
    PURGEDOWNLOADRESULT_METHOD="aria2.purgeDownloadResult"
    REMOVEDOWNLOADRESULT_METHOD="aria2.removeDownloadResult"

    def __init__(self, host, port, token=None):
        self._idCount = 0
        self.host = host
        self.port = port
        self.serverUrl = "ws://{host}:{port}/jsonrpc".format(**locals())

    def _genParams(self, method , params):
        p = {
            'jsonrpc': '2.0',
            'id': self._idCount,
            'method': method,
            'test': 'test',
            'params': []
        }
        
        for i in params:
            if i is not None:
		p['params'].append(i)

        return p

    def _post(self, action, params):
	#print params
        paramsObject = self._genParams(action, params)
        #print paramsObject 
        data=json.dumps(paramsObject)
        return data

    def addUri(self, uris, options=None):
        if isinstance(uris, basestring):
            return self._post(Wsrpc.ADDURI_METHOD, [[uris,], options])
        else:
            return self._post(Wsrpc.ADDURI_METHOD, [uris, options])

    def tellStatus(self,gid,keys=None):
        return self._post(Wsrpc.TELLSTATUS_METHOD,[gid,keys])

    def tellActive(self,keys=None):
        return self._post(Wsrpc.TELLACTIVE_METHOD,[keys])

    def tellWaiting(self,offset=0,num=0,keys=None):
        return self._post(Wsrpc.TELLWAITING_METHOD,[offset,num,keys])

    def tellStopped(self,offset=0,num=0,keys=None):
        return self._post(Wsrpc.TELLSTOPPED_METHOD,[offset,num,keys])

    def remove(self,gid):
        return self._post(Wsrpc.REMOVE_METHOD,[gid])

    def forceRemove(self,gid):
        return self._post(Wsrpc.FORCEREMOVE_METHOD,[gid])

    def getGlobalStat(self):
        return self._post(Wsrpc.GETGLOBALSTAT_METHOD,[])

    def purgeDownloadResult(self):
        return self._post(Wsrpc.PURGEDOWNLOADRESULT_METHOD,[])

    def removeDownloadResult(self,gid):
        return self._post(Wsrpc.REMOVEDOWNLOADRESULT_METHOD,[gid])

class Jsonrpc(object):

    MUTI_METHOD = "system.multicall"
    ADDURI_METHOD = "aria2.addUri"
    TELLSTATUS_METHOD= "aria2.tellStatus"
    TELLACTIVE_METHOD="aria2.tellActive"
    TELLWAITING_METHOD="aria2.tellWaiting"
    TELLSTOPPED_METHOD="aria2.tellStopped"
    REMOVE_METHOD="aria2.remove"
    FORCEREMOVE_METHOD="aria2.forceRemove"
    GETGLOBALSTAT_METHOD="aria2.getGlobalStat"
    PURGEDOWNLOADRESULT_METHOD="aria2.purgeDownloadResult"
    REMOVEDOWNLOADRESULT_METHOD="aria2.removeDownloadResult"

    def __init__(self, host, port, token=None):
        self._idCount = 0
        self.host = host
        self.port = port
        self.serverUrl = "http://{host}:{port}/jsonrpc".format(**locals())

    def _genParams(self, method , params):
        p = {
            'jsonrpc': '2.0',
            'id': self._idCount,
            'method': method,
            'test': 'test',
            'params': []
        }
        
        for i in params:
            if i is not None:
		p['params'].append(i)

        return p

    def _post(self, action, params, onSuccess, onFail=None):
        if onFail is None:
            onFail = Jsonrpc._defaultErrorHandle
	print params
        paramsObject = self._genParams(action, params)
        print paramsObject 
        resp = requests.post(self.serverUrl, data=json.dumps(paramsObject))
        result = resp.json()
        if "error" in result:
            return onFail(result["error"]["code"], result["error"]["message"])
        else:
            return onSuccess(result)#give json object back

    def addUri(self, uris, options=None):
        def success(response):
            return response["result"]
        if isinstance(uris, basestring):
            return self._post(Jsonrpc.ADDURI_METHOD, [[uris,], options], success)
        else:
            return self._post(Jsonrpc.ADDURI_METHOD, [uris, options], success)

    def tellStatus(self,gid,keys=None):
        def success(response):
            return response
        return self._post(Jsonrpc.TELLSTATUS_METHOD,[gid,keys],success)

    def tellActive(self,keys=None):
        def success(response):
            return response
        return self._post(Jsonrpc.TELLACTIVE_METHOD,[keys],success)

    def tellWaiting(self,offset=0,num=0,keys=None):
        def success(response):
            return response
        return self._post(Jsonrpc.TELLWAITING_METHOD,[offset,num,keys],success)

    def tellStopped(self,offset=0,num=0,keys=None):
        def success(response):
            return response
        return self._post(Jsonrpc.TELLSTOPPED_METHOD,[offset,num,keys],success)

    def remove(self,gid):
        def success(response):
            return response
        return self._post(Jsonrpc.REMOVE_METHOD,[gid],success)

    def forceRemove(self,gid):
        def success(response):
            return response
        return self._post(Jsonrpc.FORCEREMOVE_METHOD,[gid],success)

    def getGlobalStat(self):
        def success(response):
            return response
        return self._post(Jsonrpc.GETGLOBALSTAT_METHOD,[],success)

    def purgeDownloadResult(self):
        def success(response):
            return response
        return self._post(Jsonrpc.PURGEDOWNLOADRESULT_METHOD,[],success)

    def removeDownloadResult(self,gid):
        def success(response):
            return response
        return self._post(Jsonrpc.REMOVEDOWNLOADRESULT_METHOD,[gid],success)


    @staticmethod
    def _defaultErrorHandle(code, message):
        print ("pyaria2 ERROR: {},{}".format(code, message))
        return None
