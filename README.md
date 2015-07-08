# apigee-template-project
An Apigee template project that can be a starting pointing for creating your own Apigee project
Following followig steps to create an Apigee project
(1) clone the repository git@github.com:dhewzulla/apigee-template-project.git

(2) edit the following files:

pom.xml
package-apigee-proxy/pom.xml
package-apigee-modules/pom.xml 
and change the value of the groupId and artifactId to the ones you prefer.

(3) In your home directory create the following file: ~/credentials/apigee.sh with the following content export apigeePassword="your apigee password" export apigeeUsername="your apigee user name"

(4) Edit deploy.sh file modify the following values appname="Your Prefered app name" org="The Target Apigee organization your would like to deploy"

(5) Run the following command to deploy ./deploy.sh
