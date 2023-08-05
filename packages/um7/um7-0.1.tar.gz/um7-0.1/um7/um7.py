# Daniel Kurek
# d'Arbeloff Lab, MIT
# January, 2016
# Module that holds UM7 class
# Creates serial objects, contains functions to parse serial data

#####################################################################
# TODO: Sensor Array, Commands
#####################################################################

import serial
import time
import binascii
import struct


class um7(object):

    def __init__(self, name, port):
        """Create new UM7 serial object.
        Baud Rate = 115200
        Byte Size = 8 bits
        No Parity, 1 Stop Bit, 0 second timeout
        EOL string is 'snp'
        For macs, type "ls /dev/tty.*" into termina to find connected device ports

        :param port: Virtual COM port to which the IMU is connected
                name: name of object
                t0: Start of sensing time.  All OS times will be relative to this.
                        If not give, sensing time will just be OS time.
        :return: UM7 Object
        """
        self.name = name
        self.t0 = time.time()
        self.state = {}
        try:
            self.serial = serial.Serial(port, 115200, bytesize=8, parity='N', stopbits=1, timeout=5)  # Open serial device
            print '%s serial device opened!' % self.name
        except OSError:
            print 'Could not connect to ' + self.name + '.  Is it plugged in or being used by another program?'

    def __del__(self):
        """Closes virtual com port

        :return: None
        """
        self.serial.close()
        print '%s serial device closed' % self.name

    def __name__(self):
        return self.name

    def state(self):
        return self.state

    def catchsample(self):
        [foundpacket, hasdata, startaddress, data, commandfailed] = self.readpacket()
        if not foundpacket:
            return False
        sample = parsedatabatch(data, startaddress, self.name)
        if sample:
            t = 'time'
            sample.update({t: time.time() - self.t0})
            self.state.update(sample)
        return sample

    def grabsample(self, datatype):
        address = name2hex_reg[datatype]
        returnaddress = []
        while address != returnaddress:
            self.request(datatype)
            [foundpacket, hasdata, returnaddress, data, commandfailed] = self.readpacket()
        sample = parsedata(data, returnaddress, self.name)
        if sample:
            t = 'time'
            sample.update({t: time.time() - self.t0})
            self.state.update(sample)
        return sample

    def readpacket(self):
        foundpacket = 0
        t0 = time.time()
        timeout = 1
        while time.time() - t0 < timeout:
            byte = self.serial.read(size=1)
            if byte == 's':
                byte2 = self.serial.read(size=1)
                if byte2 == 'n':
                    byte3 = self.serial.read(size=1)
                    if byte3 == 'p':
                        foundpacket = 1
                        break
        if foundpacket == 0:
            # print 'Could not find valid data packet or input buffer is empty (%s)' % self.name
            hasdata = 0
            commandfailed = 0
            startaddress = 0
            data = 0
        else:
            ptbyte = bin(int(binascii.hexlify(self.serial.read(size=1)), 16))[2:]
            hasdata = int(ptbyte[0], 2)
            numdatabytes = (int(ptbyte[2:6], 2))*4+4
            commandfailed = int(ptbyte[7], 2)
            startaddress = int(binascii.hexlify(self.serial.read(size=1)), 16)
            if hasdata:
                data = binascii.hexlify(self.serial.read(size=numdatabytes))
            else:
                data = 0
        return [foundpacket, hasdata, startaddress, data, commandfailed]

    def request(self, datatype):
        init = [0x73, 0x6e, 0x70, 0x00]
        address = name2hex_reg[datatype]
        decimalchecksum = 337 + address
        decimalchecksum1, decimalchecksum2 = divmod(decimalchecksum, 0x100)
        init.append(address)
        init.append(decimalchecksum1)
        init.append(decimalchecksum2)
        self.serial.write(init)

    def settimer(self, t=False):
        if t:
            self.t0 = t
        else:
            self.t0 = time.time()

    def checkinputbuffer(self):
        return self.serial.inWaiting()


