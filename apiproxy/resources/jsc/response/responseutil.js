var responseutil={
		cachettl:60,
		getResponseHeaderValue:function(context,varname){			
			//return context.proxyResponse.headers[identifier];
			return context.getVariable("response.header."+varname);
		},
		setResponseHeaderValue:function(context,varname,varvalue){	
			context.setVariable("response.header."+varname,varvalue);
		},
		getRequestHeaderValue:function(context,varname){			
			//return context.proxyResponse.headers[identifier];
			return context.getVariable("request.header."+varname);
		},
		log:function(context,identifier,value){
			this.setResponseHeaderValue(context,'debug-'+identifier,value);
		},
		addCacheTTL:function(context,ttl){			   
			var cachettl=this.cachettl;
			if(ttl){
				cachettl=ttl;				
			}
			else{
						var cachecontrolvalue=this.getResponseHeaderValue(context,'Cache-Control');
						if(cachecontrolvalue!=null){				
						    var maxageidentifier="max-age=";
						    var n=cachecontrolvalue.indexOf(maxageidentifier);
						    if(n>=0){
							    		n+=maxageidentifier.length;				
							            var cachecontrollength=cachecontrolvalue.length;
							           if(n<cachecontrolvalue.length){					     
							        	   cachettl=cachecontrolvalue.substring(n);				              
							           }
						     }
						}
			}
			this.setResponseHeaderValue(context,'apigee-cache-ttl',cachettl);			   
		},
		addcoors:function(context,allowedOrigins){		
		    var origin=this.getRequestHeaderValue(context,"Origin");
		    var requestMethod=this.getRequestHeaderValue(context, "Access-Control-Request-Method");
		    var requestHeaders=this.getRequestHeaderValue(context, "Access-Control-Request-Headers");
		    
		    var allowed=false;		    
		    if(origin!=null){			 						     
			     for(var i=0;i<allowedOrigins.length;i++){				
				      if(origin.indexOf(allowedOrigins[i])==0){			
					       allowed=true;
				      }
		   	      }
		    }
			if(allowed=true){			    	 			    	 
				this.setResponseHeaderValue(context,'Access-Control-Allow-Origin',origin);
			    	 //context.removeVariable("response.header.Origin");			    	 
			    this.setResponseHeaderValue(context,'Access-Control-Max-Age',"5");
			    	 
			    if(requestMethod!=null){
			    	    this.setResponseHeaderValue(context,'Access-Control-Allow-Methods',requestMethod);
			    	    //context.removeVariable("response.header.Access-Control-Request-Method");
			    }
			    if(requestHeaders!=null){			    	 
			    		 this.setResponseHeaderValue(context,'Access-Control-Allow-Headers',requestHeaders);
			    		 //context.removeVariable("response.header.Access-Control-Request-Headers");
			     }			    	 
		    }
		},
		currentTime:function(){
			   var start = new Date("March 23, 2014 00:00:00")
			   var now = new Date();
			   result= now.getTime();
			   result-=start.getTime();	
			   result/=1000;
			   return ""+parseInt(result);
			   
		},
		addCacheTimestamp:function(context){			
			   this.setResponseHeaderValue(context,'apigee-cache-timestamp',this.currentTime());   						   
		},		
		
		addCacheControlHeader:function(context){
			   
			   var cachetimestamp=this.getResponseHeaderValue(context,'apigee-cache-timestamp');
			   if(!cachetimestamp){
				   this.log(context,"controlHeaderMessage","cachetimestamp is not set");
				   this.setResponseHeaderValue(context,'Cache-Control',null);
				   
				   
				   return;				   
			   }
			   //this.log(context,"cachetimestamp",cachetimestamp); 
			   
			   var cachettl=this.getResponseHeaderValue(context,'apigee-cache-ttl');
			   if(!cachettl){
				   this.log(context,"controlHeaderMessage","apigee-cache-ttl is not set");				   
				   this.setResponseHeaderValue(context,'Cache-Control',null);
				   return;
			   }
			   //this.log(context,"cachettl",cachettl);
			   var cachecleartime=parseInt(cachetimestamp)+parseInt(cachettl);
			  // this.log(context,"cachecleartime",cachecleartime);
			   var currentT=this.currentTime();
			   var maxage=cachecleartime-currentT;
			   
			   //this.log(context,"currenttime",currentT);
			   //this.log(context,"maxage",maxage);
			   
			   if(maxage<=0)
				   maxage=0;
			   this.setResponseHeaderValue(context,'Cache-Control',"max-age="+maxage);
			   
		}
		
		
		
		
		
};