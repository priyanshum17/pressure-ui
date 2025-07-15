# Architecture Overview

This document provides a high-level overview of the project's architecture.

## Directory Structure

-   `app.py`: The main entry point for the Streamlit application.
-   `core/`: Contains the core application logic, separated into sub-modules:
    -   `config/`: Handles application configuration.
    -   `hardware/`: Interacts with the pressure sensor hardware.
    -   `interface/`: Defines the Streamlit user interface components.
    -   `logging/`: Configures and manages logging.
    -   `utils/`: Provides utility functions used across the application.
-   `data/`: Stores the raw and cleaned data from the pressure sensor trials.
-   `docs/`: Contains project documentation.
-   `tests/`: Contains the test suite for the project.

## Data Flow

1.  **Data Acquisition**: The `core/hardware/detector.py` script interacts with the sensor hardware to collect pressure data.
2.  **Data Storage**: The raw data is saved to the `data/` directory.
3.  **Data Processing**: The data is cleaned and processed, with the results saved to new files in the `data/` directory.
4.  **Data Visualization**: The `core/interface/charts.py` script reads the cleaned data, processes it into a DataFrame, and displays it in the Streamlit application.
