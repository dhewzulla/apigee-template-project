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

def apigeeCall(userPW, contentType, accept, verb, uri, body):
    headers = dict()
    headers['Authorization'] = 'Basic %s' % base64.b64encode(userPW)        
    if contentType != None:
       headers['Content-Type'] = contentType
    if accept != None:
       headers['Accept'] = accept
    print "Seding %s request to APIGee on %s" % (verb,uri)            
    conn = httplib.HTTPSConnection('api.enterprise.apigee.com')           
    conn.request(verb, uri, body, headers)
    return conn.getresponse()

def deleteOrgMap(userPW,organization,mapName):
    print 'deleting org map %s  in orgnization:%s' %(mapName,organization)
    resp = apigeeCall(userPW, None, 'application/json', 'DELETE', '/v1/o/%s/keyvaluemaps/%s' % (organization,mapName), '')
    if resp.status != 200 and resp.status != 201:
       print 'deleting map is failed with the status %i:\n%s' % (resp.status, resp.read())      

def createOrgMap(userPW, filepath,organization):
   f = open(filepath, 'r')
   body = f.read()
   f.close()   
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/keyvaluemaps' % (organization), body)      
   if resp.status != 200 and resp.status != 201:
      print 'Creating  the org map  failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   responseInJson = json.load(resp)
   print 'Created the org map successfully with %s organization:%s' % (filepath,organization)

def createProduct(userPW, filepath,organization):
   f = open(filepath, 'r')
   body = f.read()
   f.close()   
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/apiproducts' % (organization), body)      
   if resp.status != 200 and resp.status != 201:
      print 'Creating  the api product  failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   responseInJson = json.load(resp)
   print 'Created the apiproduct successfully with %s organization:%s' % (filepath,organization)

def createDeveloper(userPW, filepath,organization):
   f = open(filepath, 'r')
   body = f.read()
   f.close()   
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/developers' % (organization), body)      
   if resp.status != 200 and resp.status != 201:
      print 'Creating  the developer  failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   responseInJson = json.load(resp)
   print 'Created the developer successfully with %s organization:%s' % (filepath,organization)

def createDeveloperApp(userPW, filepath,organization,developer):
   f = open(filepath, 'r')
   body = f.read()
   f.close()   
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/developers/%s/apps' % (organization,developer), body)      
   if resp.status != 200 and resp.status != 201:
      print 'Creating  the developer app failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   responseInJson = json.load(resp)
   print 'Created the developer app successfully with %s organization:%s' % (filepath,organization)


def createContract(userPW, organization,developer, developerapp, consumerkey, apiProduct):
   contractContent='{"consumerKey": "%s", "apiProducts": ["%s"]}' % (consumerkey, apiProduct)     
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/developers/%s/apps/%s/keys/%s' % (organization,developer,developerapp,consumerkey), contractContent)      
   if resp.status != 200 and resp.status != 201:
      print 'Creating  the contract with the product failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   responseInJson = json.load(resp)
   print 'Created the contract successfully with the product %s  for the developer app %s' % (apiProduct, developerapp)


def updateEnvMap(userPW, filepath,organization,environment,mapName):
   f = open(filepath, 'r')
   body = f.read()
   f.close()   
   resp = apigeeCall(userPW, None, 'application/json', 'DELETE', '/v1/o/%s/environments/%s/keyvaluemaps/%s' % (organization, environment,mapName), None)      
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'POST', '/v1/o/%s/environments/%s/keyvaluemaps' % (organization, environment), body)      
   if resp.status != 200 and resp.status != 201:
      print 'Updating the env map  failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)   
   print 'Updated the env map successfully with %s organization:%s environment:%s mapName:%s' % (filepath,organization,environment,mapName)
   
   
   
def createNewRevision(userPW, body, organization, proxyname):
   print 'importing a new revision to the the organization:%s for the apiproxy: %s' %(organization,proxyname)       
   resp = apigeeCall(userPW, 'application/octet-stream', 'application/json', 'POST', '/v1/organizations/%s/apis?action=import&name=%s' % (organization, proxyname), body)
   if resp.status != 200 and resp.status != 201:
      print 'Import failed to with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   deployment = json.load(resp)
   revision = int(deployment['revision'])
   print 'Imported new proxy version %i' % revision   
   return revision
   

def createNewRevisionFromFile(userPW, filepath, organization, proxyname):
   print 'start to import a new revision from the artefact:%s into the organization:%s for the apiproxy: %s' %(filepath,organization,proxyname)    
   f = open(filepath, 'r')
   body = f.read()
   f.close()
   return createNewRevision(userPW,body,organization,proxyname)

