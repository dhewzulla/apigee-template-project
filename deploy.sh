#!/bin/bash
appname="template-service"
org="dilshathewzulla"
env="test"

source ~/credentials/dilshat/credentials.sh
python deploy.py -n $appname -u $apigeeUsername:$apigeePassword  -o $org  -v development -e $env -s true -d 1 
#python delete-unused-revision.py -n $appname -u $apigeeUsername:$apigeePassword  -o $org  -v development -e $env -s true -d 1

  


