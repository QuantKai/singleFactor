# -*- coding: utf-8 -*-
# __author__ = 'Feiz-Chong'
import datetime as dt
import urllib2
import json
datetime_format = "%Y-%m-%d %X"
url = "http://192.168.1.10:7777"


def clf(obj):
    if isinstance(obj, dt.datetime) or isinstance(obj, dt.date):
        return obj.strftime('%Y-%m-%d %X')
    else:
        raise TypeError('%r is not JSON serializable' % obj)


class MyWindData:

    def __init__(self):
        self.ErrorCode = 0
        self.StateCode = 0
        self.RequestID = 0
        self.Codes = list()  #list( string)
        self.Fields = list() #list( string)
        self.Times = list() #list( time)
        self.Data = list()  #list( list1,list2,list3,list4)
        self.asDate=False
        self.datatype=0#0-->DataAPI output, 1-->tradeAPI output
        pass

    def set(self,dataDict):
        self.ErrorCode = dataDict["ErrorCode"]
        self.StateCode = dataDict["StateCode"]
        self.RequestID = dataDict["RequestID"]
        self.Codes = dataDict["Codes"] #list( string)
        self.Fields = dataDict["Fields"] #list( string)
        self.Times = dataDict["Times"]#list( time)
        self.Data = dataDict["Data"]  #list( list1,list2,list3,list4)
        self.asDate=dataDict["asDate"]
        self.datatype=dataDict["datatype"]#0-->DataAPI output, 1-->tradeAPI output

    def __str__(self):
        def str1D(v1d):
            if( not(isinstance(v1d,list)) ):
                  return str(v1d);

            outLen = len(v1d);
            if(outLen==0):
                return '[]';
            outdot = 0;
            outx='';
            outr='[';
            if outLen>10 :
                outLen = 10;
                outdot = 1;


            for x in v1d[0:outLen]:
              try:
                outr = outr + outx + str(x);
                outx=',';
              except UnicodeEncodeError:
                outr = outr + outx + repr(x);
                outx=',';

            if outdot>0 :
                outr = outr + outx + '...';
            outr = outr + ']';
            return outr;

        def str2D(v2d):
            #v2d = str(v2d_in);
            outLen = len(v2d);
            if(outLen==0):
                return '[]';
            outdot = 0;
            outx='';
            outr='[';
            if outLen>10 :
                outLen = 10;
                outdot = 1;

            for x in v2d[0:outLen]:
               outr = outr + outx + str1D(x);
               outx=',';

            if outdot>0 :
                outr = outr + outx + '...';
            outr = outr + ']';
            return outr;

        a=".ErrorCode=%d"%self.ErrorCode
        if(self.datatype==0):
            if(self.StateCode!=0): a=a+ "\n.StateCode=%d"%self.StateCode
            if(self.RequestID!=0): a=a+ "\n.RequestID=%d"%self.RequestID
            if(len(self.Codes)!=0):a=a+"\n.Codes="+str1D(self.Codes)
            if(len(self.Fields)!=0): a=a+"\n.Fields="+str1D(self.Fields)
            if(len(self.Times)!=0):
                if(self.asDate):a=a+ "\n.Times="+str1D([ format(x,'%Y%m%d') for x in self.Times])
                else:
                    a=a+ "\n.Times="+str1D([ format(x,'%Y%m%d %H:%M:%S') for x in self.Times])
        else:
            a=a+"\n.Fields="+str1D(self.Fields)

        a=a+"\n.Data="+str2D(self.Data)
        return a;

    def __repr__(self):
        return str(self);

def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v,list):
            for i in range(len(v)):
                if isinstance(v[i], unicode):
                    try:
                        v[i] = dt.datetime.strptime(v[i], datetime_format)
                    except:
                        pass
        elif isinstance(v, str):
            try:
                v = dt.datetime.strptime(v, datetime_format)
            except:
                pass
    return dct

class MyWind:
    def __init__(self):
        pass

    def start(self):
        pass

    def wsq(self,codes, fields, options=None, func=None,*arga,**argb):
        if options is None:
            options = "None"
        if func is None:
            func = "None"
        data = {'codes':codes, 'fields': fields, 'options': options, 'func': func,"arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/wsq", headers=headers, data=json.dumps(data, default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

    def wss(self,codes, fields, options=None, *arga, **argb):
        if options is None:
            options = "None"
        data = {'codes':codes, 'fields': fields, 'options': options, "arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/wss", headers=headers, data=json.dumps(data, default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

    def wsd(self,codes, fields, beginTime=None, endTime=None, options=None,*arga,**argb):
        if options is None:
            options = "None"
        if beginTime is None:
            beginTime = "None"
        if endTime is None:
            endTime = "None"
        data = {'codes':codes, 'fields': fields, 'options': options, 'beginTime': beginTime,'endTime': endTime,"arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/wsd", headers=headers, data=json.dumps(data, default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

    def wsi(self,codes, fields, beginTime=None, endTime=None, options=None,*arga,**argb):
        if options is None:
            options = "None"
        if beginTime is None:
            beginTime = "None"
        if endTime is None:
            endTime = "None"
        data = {'codes':codes, 'fields': fields, 'options': options, 'beginTime': beginTime,'endTime': endTime,"arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/wsi", headers=headers, data=json.dumps(data,default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

    def wset(self,tablename, options=None,*arga,**argb):
        if options is None:
            options = "None"
        data = {'tablename':tablename, 'options': options,"arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/wset", headers=headers, data=json.dumps(data, default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

    def tdays(self,beginTime=None, endTime=None, options=None,*arga,**argb):
        if beginTime is None:
            beginTime = "None"
        if endTime is None:
            endTime = "None"
        if options is None:
            options = "None"
        data = {'beginTime':beginTime, 'endTime':endTime,'options': options,"arga":arga,"argb":argb}
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url=url+"/tdays", headers=headers, data=json.dumps(data, default=clf))
        response = urllib2.urlopen(request)
        res = response.read()
        dataDict = json.loads(res, object_hook=datetime_parser)
        w = MyWindData()
        w.set(dataDict)
        return w

w=MyWind()