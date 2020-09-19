import serial

serialCom = serial.Serial('com1', 9600)

serialCom.write(b'Hello')
