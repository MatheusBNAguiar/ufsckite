import serial
import subprocess

class Gps:
    def __init__(self):
        self.ser = self.init_serial()

    def init_serial(self):
        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = '/dev/ttyUSB0'
        ser.timeout = 2
        ser.open()

        if ser.isOpen():
            print 'Open GPS serial port: ' + ser.portstr
        self.ser = ser
    def read_data(self):
        subprocess.Popen("sudo rmmod ftdi_sio", shell=True)
        subprocess.Popen("sudo rmmod usbserial", shell=True)
        return self.ser.readline()