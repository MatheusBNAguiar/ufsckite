#!/bin/bash
echo "Install base dependencies"
sudo apt-get install python3-pip


echo "Install swarmbee"
sh ./modules/swarmbee/setup.sh