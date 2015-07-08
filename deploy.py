#!/usr/bin/env python

import base64
import getopt
import httplib
import json
import re
import os
import sys
import StringIO
import urlparse
import xml.dom.minidom
import zipfile
import apigeeutil


arguments=apigeeutil.parseArguments()
deployedRevision=apigeeutil.getDeployedRevision(arguments['userPW'],arguments['organization'],arguments['proxyName'],arguments['environment'])
print "deployed revions:",deployedRevision

body=apigeeutil.makeBundleZip()
createdRevision=apigeeutil.createNewRevision(arguments['userPW'], body, arguments['organization'], arguments['proxyName'])
apigeeutil.mapRevisionToVersion(arguments['userPW'],arguments['organization'],arguments['proxyName'],createdRevision,arguments['deployVersion'])

print "Created a new revision:%s" %(createdRevision)
apigeeutil.activateRevision(arguments['userPW'], arguments['organization'], arguments['environment'], arguments['proxyName'], createdRevision,arguments['seamless'],arguments['delay'])
apigeeutil.deleteRevision(arguments['userPW'], arguments['organization'],arguments['proxyName'],deployedRevision)
apigeeutil.deleteRevisionToVersionMapEntry(arguments['userPW'], arguments['organization'],arguments['proxyName'],deployedRevision)
