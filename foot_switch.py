import serial
import time

def initialise_port():
    """initialize the serial port"""
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.port = '/dev/ttyUSB0'
    ser.setRTS(False)
    ser.open()
    return ser

def send_signal(ser):
    """command to start a Scan (like a single press of the footswitch)"""
    ser.setRTS(True)
    time.sleep(0.5)
    ser.setRTS(False)

def close_port(ser):
    """"CLose serial port"""
    ser.close()
