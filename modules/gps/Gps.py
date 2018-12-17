import serial
import subprocess

class Gps:
    def __init__(self):
        self.ser = self.init_serial()

    def remove_blockage():
        subprocess.Popen("sudo rmmod ftdi_sio", shell=True)
        subprocess.Popen("sudo rmmod usbserial", shell=True)

    def init_serial(self):
        self.remove_blockage()
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = '/dev/ttyUSB0'
        ser.timeout = 2
        ser.open()
        if ser.isOpen():
            print('Open GPS serial port: ' + ser.portstr)
            
    def read_data(self):
        self.remove_blockage()
        return self.ser.readline()