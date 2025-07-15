from core.hardware.detector import find_arduino_ports
import serial.tools.list_ports


def debug_serial_ports():
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No serial ports detected on the system.")
        return

    print("Serial Port Scan Report:\n")
    for port in ports:
        print(f"Device         : {port.device}")
        print(f"Name           : {port.name}")
        print(f"Description    : {port.description or 'N/A'}")
        print(f"Manufacturer   : {port.manufacturer or 'N/A'}")
        print(f"Product        : {port.product or 'N/A'}")
        print(f"Interface      : {port.interface or 'N/A'}")
        print(f"Serial Number  : {port.serial_number or 'N/A'}")
        print(f"Location       : {port.location or 'N/A'}")
        print(f"HWID           : {port.hwid}")
        print(
            f"VID:PID        : {port.vid}:{port.pid}"
            if port.vid and port.pid
            else "VID:PID        : N/A"
        )
        print("-" * 70)

    arduino_ports = find_arduino_ports()
    if arduino_ports:
        print("\nDetected Arduino/Teensy-Compatible Devices:")
        for p in arduino_ports:
            print(f"  - {p}")
    else:
        print("\nNo Arduino or Teensy-compatible devices detected.")


if __name__ == "__main__":
    debug_serial_ports()
