import sys
import subprocess
import serial
import time
import re
import cowsay
import pyfiglet
#"/dev/ttyUSB0"
def flash_and_monitor(port="/dev/ttyUSB0", flash_baud=460800, monitor_baud=115200):
    cowsay.tux("Laboratorio 2025")
    try:
        # Flash ESP32
        cmd = [
            "python", "-m", "esptool",
            "--chip", "esp32",
            "--port", port,
            "--baud", str(flash_baud),
            "write_flash",
            "0x1000", "/home/pi/Esp-tool/ScriptLab/bootloader.bin",
            "0x8000", "/home/pi/Esp-tool/ScriptLab/partitions.bin",
            "0x10000", "/home/pi/Esp-tool/ScriptLab/firmware.bin"
        ]
        subprocess.run(cmd, check=True)
        #print("Flash Completado.... Iniciando Monitoreo....")
        cowsay.tux("Flash Completado.... Iniciando Monitoreo....")
        # Wait for device to reset
        time.sleep(0.1)
        
        # Monitor serial output
        ser = serial.Serial(port, monitor_baud, timeout=1)
        print(f"Monitoreando: {port} Velocidad: {monitor_baud} baud. Presione Ctrl+C para Salir.")
        patron = r"IP:\s*(\d+\.\d+\.\d+\.\d+)"
        IPdata = "0.0.0.0"
        flagCon = True
        ascii_text = pyfiglet.figlet_format("successful")
        while True:
            if ser.in_waiting:
                line = ser.readline().decode('utf-8', errors='replace')
                print(line, end='')
                coincidencia = (re.search(patron, line))
                if coincidencia and flagCon:
                    ip = coincidencia.group(1)
                    if "IP: "+ip in line:
                        IPdata = ip
                        #print(f"Esta es la ip {ip}")
                        flagCon = False
                if "[Server]: Server IP: "+IPdata in line:
                    if "[Server]: Server IP: 172.20.201.19" in line:
                        cowsay.fox(f"\n¡Actualizacion Completa IP Bus: {IPdata}")
                        print(ascii_text)
                        time.sleep(10)
                        ser.close()
                        return True
                    else:
                        cowsay.cow(f"\n¡Actualizacion Completa IP: {IPdata}")
                        time.sleep(10)
                        ser.close()
                        return True
                if "[Server]: Server IP: 0.0.0.0" in line:
                        cowsay.pig(f"\n¡Actualizacion Completa IP Vacia: {IPdata}")
                        #print(ascii_text)
                        #print(cowsay.char_names)
                        time.sleep(20)
                        ser.close()
                        return True
                
    except subprocess.CalledProcessError as e:
        print(f"Error Programando ESP32: {e}")
        cowsay.milk(f"Error Programando Logic Control System")
        sys.exit(1)
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        cowsay.milk(f"Error")
        sys.exit(1)
    except KeyboardInterrupt:
        cowsay.milk("Saliendo")
        #print("\nSaliendo...")
        if 'ser' in locals():
            ser.close()
        sys.exit(0)

if __name__ == "__main__":
    flash_and_monitor()
        
