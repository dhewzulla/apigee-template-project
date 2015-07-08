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

apigeeutil.deletedUnusedRevisions(arguments['userPW'], arguments['organization'],arguments['proxyName'])


    


