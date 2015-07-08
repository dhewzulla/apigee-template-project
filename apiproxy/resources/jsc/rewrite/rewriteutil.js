var rewriteutil={						
		log:function(context,identifier,value){
			context.setVariable("response.header.debug-"+identifier,value);
			
		},
		escapeRegExp:function(str) {
				return str.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, "\\$&");
		},
        replaceContent:function(content,fromRegExpression,toValue){        	
        	return content.replace(new RegExp(fromRegExpression,'g'),toValue);        
        },
		getBaseURL:function(context){						
            var orgname=context.getVariable("organization.name");
            var environmentname=context.getVariable ("environment.name");                  
            return "http://"+orgname+"-"+environmentname+".apigee.net";
		},
        getCurrentProxyURL:function(context){        	
        	var proxybasepath=context.getVariable("proxy.basepath");        
            return this.getBaseURL(context)+proxybasepath+"/";
        },
        getProxyURL:function(context,proxypath){
        	        
            return this.getBaseURL(context)+proxypath;
        },
        
        rewriteTargetLinkToItself:function(context){            
            var targetURL=context.getVariable("verifyapikey.c4verifyapikey.portal")+"/";
            var proxyURL=this.getCurrentProxyURL(context);
            if(targetURL!=null && context.proxyResponse.content!=null){
	            var regExpression=this.escapeRegExp(targetURL);
	            context.proxyResponse.content=this.replaceContent(context.proxyResponse.content,regExpression,proxyURL);
            }
        },
        
};


