import sys
import serial

class SerCom:
    """
    This is the wrapper class for pyserial API
    @__init__ : Accepts a port name.
    Must do a check for correct input like '/dev/tty' for Linux, 'COM' for Windows and so on
    @open_port: Do opening of the port
    @close_port: Do closing of the port
    @send_command(command): Pass the string you want to be sent to the port.
    At the end of the command adds _RETEND bytestring
    """

    _RETEND = b'\r\n'

    def __init__(self, port):
        self.port = port
        self.ser = None

    def open_port(self, baud=115200):
        try:
            self.ser = serial.Serial(self.port, baud)
            print("Port %s is opened now at baud %s" % (self.port, baud))
        except serial.SerialException:
            print("Device on port %s is busy or not found" % self.port)
            sys.exit()

    def close_port(self):
        if self.ser.isOpen():
            self.ser.close()
            print("The port is succesfully closed" if not self.ser.isOpen() else "Can not close the port")
        else:
            print("Port was not opened")

    def send_command(self, command):
        b_com = command.encode('utf-8') + self._RETEND
        self.ser.write(b_com)