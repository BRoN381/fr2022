import serial
from time import sleep

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
    while ser.in_waiting:
        serinput = int(ser.readline().decode('utf-8'))
        print('serinput', serinput)
        sleep(0.5)
        ser.write('000111'.encode('utf-8'))
