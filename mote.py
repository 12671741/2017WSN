#!/usr/bin/env python
from coapthon.client.helperclient import HelperClient
import re
import time


class mote:
    def __init__(self,moteip):
        self.ip = moteip
        self.port = 5683
        path =".well-known/core"
        self.client = HelperClient(server=(self.ip, self.port))
        self.manl=0
        response = self.client.get(path)
        response=response.pretty_print().split(',')
        sensorlist=[]
        for i in range(2,len(response)):
            sensor=[]
            try:
                attr=re.search(r'\<(.*)\>;title=\"(.*)";(.*)',response[i])
                sensor.append(attr.group(1))
                sensor.append(attr.group(2))
                sensor.append(attr.group(3))
                sensorlist.append(sensor)
            except:
                pass
        self.sensorlist=sensorlist

    global client_callback_observe
    def client_callback_observe(self):
        pass


    def man(self,):
        for index, item in enumerate(self.sensorlist): print index, item
        self.manl=index
        return index

    def start(self,):
        self.client = HelperClient(server=(self.host, self.port))

    def stop(self,):
        self.client.stop()

    def get(self,pathInd):
        path=self.sensorlist[pathInd][0]
        try:
            response = self.client.get(path)
            response=response.pretty_print()
            response = re.sub(r'\n','', response)
            response = re.sub(r'.*yload:\ ','', response)
            return response,self.sensorlist[pathInd][1]
        except:
            print "(GET)can't reach server"
            print path

    def post(self,pathInd,payload):
        response = self.client.post(self.sensorlist[pathInd][0], payload)
        return response
    def put(self,pathInd,payload):
        response = self.client.put(self.sensorlist[pathInd][0], payload)
        return response
    def observe(self,pathInd):
        path=self.sensorlist[pathInd][0]
        try:
            response = self.client.get(path)
            response=response.pretty_print()
            response = re.sub(r'\n','', response)
            response = re.sub(r'.*"v":','', response)
            response = re.sub(r'\,\".*','', response)
            return response,self.sensorlist[pathInd][1]
        except:
            print "(GET)can't reach server"
            print path
    def discover(self,):
        response = self.client.discover()
        return response
    def delete(self,pathInd):
        response = self.client.delete(self.sensorlist[pathInd][0])
        return response

    def __del__(self):
        self.client.stop()
