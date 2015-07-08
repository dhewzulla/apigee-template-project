var http = require('http');

var svr = http.createServer(function(req, resp) {
  resp.writeHead(200, { 'Content-Type': 'text/json' });
  resp.write(JSON.stringify({"title":"This the default title for the NodeJS service","content":"This is the default content for the NodeJS service "}));  
  resp.end('\n');
});

svr.listen(9000, function() {
  console.log('The server is listening on port 9000');
});










