import csv
import re
import logging
import threading
import time
from datetime import datetime
from pathlib import Path

import serial
from core.hardware.detector import (
    find_arduino_ports,
    ArduinoNotFoundError,
    MultipleArduinoPortsFoundError,
)
from core.utils.mock_data import generate_mock_data

POLL_INTERVAL = 0.01

class VernierFSRLogger:
    def __init__(self, baud: int = 9600, timeout: float = 1.0, use_mock: bool = False):
        self.use_mock = use_mock
        if self.use_mock:
            self.port = "mock"
            logging.info("Using mock data logger.")
        else:
            try:
                ports = find_arduino_ports()
            except ArduinoNotFoundError:
                logging.error("No Arduino found. Plug it in and try again.")
                raise
            except MultipleArduinoPortsFoundError as e:
                logging.error(f"Multiple Arduinos found: {e.ports!r}")
                raise

            self.port = ports if isinstance(ports, str) else ports[0]
            if self.port == "mock":
                self.use_mock = True
                logging.info("No Arduino found, switching to mock data logger.")
            else:
                logging.info(f"Opening serial port {self.port} @ {baud} baud")
                self.ser = serial.Serial(self.port, baudrate=baud, timeout=timeout)
                time.sleep(2)
                self.ser.reset_input_buffer()

        self.is_logging = False
        self._stop_reader = threading.Event()
        self._data_lines = []

    def start_logging(self) -> None:
        if not self.is_logging and not self.use_mock:
            self.ser.write(b's')
        self.is_logging = True

    def stop_logging(self) -> None:
        if self.is_logging and not self.use_mock:
            self.ser.write(b'e')
        self.is_logging = False

    def _reader_loop(self) -> None:
        while not self._stop_reader.is_set():
            if self.use_mock:
                line = generate_mock_data()
                timestamp = datetime.now().strftime('%H:%M:%S')
                entry = f"[{timestamp}] {line}"
                print(entry)
                self._data_lines.append(entry)
                time.sleep(POLL_INTERVAL)
            else:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        timestamp = datetime.now().strftime('%H:%M:%S')
                        entry = f"[{timestamp}] {line}"
                        print(entry)
                        self._data_lines.append(entry)
                    else:
                        time.sleep(POLL_INTERVAL)
                except serial.SerialException as e:
                    logging.error(f"Serial read error: {e}")
                    break

    def run(
        self,
        duration_seconds: float,
        start_delay: float = 0,
        save_dir: Path | str | None = None,
        file_stem: str | None = None
    ) -> tuple[Path | None, Path | None]:
        """
        Run the logger, save raw and clean CSV files after logging.

        Args:
            duration_seconds: Logging time in seconds.
            start_delay: Optional delay before start.
            save_dir: Directory to save files.
            file_stem: Base filename without extension.

        Returns:
            (raw_csv_path, clean_csv_path)
        """
        reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        reader_thread.start()

        if start_delay > 0:
            logging.info(f"Waiting {start_delay}s before logging...")
            time.sleep(start_delay)

        logging.info(f"Logging for {duration_seconds}s started.")
        self.start_logging()

        try:
            time.sleep(duration_seconds)
        except KeyboardInterrupt:
            logging.warning("Logging interrupted by user.")
        finally:
            self.stop_logging()
            self._stop_reader.set()
            self.ser.close()
            logging.info("Logging finished.")

        save_dir = Path(save_dir or ".")
        save_dir.mkdir(parents=True, exist_ok=True)
        file_stem = file_stem or "vernier"

        raw_path = self.save_to_csv(save_dir, f"RAW_{file_stem}.csv")
        clean_path = self.save_clean_csv(save_dir, f"CLEAN_{file_stem}.csv")
        return raw_path, clean_path

    def save_to_csv(self, save_dir: Path, filename: str) -> Path:
        filepath = save_dir / filename
        with filepath.open("w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamped_line"])
            for line in self._data_lines:
                writer.writerow([line])
        logging.info(f"Saved raw log to {filepath.resolve()}")
        return filepath


    def save_clean_csv(self, save_dir: Path, filename: str) -> Path | None:
        """
        Parse raw lines with format:
        [15:42:33] 0.100 | 31085 | 29010 | 50 | 25444

        Output columns: Time(s), A, B, C, D
        """
        pattern = re.compile(
            r"\[\d{2}:\d{2}:\d{2}\]\s+([\d.]+)\s+\|\s+(\d+)\s+\|\s+(\d+)\s+\|\s+(\d+)\s+\|\s+(\d+)"
        )

        extracted = list()
        for line in self._data_lines:
            match = pattern.search(line)
            if match:
                extracted.append(match.groups())

        if not extracted:
            logging.warning("No valid structured sensor data found.")
            return None

        filepath = save_dir / filename
        with filepath.open("w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Time(s)", "A", "B", "C", "D"])
            writer.writerows(extracted)

        logging.info(f"Saved clean log to {filepath.resolve()}")
        return filepath