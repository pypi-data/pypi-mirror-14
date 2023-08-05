#!/usr/bin/python
# coding:utf-8

import boto3
from boto3.session import Session
import sys,traceback
import os
import subprocess
import time
from os import path
import logging
import traceback
import pprint
import base64
import re


LOG = logging.getLogger(__name__)

version = 0.01
here = path.abspath(path.dirname(__file__))

pp = pprint.PrettyPrinter(indent=4)

def display_list_function(client):

    response = client.list_functions()

    print '+------------------------------+------------+--------+--------+----------+------------------------------+'
    print "|%-30s|%-12s|%-8s|%-8s|%-10s|%-30s|" % ('FunctionName','Runtime','Memory','Timeout','Version','LastModefied' )
    print '+------------------------------+------------+--------+--------+----------+------------------------------+'
    for element in response['Functions']:
        print "|%-30s|%-12s|%-8s|%-8s|%-10s|%-30s|" % (element['FunctionName'],element['Runtime'],element['MemorySize'],element['Timeout'],element['Version'],element['LastModified'])

    print '+------------------------------+------------+--------+--------+----------+------------------------------+'

def display_function_detail(client,function_name):

    try:
        response = client.get_function(FunctionName=function_name)
    except Exception:
        #print Exception
        print 'No Resource Name'
        return

    print '+--------------------+--------------------------------------------------------------------------------+'
    for element in response['Configuration']:
       print "|%-20s|%-80s|" % (element,response['Configuration'][element])

    print '+--------------------+--------------------------------------------------------------------------------+'

def invoke_function(client,function_name):

    try:
        response = client.invoke(
                    FunctionName=function_name,
                    InvocationType='RequestResponse',
                    LogType='Tail',
                    #ClientContext='string',
                    #Payload=b'bytes',
                    #Qualifier='string'
                   )

    except Exception:
        print 'No Resource Name'
        return

    log = base64.b64decode(response['LogResult'])
    position = log.find('REPORT RequestId')
    results_log = log[:position-1]
    print '+---------------------------------------------------------------------------------------------------+' 
    print '| Summary                                                                                           |'
    print '+---------------------------------------------------------------------------------------------------+'
    results = re.split('\t',log[position:])

    for result in results:
        if len(result.strip()) != 0:
            display_result = result.split(':')
            print "|%-30s|%-68s|" %(display_result[0],display_result[1] ) 

    print '+---------------------------------------------------------------------------------------------------+'
    print

    print '+---------------------------------------------------------------------------------------------------+'
    print '| Log output                                                                                        |'
    print '+---------------------------------------------------------------------------------------------------+'
    print results_log
    print 


def main():

    if not (sys.version_info[0] == 2 and sys.version_info[1] == 7):
        raise RuntimeError('lambda-controller requires Python 2.7')

    import argparse

    parser = argparse.ArgumentParser(
            version=('version %s' % version),
            description='AWS Lambda Controller')

    parser.add_argument('--profile','-p', 
                        dest='profile',
                        help='specify AWS cli profile')

    parser.add_argument('--list','-l', 
                        dest='list',
                        action='store_const',
                        help='Lambda Function List',
                        const=True)

    parser.add_argument('--detail','-d', 
                        dest='detail',
                        default=None, 
                        help='Lambda Function Detail Info')

    parser.add_argument('--invoke', '-i', 
                        dest='invoke',
                        default=None, 
                        help='Invoke Lambda Function')

    parser.add_argument('--region', '-r', 
                        dest='region',
                        default=None, 
                        help='region')

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('-V', dest='loglevel', action='store_const',
                         const=logging.INFO,
                         help="Set log-level to INFO.")
    verbose.add_argument('-VV', dest='loglevel', action='store_const',
                         const=logging.DEBUG,
                         help="Set log-level to DEBUG.")
    parser.set_defaults(loglevel=logging.WARNING)

    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel)
    LOG.debug(args)

    session = Session(region_name="ap-northeast-1",
             profile_name=args.profile)

    client = session.client('lambda')

    if args.list is None \
        and ( args.detail is None or len(args.detail)==0 ) \
        and ( args.invoke is None or len(args.invoke)==0 ):
            print 'usage: lambda-controller '
            print '  -h, --help     show this help message and exit'
            print '  -v, --version  show program\'s version number and exit'
            print '  -p, --profile  specify AWS cli profile'
            print '  -l, --list,    Lambda Function List'
            print '  -d, --detail,  Lambda Function Detail'
            print '  -i, --invoke,  Invoke Lambda Function'
            print '  -r, --region,  Region'

    if args.list == True:
        display_list_function(client)

    elif not args.detail is None and  len(args.detail) != 0:
        display_function_detail(client,args.detail)

    elif not args.invoke is None and len(args.invoke) != 0:
        invoke_function(client,args.invoke)   

if __name__ == "__main__":
    main()

