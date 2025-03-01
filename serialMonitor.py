import serial
import sys
import re
import time

def validate_ip(ip):
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    octets = ip.split('.')
    return all(0 <= int(octet) <= 255 for octet in octets)

def get_network_config():
    while True:
        ip = input("Enter IP address (xxx.xxx.xxx.xxx): ")
        if validate_ip(ip):
            break
        print("Invalid IP format")
    
    while True:
        subnet = input("Enter subnet mask (xxx.xxx.xxx.xxx): ")
        if validate_ip(subnet):
            break
        print("Invalid subnet format")
    
    while True:
        gateway = input("Enter gateway (xxx.xxx.xxx.xxx): ")
        if validate_ip(gateway):
            break
        print("Invalid gateway format")
    
    return f"ip:{ip}-gateway:{gateway}-subnet:{subnet}"

def monitor_serial(port="COM5", baudrate=115200):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print("Starting serial connection...")
        
        # Monitoring and reading for first 2 seconds
        start_time = time.time()
        while time.time() - start_time < 2:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
        
        # Send Y without newline
        ser.write(b'Y')  # Solo envía Y sin \n
        ser.flush()      # Asegura que se envíe inmediatamente
        print("\nSent 'Y' command")
        time.sleep(0.5)  # Pequeña pausa después de enviar Y
        
        # Get and send network configuration
        config = get_network_config()
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