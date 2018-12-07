sudo apt-get install libusb-1.0
cp ./11-ftdi.rules /etc/udev/rules.d/11-ftdi.rules
sudo adduser $USER plugdev
pip3 install pyftdi