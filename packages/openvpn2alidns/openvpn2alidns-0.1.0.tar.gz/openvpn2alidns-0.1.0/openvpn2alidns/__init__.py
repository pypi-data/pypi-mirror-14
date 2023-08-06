#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import getopt
import ConfigParser

import json
import re

from pprint import pprint

from aliyunsdkcore import client as AliyunClient
from aliyunsdkcore.profile import region_provider

from aliyunsdkalidns.request.v20150109 import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest

__version__ = '0.1.0'

class Client:
    
    def __init__(self, configFile, clientPath):
        
        config = ConfigParser.RawConfigParser()
        config.read(configFile)
        self.accessKey = config.get('alidns', 'accessKey')
        self.accessSecret = config.get('alidns', 'accessSecret')
        self.regionId = config.get('alidns', 'regionId')
        self.productName = config.get('alidns', 'productName')
        self.serviceAddr = config.get('alidns', 'serviceAddr')
        self.domainName = config.get('alidns', 'domainName')
        self.rrSuffix = config.get('alidns', 'rrSuffix')
        
        self.clientPath = clientPath

        if not region_provider.find_product_domain(self.regionId, self.productName):
            print("We need to update endpoint.xml since you don't have Alidns in it.")
            region_provider.modify_point(self.productName, self.regionId, self.serviceAddr)
        self.ac = AliyunClient.AcsClient(self.accessKey, self.accessSecret, self.regionId)

    def getDomainRecords(self):
        existedRecords = {}

        request=DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        request.set_accept_format('json')
        request.set_DomainName(self.domainName)
        request.set_PageNumber(1)
        request.set_PageSize(1)
        result = json.loads(self.ac.do_action(request), encoding='utf-8')

        total = result['TotalCount']
        if total > 0:
            request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
            request.set_accept_format('json')
            request.set_DomainName(self.domainName)
            request.set_PageNumber(1)
            request.set_PageSize(total)
            result = json.loads(self.ac.do_action(request), encoding='utf-8')
            if 'Code' not in result:
                for record in result['DomainRecords']['Record']:
                    match = re.match('^(.+)\.'+re.escape(self.rrSuffix)+'$', record['RR'])
                    if match:
                        server = match.group(1)
                        existedRecords[server] = record

        return existedRecords

    def getClients(self):
        clients = {}
        for subdir, dirs, files in os.walk(self.clientPath):
            for file in files:
                match = re.match('^(.+)\.'+re.escape(self.rrSuffix+'.'+self.domainName)+'$', file)
                if match:
                    with open(os.path.join(subdir, file), 'r') as f:
                        content = f.read()
                        content_match = re.match('ifconfig-push\s*([0-9\.]+)', content)
                        if content_match:
                            clients[match.group(1)] = content_match.group(1)
        return clients

    def updateRecords(self):
        existedRecords = self.getDomainRecords()
        for client,ip in self.getClients().items():
            print('{client}: {ip}'.format(client=client, ip=ip))
            if client in existedRecords:
                # existed record
                record = existedRecords[client]
                if record['Value'] != ip:
                    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
                    request.set_accept_format('json')
                    request.set_RecordId(record['RecordId'])
                    request.set_RR(client + '.' + self.rrSuffix)
                    request.set_Type('A')
                    request.set_Value(ip)
                    request.set_TTL(600)
                    result = self.ac.do_action(request)
                    print(result)
            else:
                # new record
                request = AddDomainRecordRequest.AddDomainRecordRequest()
                request.set_accept_format('json')
                request.set_DomainName(self.domainName)
                request.set_RR(client + '.' + self.rrSuffix)
                request.set_Type('A')
                request.set_Value(ip)
                request.set_TTL(600)
                result = self.ac.do_action(request)
                print(result)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "vc:", ["version", "config"])
    except getopt.GetoptError as _:
        print("Usage: openvpn2alidns [-c config] [openvpn path]")
        sys.exit(2)
    
    configFile = './config.ini'
    clientPath = '/etc/openvpn/client.d'

    for opt, arg in opts:
        if opt == '-v':
            print(__version__)
            sys.exit()
        elif opt == '-c' or opt == '--config':
            configFile = arg
            break

    if len(args) > 0:
        clientPath=args[0]

    c = Client(configFile=configFile, clientPath=clientPath)
    c.updateRecords();


if __name__ == '__main__':
    main()