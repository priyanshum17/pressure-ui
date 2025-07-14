# Understanding Mock Mode in PreSure

PreSure includes a "mock mode" that allows you to run and test the application without needing a physical Arduino device connected. This is particularly useful for development, debugging, and demonstrating the application's functionality.

## How Mock Mode Works

When in mock mode, the application simulates sensor data instead of attempting to read from a serial port. This prevents errors related to missing hardware and allows the data logging and analysis features to be tested end-to-end.

## Instances of Mock Usage in the Codebase

Here's where mock mode is implemented and how it affects the application's behavior:

### 1. `core/hardware/detector.py`

This file is responsible for detecting connected Arduino devices. If no physical Arduino is found, the `find_arduino_ports()` function will return the string `"mock"`.

```python
# core/hardware/detector.py
# ...
    if not arduino_ports:
        return "mock" # Returns "mock" if no Arduino is found
# ...
```

This allows the `VernierFSRLogger` to gracefully switch to mock data generation.

### 2. `core/logging/logger.py`

The `VernierFSRLogger` class is the core component for data acquisition. It has a `use_mock` parameter in its constructor and logic to handle both real and mock data streams.

-   **`__init__(self, ..., use_mock: bool = False)`:** The constructor accepts a `use_mock` boolean. If set to `True`, the logger will explicitly operate in mock mode.

    ```python
    # core/logging/logger.py
    # ...
    class VernierFSRLogger:
        def __init__(self, baud: int = 9600, timeout: float = 1.0, use_mock: bool = False):
            self.use_mock = use_mock
            if self.use_mock:
                self.port = "mock"
                logging.info("Using mock data logger.")
            # ... (rest of the initialization)
    ```

-   **Automatic Mock Mode Activation:** If `find_arduino_ports()` returns `"mock"` (meaning no Arduino was detected), the logger automatically sets `self.use_mock = True`.

    ```python
    # core/logging/logger.py
    # ...
            self.port = ports if isinstance(ports, str) else ports[0]
            if self.port == "mock":
                self.use_mock = True
                logging.info("No Arduino found, switching to mock data logger.")
            # ...
    ```

-   **`start_logging()` and `stop_logging()`:** These methods conditionally send commands (`'s'` for start, `'e'` for end) to the serial port only when `use_mock` is `False`.

    ```python
    # core/logging/logger.py
    # ...
    def start_logging(self) -> None:
        if not self.is_logging and not self.use_mock:
            self.ser.write(b's')
        self.is_logging = True

    def stop_logging(self) -> None:
        if self.is_logging and not self.use_mock:
            self.ser.write(b'e')
        self.is_logging = False
    # ...
    ```

-   **`_reader_loop()`:** This internal method either reads from the serial port or calls `generate_mock_data()` based on the `self.use_mock` flag.

    ```python
    # core/logging/logger.py
    # ...
    def _reader_loop(self) -> None:
        while not self._stop_reader.is_set():
            if self.use_mock:
                line = generate_mock_data() # Generates simulated data
                # ...
            else:
                # ... (reads from serial port)
    ```

-   **`run()` method:** The `ser.close()` call is also conditional, ensuring no errors occur when no physical serial port is open.

    ```python
    # core/logging/logger.py
    # ...
        finally:
            self.stop_logging()
            self._stop_reader.set()
            if not self.use_mock:
                self.ser.close() # Only closes if not in mock mode
            logging.info("Logging finished.")
    # ...
    ```

### 3. `core/interface/trials.py`

In the `run_trials` function, when a trial is initiated, the `VernierFSRLogger` is instantiated. For testing and demonstration purposes, it is explicitly set to `use_mock=True`.

```python
# core/interface/trials.py
# ...
                    try:
                        # Set use_mock=True for testing without a physical Arduino
                        logger = VernierFSRLogger(use_mock=True) 
                    except Exception as e:
# ...
```

### 4. `core/utils/mock_data.py`

This dedicated file contains the `generate_mock_data()` function, which produces realistic-looking simulated sensor readings.

```python
# core/utils/mock_data.py
import random
import time
from datetime import datetime

def generate_mock_data():
    """
    Generate a mock data line simulating sensor readings.
    """
    # ... (logic to generate random sensor values)
```

## Switching Between Mock and Real Runs

To switch between mock and real Arduino runs, you primarily need to adjust one line in `core/interface/trials.py`:

1.  **For Mock Runs (No Arduino Needed):**

    Keep the line as it is:

    ```python
    logger = VernierFSRLogger(use_mock=True)
    ```

    This forces the logger to use simulated data, regardless of whether an Arduino is detected.

2.  **For Real Arduino Runs (Requires Physical Arduino):**

    Change the line to:

    ```python
    logger = VernierFSRLogger(use_mock=False)
    ```

    Or simply:

    ```python
    logger = VernierFSRLogger()
    ```

    (since `use_mock` defaults to `False`). In this mode, the application will attempt to find and connect to a physical Arduino. If no Arduino is found, it will automatically fall back to mock mode, as handled by `core/hardware/detector.py` and `core/logging/logger.py`.

By making this small change, you can easily toggle between development/testing and live data collection.