def deleteRevision(userPW,organization,proxyname,revision):
    print 'deleting the revision %s from %s in the organization:%s' %(revision,proxyname,organization)
    resp = apigeeCall(userPW, None, 'application/json', 'DELETE', '/v1/o/%s/apis/%s/revisions/%s' % (organization,proxyname,revision), '')
    if resp.status != 200 and resp.status != 201:
       print 'Deletion of the revision is failed with the status %i:\n%s' % (resp.status, resp.read())      
    else:        
       print 'deleted the revison  %s' % revision   

def getAPIProxyRevisions(userPW,organization,proxyname):
    print 'getting the revisions for %s in the orgnization:%s' %(proxyname, organization)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/apis/%s' % (organization,proxyname), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the proxy revisions failed with the status %i:\n%s' % (resp.status, resp.read())
       return None       
    responseInJson = json.load(resp)
    return responseInJson["revision"]

def getListOfProducts(userPW,organization):
    print 'getting the list of products in the orgnization:%s' %(organization)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/apiproducts' % (organization), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the list of products failed with the status %i:\n%s' % (resp.status, resp.read())
       return None       
    responseInJson = json.load(resp)
    return responseInJson

def getListOfDevelopers(userPW,organization):
    print 'getting the list of developers in the orgnization:%s' %(organization)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/developers' % (organization), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the list of developers failed with the status %i:\n%s' % (resp.status, resp.read())
       return None       
    responseInJson = json.load(resp)
    return responseInJson

def getListOfDeveloperApps(userPW,organization,developer):
    print 'getting the list of developer apps in the orgnization:%s for the developer %s' %(organization,developer)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/developers/%s/apps' % (organization,developer), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the list of developer apps failed with the status %i:\n%s' % (resp.status, resp.read())
       return None       
    responseInJson = json.load(resp)
    return responseInJson

def viewDeveloperAppDetails(userPW,organization,developer,developerapp):
    print 'getting the details of developer app in the orgnization:%s for the developer %s on the app %s' %(organization,developer,developerapp)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/developers/%s/apps/%s' % (organization,developer,developerapp), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the details of the developer app failed with the status %i:\n%s' % (resp.status, resp.read())
       return None       
    responseInJson = json.load(resp)
    return responseInJson


def getEnvironments(userPW,organization):
    print 'getting the envrionments for %s ' %(organization)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/environments' % (organization), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting the environments failed with the status %i:\n%s' % (resp.status, resp.read())
       return None    
    return json.load(resp)

def deletedUnusedRevisions(userPW,organization,proxyname):
    deployedRevisions=dict()
    environments=getEnvironments(userPW, organization)
    for environment in environments:    
       deployedRevision=getDeployedRevision(userPW, organization,proxyname,environment)
       deployedRevisions[deployedRevision]=True
    proxyRevisions=getAPIProxyRevisions(userPW, organization,proxyname)
    for rev in proxyRevisions:
       if deployedRevisions.get(rev) != None:
           print " revision is kept:%s" % (rev)
       else:
            deleteRevision(userPW,organization,proxyname,rev)
            print " revision is deleted:%s" % (rev)
           
    
def getDeployedRevision(userPW,organization,proxyname,environment):
    print 'getting the deployed revision for %s in the environment: %s, orgnization:%s' %(proxyname,environment, organization)
    resp = apigeeCall(userPW, None, 'application/json', 'GET', '/v1/o/%s/apis/%s/deployments' % (organization,proxyname), '')
    if resp.status != 200 and resp.status != 201:
       print 'getting deployments failed with the status %i:\n%s' % (resp.status, resp.read())
       return None      
    responseInJson = json.load(resp)
    for env in responseInJson['environment']:
        if env['name']==environment:
            for revision in env['revision']:
               return revision['name']    
    return None


    
def activateRevision(userPW, organization, environment, proxyname, revision,seamless,delay):
   print 'activating the new revision:%s in the organization:%s environment:%s for the apiproxy: %s  seamless:%s, delay:%s' %(revision,organization,environment,proxyname,seamless,delay)       
   resp = apigeeCall(userPW, 'application/x-www-form-urlencoded', 'application/json', 'POST', '/v1/o/%s/environments/%s/apis/%s/revisions/%s/deployments?override=%s&delay=%i' % (organization, environment,proxyname,revision,seamless,delay), '')
   if resp.status != 200 and resp.status != 201:
      print 'Activation failed with status %i:\n%s' % (resp.status, resp.read())
      sys.exit(2)
   deployment = json.load(resp)
   print 'activated the revision %s' % revision


