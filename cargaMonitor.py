import sys
import subprocess
import serial
import time
import re
import cowsay

def flash_and_monitor(port="COM5", flash_baud=460800, monitor_baud=115200):
    cowsay.tux("Laboratorio 2025")
    try:
        # Flash ESP32
        cmd = [
            "python", "-m", "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", str(flash_baud),
            "write_flash",
            "0x1000", "bootloader.bin",
            "0x8000", "partitions.bin",
            "0x10000", "firmware.bin"
        ]
        subprocess.run(cmd, check=True)
        #print("Flash Completado.... Iniciando Monitoreo....")
        cowsay.tux("Flash Completado.... Iniciando Monitoreo....")
        # Wait for device to reset
        time.sleep(5)
        
        # Monitor serial output
        ser = serial.Serial(port, monitor_baud, timeout=1)
        print(f"Monitoreando: {port} Velocidad: {monitor_baud} baud. Presione Ctrl+C para Salir.")
        patron = r"IP:\s*(\d+\.\d+\.\d+\.\d+)"
        IPdata = "0.0.0.0"
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
                coincidencia = (re.search(patron, line))
                if "[Server]: Server IP: "+IPdata in line:
                    if "[Server]: Server IP: 0.0.0.0" in line:
                        cowsay.daemon(f"\n¡Actualizacion Completa IP Vacia: {IPdata}")
                        #print(cowsay.char_names)
                        ser.close()
                        return True
                    if "[Server]: Server IP: 172.20.201.19" in line:
                        cowsay.turtle(f"\n¡Actualizacion Completa IP Bus: {IPdata}")
                        ser.close()
                        return True
                    cowsay.cow(f"\n¡Actualizacion Completa IP: {IPdata}")
                    ser.close()
                    return True
                if coincidencia:
                    ip = coincidencia.group(1)
                    if "IP: "+ip in line:
                        IPdata = ip
                
                
    except subprocess.CalledProcessError as e:
        cowsay.ghostbusters(f"Error Programando ESP32: {e}")
        #print(f"Error Programando ESP32: {e}")
        sys.exit(1)
    except serial.SerialException as e:
        cowsay.ghostbusters(f"Serial error: {e}")
        #print(f"Serial error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        cowsay.ghostbusters("Saliendo")
        #print("\nSaliendo...")
        if 'ser' in locals():
            ser.close()
        sys.exit(0)

if __name__ == "__main__":
    flash_and_monitor()