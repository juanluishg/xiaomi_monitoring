import serial
import time

def get_arduino(port='COM3', baudrate=9600, timeout=.1):
	arduino = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
	return arduino

def write(message, device):
	device.write(bytes(message, 'utf-8'))
	time.sleep(0.05)
	data = device.readline()
	return data

def read(device):
	return device.readline()


if __name__ == "__main__":
	arduino = get_arduino("/dev/ttyACM0")
	print(write("on",arduino))
