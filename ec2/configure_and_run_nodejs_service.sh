#!/bin/bash

# This script downloads & installs npm, pm2 and creates a basic Node JS service that responds to "Hello World" at port 8081
# This also configures the service to be up and running on EC2 reboot
# Tested on: AWS Linux AMI 2

echo "Installing NPM and PM2"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node
npm install -g pm2

echo "Creating Service Script"
echo "var http = require('http');" > ./app.js
echo "var port = 8081;" >> ./app.js
echo "http.createServer(function (request, response) {" >> ./app.js
echo "  response.writeHead(200, {'Content-Type': 'text/plain'});" >> ./app.js
echo "  response.end('Hello World\n');" >> ./app.js
echo "}).listen(port);" >> ./app.js
echo "console.log('Server running at http://127.0.0.1:'+port);" >> ./app.js

echo "Starting Service"
pm2 start -f app.js -i 1

echo "Enabling service run at startup"
pm2 startup
sudo env PATH=$PATH:/home/ec2-user/.nvm/versions/node/v15.14.0/bin /home/ec2-user/.nvm/versions/node/v15.14.0/lib/node_modules/pm2/bin/pm2 startup systemd -u ec2-user --hp /home/ec2-user
