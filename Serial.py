import serial
import sys
import re
import time


def monitor_serial(port="COM5", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("Starting serial connection...")
        print("Mayde y Paulo")
        # Continue monitoring
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
                
    except serial.SerialException as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        ser.close()
        sys.exit(0)

if __name__ == "__main__":
    monitor_serial()