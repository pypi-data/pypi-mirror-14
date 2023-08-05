from um7 import UM7

sensor = UM7('sensor', '/dev/tty.usbserial-A903AAUZ')
sensor.settimer()

while True:
    sensor.grabsample(['xaccel', 'yaccel', 'zaccel', 'xgyro', 'rollpitch', 'yaw'])
    print sensor.state
