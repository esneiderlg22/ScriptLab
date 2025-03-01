import serial
import sys
import time

def get_fixed_network_config():
    ip = "172.20.201.19"
    subnet = "255.255.255.0"
    gateway = "172.20.201.1"
    return f"ip:{ip}-gateway:{gateway}-subnet:{subnet}"

def monitor_serial(port="COM5", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("Starting serial connection...")
        
        # Monitoring and reading for first 2 seconds
        start_time = time.time()
        while time.time() - start_time < 3:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
        
        # Send Y without newline
        ser.write(b'Y')  # Solo envía Y sin \n
        ser.flush()      # Asegura que se envíe inmediatamente
        print("\nSent 'Y' command")
        time.sleep(5)  # Pequeña pausa después de enviar Y
        
        # Monitoring and reading for first 2 seconds
        start_time = time.time()
        while time.time() - start_time < 3:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
        
        # Get and send fixed network configuration
        config = get_fixed_network_config()
        ser.write(f"{config}\n".encode())
        print(f"\nSent configuration: {config}")
        print("\nContinuing monitoring. Press Ctrl+C to exit.")
        
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