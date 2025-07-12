import threading
import time
import csv
import re
import math
from datetime import datetime
from pathlib import Path

import serial
from core.detector import (
    find_arduino_ports,
    ArduinoNotFoundError,
    MultipleArduinoPortsFoundError,
)

POLL_INTERVAL = 0.01  # 10 ms


class VernierFSRLogger:
    def __init__(self, baud=9600, timeout=1.0):
        # try:
        #     p = find_arduino_ports()
        # except ArduinoNotFoundError:
        #     raise RuntimeError("No Arduino found. Plug it in and try again.")
        # except MultipleArduinoPortsFoundError as e:
        #     raise RuntimeError(f"Multiple Arduinos found: {e.ports!r}")
        
        # self.port = p if isinstance(p, str) else p[0]
        # print(f"Opening {self.port} @ {baud} baud")
        # self.ser = serial.Serial(self.port, baudrate=baud, timeout=timeout)
        # time.sleep(2)  # let Arduino reboot
        # self.ser.reset_input_buffer()

        self.is_logging = False
        self._stop_reader = threading.Event()
        self._data_lines = []

    def start_logging(self):
        if not self.is_logging:
            # self.ser.write(b's')
            self.is_logging = True

    def stop_logging(self):
        if self.is_logging:
            # self.ser.write(b'e')
            self.is_logging = False

    def _reader_loop(self):
        while not self._stop_reader.is_set():
            # line = self.ser.readline().decode('utf-8', errors='ignore').strip()
            # if line:
            #     timestamped_line = f"[{datetime.now().strftime('%H:%M:%S')}] {line}"
            #     print(timestamped_line)
            #     self._data_lines.append(timestamped_line)
            # else:
            #     time.sleep(POLL_INTERVAL)
            pass

    def _dummy_reader_loop(self):
        start_time = time.time()
        while not self._stop_reader.is_set():
            elapsed_time = time.time() - start_time
            force_n = 2.5 + 1.5 * (1 + round(math.sin(2 * math.pi * 0.5 * elapsed_time), 4))
            delta_f = 0.1 * (1 + round(math.sin(2 * math.pi * 1 * elapsed_time), 4))
            fsr1 = 500 + int(100 * (1 + round(math.sin(2 * math.pi * 0.2 * elapsed_time), 4)))
            fsr2 = 600 + int(150 * (1 + round(math.sin(2 * math.pi * 0.3 * elapsed_time), 4)))
            fsr3 = 700 + int(200 * (1 + round(math.sin(2 * math.pi * 0.4 * elapsed_time), 4)))

            line = f"{elapsed_time:.2f}, Force(N): {force_n:.4f}, ΔF(N): {delta_f:.4f}, FSR1: {fsr1}, FSR2: {fsr2}, FSR3: {fsr3}"
            timestamped_line = f"[{datetime.now().strftime('%H:%M:%S')}] {line}"
            print(timestamped_line)
            self._data_lines.append(timestamped_line)
            time.sleep(POLL_INTERVAL)

    def run_for(self, duration_seconds: float, start_delay: float = 0):
        # t = threading.Thread(target=self._reader_loop, daemon=True)
        t = threading.Thread(target=self._dummy_reader_loop, daemon=True)
        t.start()

        if start_delay > 0:
            print(f"Waiting {start_delay}s before starting logging...")
            time.sleep(start_delay)

        print(f"Logging started for {duration_seconds}s...")
        self.start_logging()

        try:
            time.sleep(duration_seconds)
        except KeyboardInterrupt:
            print("Interrupted by user.")
        finally:
            self.stop_logging()
            self._stop_reader.set()
            # self.ser.close()
            print("Logging stopped.")

    def save_to_csv(self, filename=None):
        if not filename:
            filename = f"vernier_log_{datetime.now():%Y%m%d_%H%M%S}.csv"

        with open(filename, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["timestamped_line"])
            for line in self._data_lines:
                writer.writerow([line])

        print(f"Saved raw log to {filename}")
        return filename

    def save_clean_csv(self, filename=None):
        if filename is None:
            filename = f"vernier_clean_{datetime.now():%Y%m%d_%H%M%S}.csv"

        pattern = re.compile(
            r"^\s*([\d.]+), Force\(N\): ([\d.\-]+), ΔF\(N\): ([\d.\-]+), "
            r"FSR1: (\d+), FSR2: (\d+), FSR3: (\d+)"
        )

        extracted_rows = []
        for line in self._data_lines:
            if line.startswith('['):
                try:
                    line = line.split('] ', 1)[1]
                except IndexError:
                    continue

            match = pattern.match(line)
            if match:
                extracted_rows.append(match.groups())

        if not extracted_rows:
            print("No valid sensor data found to save.")
            return None

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Time(s)", "Force(N)", "DeltaF(N)", "FSR1", "FSR2", "FSR3"])
            writer.writerows(extracted_rows)

        print(f"Saved clean CSV to: {filename}")
        return filename


def run_logger_session(
    duration=30,
    delay=0,
    baud=9600,
    timeout=1.0,
    save_csv=True,
    experiment_name=None
):
    """
    Runs the VernierFSRLogger for a specified duration and optionally saves logs.

    Returns:
        Tuple[str | None, str | None]: (raw_csv_path, clean_csv_path)
    """
    logger = VernierFSRLogger(baud=baud, timeout=timeout)
    logger.run_for(duration_seconds=duration, start_delay=delay)

    raw_file, clean_file = None, None
    if save_csv:
        if experiment_name:
            base_dir = Path(experiment_name)
            base_dir.mkdir(parents=True, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_prefix = base_dir.name
            raw_file = base_dir / f"{file_prefix}_raw_{ts}.csv"
            clean_file = base_dir / f"{file_prefix}_clean_{ts}.csv"
        raw_file = logger.save_to_csv(filename=str(raw_file) if raw_file else None)
        clean_file = logger.save_clean_csv(filename=str(clean_file) if clean_file else None)

    return raw_file, clean_file
