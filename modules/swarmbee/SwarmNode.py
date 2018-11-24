import sys
import serial
import serial.tools.list_ports
import colorama
import time
from swarmbee.SerCom import SerCom

def get_ports():
    if sys.platform.startswith('win32'):
        com_ports = [(name, desc.encode('utf-16-be').decode('cp1251'), v_p)
                     for name, desc, v_p
                     in serial.tools.list_ports.comports()]
    else:
        raise NotImplementedError('Add functionality for other than win32 systems')
    s_cp = sorted(com_ports, key=lambda tup: tup[0])
    for num, port in enumerate(s_cp):
        print('{0} - PORT: {1[0]}, DESCRIPTION: {1[1]}'.format(num, port))

    return s_cp


def num_to_portname(ser, num):
    return ser[num][0]


def select_port(cp_list):
    num = int(input('Which port do you want to select?: '))
    return cp_list[num][0]

class SwarmNode(SerCom):
    CUR_FILE = r'D:\PVE\Utilities\cur.txt'
    __rato_buf = []
    __rrn_buf = []
    __buffer = []
    __COMMANDS = {
        'RATO_WO_TO': 'RATO 0 ',
        'RATO_W_TO': 'RATO 1 ',
        'GET_SET': 'GSET',
        'RES_SET': 'RSET',
        'SAVE_SET': 'SSET',
        'GET_ID': 'GNID'
    }

    __OUT_LEN = {
        'RATO': 3,
        'RRN': 5
    }

    __NOTIF = ['RRN', 'NIN', 'AIR', 'SDAT', 'DNO']
    __NOTIF_LEN = 5

    def __init__(self, port, disp_dist=False, disp_rrn=False):
        SerCom.__init__(self, port)
        self.disp_dist = disp_dist
        self.disp_rrn = disp_rrn

    def ranging(self, addr):
        if type(addr) != str:
            raise TypeError
        
        self.send_command(self.__COMMANDS['RATO_WO_TO'] + addr)
    
    def getNodeId(self):
        self.send_command(self.__COMMANDS['GET_ID'])
        return self.get_resp_u()

    def getSettings(self):
        self.send_command(self.__COMMANDS['GET_SET'])
        return self.get_resp_u()

    def getSwarmData(self):
        """ Method for working with threads
        Can be used for obtaining all messages from the connected SWARMBEE module
        For others activities, e.g. getting response after sending a command
        use the get_resp_u method
        """
        while True:
            try:
                msg = self.get_resp_u()
                # print(msg)  # FOR DEBUG
                self.__buffer.append(msg)
            except serial.SerialException:
                raise

    def get_resp_b(self):
        serialBuffer = self.ser.read()
        data = []
        if serialBuffer == b'=' or serialBuffer == b'*':
            data = self.ser.readline()
        else:
            nlines = int(self.ser.readline())
            for i in range(nlines):
                data.append(self.ser.readline())
            serialBuffer += bytes(str(nlines).encode('utf-8')) + self._RETEND
            data = b''.join(data)

        ts = self.__time_stamp().encode('utf-8')
        return ts + b' ' + serialBuffer + data

    def get_resp_u(self):
        return self.get_resp_b().decode('utf-8')

    @staticmethod
    def __split_buf_msg(buf, msg_len):
        split_msg = []
        num_val = len(buf)
        if not num_val == 0:
            for msg in buf:
                ts, msg = msg.split()  # Remove timestamp in buffer from useful payload
                msg = msg.split(',')
                if not len(msg) == msg_len:
                    continue
                split_msg.append(msg)
            
            return split_msg
        else:
            return -1

    def __process_rato(self):
        dist = 0
        t_buf = self.__split_buf_msg(self.__rato_buf, self.__OUT_LEN['RATO'])

        sz = len(t_buf) if not t_buf == -1 else 0
        if not sz == 0:
            for err, d, rssi in iter(t_buf):
                if not err[-1] == '0':
                    sz -= 1
                    continue
                dist += int(d) / 100

        dist = dist / sz if not sz == 0 else 0

        return dist

    def __process_rrn(self):
        dist = 0
        t_buf = self.__split_buf_msg(self.__rrn_buf, self.__OUT_LEN['RRN'])

        sz = len(t_buf) if not t_buf == -1 else 0
        if not sz == 0:
            for srca, reca, err, d, *ncfg in iter(t_buf):
                if not err == '0':
                    sz -= 1
                    continue
                dist += int(d) / 100

        dist = dist / sz if not sz == 0 else 0

        return dist

    def process_buf(self, out):
        t_buf = self.__buffer[:]

        for i in range(len(t_buf)):
            if self.__NOTIF[0] in t_buf[i]:
                ''' Process RRN notification
                Firmware version 2.1 has such format of Ranging Notification:
                '*RRN:<SrcID>,<DestID>,<ErrCode>,<Distance>,<DataNCFG>'
                Pass '*RRN:' and append it to __rrn_buffer
                '''
                self.__rrn_buf.append(self.__buffer[i][self.__NOTIF_LEN:])
            elif any(n in t_buf[i] for n in self.__NOTIF):
                continue
            else:
                ''' Process RATO
                Format of RATO messages is: '=<ErrC>,<Distance>,<RSSI>'
                '''
                self.__rato_buf.append(self.__buffer[i])

        self.__buffer.clear()
        
        for item in self.__rato_buf:
            out.write(item)

        if self.disp_dist:
            rato_dist = self.__process_rato()
            rrn_dist = self.__process_rrn()

            out_str = "Current distance (RATO): {:>5.2f} m".format(rato_dist)
            if self.disp_rrn:
                out_str += " " + \
                           "Current distance (RRN): {:>5.2f} m".format(rrn_dist)

            colored_out = colorama.Style.BRIGHT + colorama.Fore.CYAN + out_str + colorama.Style.RESET_ALL
            print(colored_out, end='\r')
            print(out_str, file=open(self.CUR_FILE, 'a'))

        self.__rato_buf.clear()
        self.__rrn_buf.clear()

        out.flush()

    @staticmethod
    def __time_stamp():
        c_time = time.time()
        ms = int(round(c_time * 1000 % 1000))

        time_str = '{}.{:0=3d}'.format(time.strftime('%H:%M:%S'), ms)
        return time_str