def mapRevisionToVersion(userPW,organization,proxyname,revision,version):   
   resp = apigeeCall(userPW, 'application/json', 'application/json', 'PUT', '/v1/o/%s/keyvaluemaps/revision-version-map' % (organization) , '{"entry" : [{"name":"%s.%s","value":"%s"}], "name" : "revision-version-map"}' %(proxyname,revision,version))   
   print 'Updated revision to version map status: %i revision:%s version: %s ' % (resp.status, revision,version)
   #resp = apigeeCall(userPW, 'application/json', 'application/json', 'PUT', '/v1/o/%s/keyvaluemaps/revision-version-map' % (organization) , '{"entry" : [{"name":"%s.%s","value":"%s"}], "name" : "revision-version-map"}' %(proxyname,version,revision))
   #print 'Updated version to reversion map status: %i revision:%s version: %s ' % (resp.status, version,revision)
   
def deleteRevisionToVersionMapEntry(userPW,organization,proxyname,revision):   
   resp = apigeeCall(userPW, None, 'application/json', 'DELETE', '/v1/o/%s/keyvaluemaps/revision-version-map/entries/%s.%s' % (organization,proxyname,revision) , None)   
   print 'Deleted the revion map entry  with status: %i revision:%s' % (resp.status, revision)

def parseArguments():   
   arguments=dict()
   try: 
      opts = getopt.getopt(sys.argv[1:], 'u:e:n:o:v:f:s:d:c:a:p:b:')[0]
   except getopt.GetoptError:
      print "unrecognized argument:", sys.argv[1:]
      sys.exit(2)   
   for opt, arg in opts:      
      if opt == '-n':        
        arguments['proxyName'] = arg
      elif opt == '-o':
        arguments['organization'] = arg        
      elif opt == '-e':
        arguments['environment'] = arg    
      elif opt == '-u':
        arguments['userPW'] = arg    
      elif opt == '-v':
        arguments['deployVersion'] = arg
      elif opt == '-f':
        arguments['filepath'] = arg
      elif opt == '-s':
        arguments['seamless'] = arg
      elif opt == '-d':
        arguments['delay'] = int(arg)
      elif opt == '-c':
        arguments['config']=arg
      elif opt == '-a':
        arguments['developerapp']=arg
      elif opt == '-p':
        arguments['product']=arg
      elif opt == '-b':
        arguments['developer']=arg
   return arguments
 
def pathContainsDot(p):
    c = re.compile('\.\w+')
    for pc in p.split('/'):
        if c.match(pc) != None:
            return True
    return False

def addFileEntriesToZip(dirEntry,fileEntries,zipout,zipOutForNodeModule):
    count=0;
    modulecount=0;
    for fileEntry in fileEntries:
        if fileEntry.endswith('~'):
             continue
        fn=os.path.join(dirEntry,fileEntry)
        en=fn
        nodeModuleIndex=en.find("/node_modules/")
        apigeeAccessNodeModule=en.find("/node_modules/apigee-access")
        if(fn.find("/.")<=0 and nodeModuleIndex<0):            
             count=count+1
             zipout.write(fn, en)                                
        elif(apigeeAccessNodeModule>0):
            pass
        elif(fn.find("/.")<=0 and nodeModuleIndex>0):
            en=fn[nodeModuleIndex:]            
            zipOutForNodeModule.write(fn, en)
            modulecount=modulecount+1;
        else:
            pass
    return (count,modulecount)
      
def makeBundleZip():
     count=0
     modulecount=0
     tf = StringIO.StringIO()
     tfForNodeModules=StringIO.StringIO()
     zipout = zipfile.ZipFile(tf, 'w')
     zipOutForNodeModule=zipfile.ZipFile(tfForNodeModules, 'w')   
     dirList = os.walk("apiproxy")
     count=0;
     moduleCount=0;
     for dirEntry in dirList:         
        counters=addFileEntriesToZip(dirEntry[0],dirEntry[2],zipout,zipOutForNodeModule)
        count=count+counters[0]
        modulecount=modulecount+counters[1]          
     zipOutForNodeModule.close();
     moduleBody = tfForNodeModules.getvalue()
     if(modulecount>0):
        zipout.writestr("apiproxy/resources/node/node_modules.zip",moduleBody);
     print 'completed zip, number of files:%d'%(count)
     zipout.close() 
     body = tf.getvalue()       
     return body   		
