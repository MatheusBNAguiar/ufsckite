wget https://www.ftdichip.com/Drivers/D2XX/Linux/libftd2xx-arm-v6-hf-1.4.8.gz
gunzip libftd2xx-arm-v6-hf-1.4.8.gz 
tar -xvf libftd2xx-arm-v6-hf-1.4.8
sudo cp -r ./release/build/lib* /usr/local/lib
sudo ln -s libftd2xx.so.1.4.8 libftd2xx.so
sudo modprobe ftdi_sio
sudo rmmod ftdi_sio
sudo rmmod usbserial

cd ./release/examples
make

bash ./pylibftdi.sh