def parsedata(data, address, devicename):

    datatype = dec2name_reg[address]

    if datatype == 'xgyro' or datatype == 'ygyro' or datatype == 'zgyro':
        data = struct.unpack('!f', data.decode('hex'))[0]
        output = {datatype: data}

    elif datatype == 'xaccel' or datatype == 'yaccel' or datatype == 'zaccel':
        data = struct.unpack('!f', data.decode('hex'))[0]
        output = {datatype: data}

    elif datatype == 'rollpitch':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 16.0
        output = {'roll': datasplit[0], 'pitch': datasplit[1]}

    elif datatype == 'yaw':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        datasplit[0] = struct.unpack('!h', datasplit[0].decode('hex'))[0] / 16.0
        output = {datatype: datasplit[0]}

    elif datatype == 'rollpitchrate':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 91.02222
        output = {'rollrate': datasplit[0], 'pitchrate': datasplit[1]}

    elif datatype == 'yawrate':
        datasplit = [data[i:i + 4] for i in range(0, len(data), 4)]
        datasplit[0] = struct.unpack('!h', datasplit[0].decode('hex'))[0] / 91.02222
        output = {datatype: datasplit[0]}

    else:
        return False

    return output


def parsedatabatch(data, startaddress, devicename):
    xg = 'xgyro'
    yg = 'ygyro'
    zg = 'zgyro'
    xa = 'xaccel'
    ya = 'yaccel'
    za = 'zaccel'
    r = 'roll'
    p = 'pitch'
    y = 'yaw'
    rr = 'rollrate'
    pr = 'pitchrate'
    yr = 'yawrate'
    if startaddress == 97:  # Processed Gyro Data
        n = 8
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[-1]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!f', datasplit[j].decode('hex'))[0]  # Convert hex string to IEEE 754 floating point
        output = {xg: datasplit[0], yg: datasplit[1], zg: datasplit[2]}
    elif startaddress == 101:  # Processed Accel Data:
        n = 8
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[-1]
        for j in range(len(datasplit)):
            datasplit[j] = struct.unpack('!f', datasplit[j].decode('hex'))[0]  # Convert hex string to IEEE 754 floating point
        output = {xa: datasplit[0], ya: datasplit[1], za: datasplit[2]}
    elif startaddress == 112:  # Processed Euler Data:
        n = 4
        datasplit = [data[i:i + n] for i
                     in range(0, len(data), n)]  # Split data string into array of data bytes (n hex chars each)
        del datasplit[9]
        del datasplit[8]
        del datasplit[7]
        del datasplit[3]  # Delete unused data bytes
        for j in range(len(datasplit)):
            if j < len(datasplit) - 3:  # Euler angle bytes
                datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 16.0  # Convert hex str to floating point
                # and convert using constant  # Euler angle rate bytes
            else:
                datasplit[j] = struct.unpack('!h', datasplit[j].decode('hex'))[0] / 91.02222  # Convert hex str to floating
                # point and convert using constant
        output = {r: datasplit[0], p: datasplit[1], y: datasplit[2], rr: datasplit[3], yr: datasplit[4], pr: datasplit[5]}
    else:
        return False
    return output


name2hex_reg = {'health': 0x55,
               'xgyro': 0x61,
               'ygyro': 0x62,
               'zgyro': 0x63,
               'xaccel': 0x65,
               'yaccel': 0x66,
               'zaccel': 0x67,
               'rollpitch': 0x70,
               'yaw': 0x71,
               'rollpitchrate': 0x72,
               'yawrate': 0x73}

dec2name_reg = {85: 'health',
                97: 'xgyro',
                98: 'ygyro',
                99: 'zgyro',
                101: 'xaccel',
                102: 'yaccel',
                103: 'zaccel',
                112: 'rollpitch',
                113: 'yaw',
                114: 'rollpitchrate',
                115: 'yawrate'}

