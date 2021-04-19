#!/bin/bash
sudo su -

PORT="8081"

cd /home
echo "Starting to install npm" > ./install_log.log

yum install -y gcc-c++ make
echo "Installed gcc and make" >> ./install_log.log

curl -sL https://rpm.nodesource.com/setup_15.x | sudo -E bash -
echo "Downloaded npm setup tool" >> ./install_log.log

yum install -y nodejs
echo "Installed Node JS" >> ./install_log.log
node -v >> ./install_log.log
npm install -g pm2
echo "Installed pm2" >> ./install_log.log

echo "Creating Service Script" >> ./install_log.log
echo "var http = require('http');" > ./app.js
echo "var port = ${PORT};" >> ./app.js
echo "http.createServer(function (request, response) {" >> ./app.js
echo "  response.writeHead(200, {'Content-Type': 'text/plain'});" >> ./app.js
echo "  response.end('Hello World From: '+port);" >> ./app.js
echo "}).listen(port);" >> ./app.js
echo "console.log('Server running at http://127.0.0.1:'+port);" >> ./app.js

echo "Starting Service" >>  ./install_log.log
pm2 start -f app.js -i 1

echo "Enabling service run at startup" >> ./install_log.log
pm2 startup

echo "all done" >> ./install_log.log
