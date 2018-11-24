sudo wget -O /usr/local/bin/rmate https://raw.githubusercontent.com/aurora/rmate/master/rmate
sudo chmod a+x /usr/local/bin/rmate

sudo chmod 777 /dev/ttyAMA0 && python test.py
python test.py



#disable bt connection
#dtoverlay=pi3-miniuart-bt
#dtparam=i2c1=on
#dtoverlay=i2c-gpio,bus=3
#dtparam=i2c_baudrate=10000