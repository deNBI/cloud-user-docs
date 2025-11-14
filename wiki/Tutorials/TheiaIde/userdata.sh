#!/bin/bash

function check_service {
  /bin/nc -z ${1} ${2}  2>/dev/null
  while test $? -eq 1; do
    echo  "wait 10s for service available at ${1}:${2}"
    sleep 10
    /bin/nc -z ${1} ${2}  2>/dev/null
  done
}

# log stdout/stderr  to /var/log/usedata
exec > /var/log/userdata.log
exec 2>&1

echo -- Wait for network configuration finished
check_service cloud.bi.denbi.de 443

# ---------------------------------------------------------------
# Attention! This userdata script was tested on 18.04 LTS image
# and must slightly modified for other systems
# ---------------------------------------------------------------

echo Install dependencies
apt-get update && apt-get -y install python-minimal make g++

echo Create build dir
# create build dir
mkdir /home/ubuntu/IDE
chown ubuntu:root /home/ubuntu/IDE
cd /home/ubuntu/IDE

echo Create configuration
cat > /home/ubuntu/IDE/package.json << "END"
{
  "private": true,
  "dependencies": {
    "typescript": "latest",
    "@theia/typescript": "latest",
    "@theia/navigator": "latest",
    "@theia/terminal": "latest",
    "@theia/outline-view": "latest",
    "@theia/preferences": "latest",
    "@theia/messages": "latest",
    "@theia/git": "latest",
    "@theia/file-search": "latest",
    "@theia/markers": "latest",
    "@theia/preview": "latest",
    "@theia/callhierarchy": "latest",
    "@theia/merge-conflicts": "latest",
    "@theia/search-in-workspace": "latest",
    "@theia/json": "latest",
    "@theia/textmate-grammars": "latest",
    "@theia/mini-browser": "latest"
  },
  "devDependencies": {
    "@theia/cli": "latest"
  }
}
END

chmod 644 /home/ubuntu/IDE/package.json


echo Create build script
cat > /home/ubuntu/IDE/theia-build.sh << "END"
#!/bin/bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.5/install.sh | bash
source /home/ubuntu/.nvm/nvm.sh
nvm install 8
npm install -g yarn
yarn
yarn theia build
END

chmod 755 /home/ubuntu/IDE/theia-build.sh

echo Build theia-ide as ubuntu user
su ubuntu -c /home/ubuntu/IDE/theia-build.sh

echo Create theia-ide startup script
cat > /home/ubuntu/IDE/theia-ide.sh << "END"
#!/bin/bash
source /home/ubuntu/.nvm/nvm.sh
cd $(dirname ${0})
yarn theia start /home/ubuntu --hostname 127.0.0.1 --port 8080 
END

chmod 755 /home/ubuntu/IDE/theia-ide.sh

echo Create theia-ide service
cat > /etc/systemd/system/theia-ide.service << "END"
[Unit]
Description=Theia-IDE service for user ubuntu
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=ubuntu
ExecStart=/home/ubuntu/IDE/theia-ide.sh 

[Install]
WantedBy=multi-user.target
END

echo Enable service 
systemctl enable theia-ide.service

echo Start service
systemctl start theia-ide.service

