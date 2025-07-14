# Chart Generation and Data Visualization Explained

This document provides a technical overview of how the `charts.py` script processes and visualizes the sensor data. It is intended for developers who want to understand the data pipeline from file discovery to final chart rendering.

---

### 1. Data Discovery and Loading

The data loading process begins by scanning the specified data directory for all files that match the `CLEAN_*.csv` pattern. This is done recursively, so it will find files in any subdirectory.

- **File Discovery**: The script uses `pathlib.Path.rglob("CLEAN_*.csv")` to find all relevant files. This returns a list of `Path` objects, each pointing to a clean data file.

- **Metadata Extraction**: For each file found, a regular expression (`r"CLEAN_TRIAL_(\d+)_LOC_(\d+)_(LUMP|NOLUMP)\.csv"`) is used to extract key metadata from the filename. This pattern captures three critical pieces of information:
    1.  **Trial Number**: The numeric identifier for the trial.
    2.  **Location Number**: The sensor quadrant where the reading was taken.
    3.  **Condition**: Whether the trial was conducted with a "LUMP" or "NOLUMP".

- **DataFrame Creation**: Each CSV file is read into a pandas DataFrame using `pd.read_csv()`. To keep the data focused, only the `Time(s)` and `D` columns are retained. The extracted metadata (trial, location, condition) and the relative path of the source file are then added as new columns to this DataFrame.

- **Concatenation**: After processing all individual files, the script concatenates the list of individual DataFrames into a single, master DataFrame. This unified DataFrame is then displayed in the Streamlit app using `st.dataframe()`.

### 2. Data Analysis and Visualization

Once the master DataFrame is loaded, the script performs several analysis and visualization steps:

- **Summary Statistics**: The script calculates summary statistics for each sensor quadrant (`Q1` through `Q4`) under both "LUMP" and "NOLUMP" conditions. This is done by grouping the data by `condition` and `quadrant` and then calculating the `mean`, `median`, and `standard deviation` for the "D" sensor values.

- **Summary Table**: The calculated summary statistics are presented in a clear, tabular format using a pandas DataFrame, which is then displayed in the Streamlit app.

- **Variability Metrics**: To compare the variability between quadrants, the script computes three key metrics for each condition:
    - **Inter-quadrant Range**: The difference between the maximum and minimum average sensor readings across the four quadrants.
    - **Standard Deviation**: The standard deviation of the average sensor readings across the quadrants.
    - **Coefficient of Variation (CV)**: A normalized measure of dispersion, calculated as `(standard deviation / mean) * 100`.

- **Heatmaps**: The final visualization is a pair of heatmaps that show the average sensor "D" reading for each quadrant, with one heatmap for the "LUMP" condition and one for the "NOLUMP" condition. The heatmaps are generated using `seaborn.heatmap()` and are annotated with the quadrant and its average reading.

This entire process is designed to be automatic and data-driven, allowing you to easily analyze new trial data by simply placing the files in the data directory.
