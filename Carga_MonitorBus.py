import sys
import subprocess
import serial
import time



def reset_com_port(port="COM5"):
    """
    Intenta cerrar y reabrir el puerto COM para 'resetearlo' en software.
    Nota: Esto no reinicia el hardware, pero puede liberar el puerto si estaba bloqueado.
    """
    try:
        ser = serial.Serial(port)
        ser.close()
        time.sleep(1)  # Espera 1 segundo para que se libere el puerto
        print(f"Puerto {port} reiniciado (cerrado y reabierto).")
    except Exception as e:
        print(f"Error al reiniciar el puerto {port}: {e}")

def enter_bootloader(port="COM5", retries=3):
    """
    Fuerza al ESP32 a entrar en modo bootloader usando la secuencia de reset.
    Se realizan varios intentos en caso de fallar.
    """
    BOOTLOADER_BAUD = 115200
    attempt = 0
    while attempt < retries:
        try:
            with serial.Serial(port, BOOTLOADER_BAUD) as ser:
                
                # Asegurar que todo esté desactivado
                ser.dtr = ser.rts = False
                time.sleep(0.1)  # Tiempo para estabilizar

                # Mantener EN (DTR) en alto y GPIO0 (RTS) en bajo para forzar el modo boot
                ser.dtr = True  # EN high
                ser.rts = False   # GPIO0 low (modo boot)
                time.sleep(0.2)    # Espera adicional
                ser.rts = True
            return  # Secuencia exitosa, salimos de la función
        except Exception as e:
            print(f"Error en intento {attempt+1}: {e}")
            attempt += 1

    raise Exception("No se pudo forzar el modo bootloader tras varios intentos.")


def flash_and_monitor(port="COM5", flash_baud=921600, monitor_baud=115200):
    try:
        # Flash ESP32
        reset_com_port(port)
        enter_bootloader(port)
        
        cmd = [
            "python", "-m", "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", str(flash_baud),
            #"--before", "no_reset",
            "--before", "default_reset",
            "--after", "no_reset",
            "write_flash",
            "--flash_mode", "dio",
            "--flash_size", "detect",
            "--flash_freq", "40m",
            "0x1000", "bootloader.bin",
            "0x8000", "partitions.bin",
            "0x10000", "firmware.bin"
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print("Flasheo exitoso")
        except subprocess.CalledProcessError as e:
            print(f"Error en esptool: {e}")
            flash_and_monitor()
        
        
        #subprocess.run(cmd, check=True)
        #print("Flash successful! Starting serial monitor...")
        
        # Wait for device to reset
        time.sleep(5)
        monitor_serial()
        # Monitor serial output
        #ser = serial.Serial(port, monitor_baud, timeout=1)
        #print(f"Monitoring {port} at {monitor_baud} baud. Press Ctrl+C to exit.")
        
        #while True:
            #if ser.in_waiting:
                #line = ser.readline().decode('utf-8', errors='replace')
                #print(line, end='')
                
    except subprocess.CalledProcessError as e:
        print(f"Error flashing ESP32: {e}")
        sys.exit(1)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        if 'ser' in locals():
            ser.close()
        sys.exit(0)


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
    flash_and_monitor()