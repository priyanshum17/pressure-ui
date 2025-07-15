import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def display_charts(data_directory: Path):
    st.title("Analysis")
    st.markdown("Analyzing quadrant sensor values from CLEAN FSR logs.")

    logging.info(f"Searching for CLEAN_*.csv files in: {data_directory.resolve()}")
    csv_files = list(data_directory.rglob("CLEAN_*.csv"))

    if not csv_files:
        st.warning(f"No CLEAN_*.csv files found in {data_directory.resolve()}.")
        logging.warning(f"No files found in {data_directory.resolve()}.")
        return

    st.subheader("DataSet")
    with st.expander("Detected clean files", expanded=False):
        st.subheader("Detected Clean Files")
        for f in csv_files:
            st.write(f"- `{f.relative_to(data_directory)}` (Exists: {f.exists()})")

    all_dfs = []
    pattern = r"^CLEAN_TRIAL_(\d+)_LOC_(\d+)_(LUMP|NOLUMP)\.csv$"  # <-- single backslash, anchored
    logging.info(f"Using regex pattern: {pattern}")

    for file_path in csv_files:
        relative_path = file_path.relative_to(data_directory)
        logging.info(f"Processing file: {relative_path}")
        logging.info(f"Full path: {file_path.resolve()}")
        logging.info(f"File exists: {file_path.exists()}")
        logging.info(f"Filename being matched: {file_path.name}")

        match = re.match(pattern, file_path.name)
        if not match:
            st.error(f"Regex mismatch for: `{relative_path}`")
            logging.error(f"Regex did not match for filename: {file_path.name}")
            continue

        logging.info(f"Regex matched for {file_path.name}! Groups: {match.groups()}")

        try:
            df = pd.read_csv(file_path)
            if "Time(s)" not in df.columns or "D" not in df.columns:
                st.warning(
                    f"Required columns ('Time(s)', 'D') not found in `{relative_path}`."
                )
                continue

            processed_df = df[["Time(s)", "D"]].copy()
            processed_df["source_file"] = str(relative_path)

            trial_num, loc, condition = match.groups()
            processed_df["trial_no"] = int(trial_num)
            processed_df["location_no"] = int(loc)
            processed_df["condition"] = condition

            all_dfs.append(processed_df)
        except Exception as e:
            st.error(f"Failed to parse or process {relative_path}: {e}")
            logging.error(f"Error processing {file_path.name}: {e}", exc_info=True)

    with st.expander("Data set preview", expanded=False):
        st.subheader("DataSet")
        if all_dfs:
            concatenated_df = pd.concat(all_dfs, ignore_index=True)
            cols = [
                "source_file",
                "trial_no",
                "location_no",
                "condition",
                "Time(s)",
                "D",
            ]
            st.dataframe(concatenated_df[cols])
        else:
            st.write("No data to display in DataFrame.")

    # --- Analysis Section ---
    st.subheader("Analysis & Visualizations")
    data = {}
    for file_path in csv_files:
        relative_path = file_path.relative_to(data_directory)
        match = re.search(pattern, file_path.name)
        if not match:
            # This should be consistent with the error above
            continue

        try:
            trial_num, loc, condition = match.groups()
            quadrant = f"Q{loc}"
            key = (condition, quadrant)
            df = pd.read_csv(file_path)
            if "D" not in df.columns:
                continue
            values = df["D"].astype(float)
            data.setdefault(key, []).append(values)
        except Exception:
            # Errors are already logged above, so we can be brief here
            st.warning(f"Skipping {relative_path} for analysis due to read error.")

    if not data:
        st.warning("No data was successfully parsed for analysis.")
        return

    # === STEP 3: Summary Stats ===
    summary = {"LUMP": {}, "NOLUMP": {}}
    for (condition, quadrant), trials in data.items():
        if not trials:
            continue
        combined = pd.concat(trials, axis=1)
        summary[condition][quadrant] = {
            "avg": round(combined.mean(axis=1).mean(), 1),
            "median": round(combined.median(axis=1).median(), 1),
            "std": round(combined.stack().std(), 1),
        }

    # === STEP 4: Summary Table ===
    st.subheader("Summary Statistics (Sensor D)")
    rows = []
    for condition in ["LUMP", "NOLUMP"]:
        for metric in ["avg", "median", "std"]:
            row = {"Condition": condition, "Metric": metric}
            for q in ["Q1", "Q2", "Q3", "Q4"]:
                row[q] = summary.get(condition, {}).get(q, {}).get(metric, np.nan)
            rows.append(row)
    st.dataframe(pd.DataFrame(rows))

    # === STEP 5: Variability Metrics ===
    def compute_metrics(summary_dict):
        quad_avgs = [
            summary_dict.get(q, {}).get("avg", np.nan) for q in ["Q1", "Q2", "Q3", "Q4"]
        ]
        quad_arr = np.array(quad_avgs)
        quad_arr_clean = quad_arr[~np.isnan(quad_arr)]
        if len(quad_arr_clean) >= 2:
            q_mean = np.mean(quad_arr_clean)
            q_std = np.std(quad_arr_clean)
            q_range = np.max(quad_arr_clean) - np.min(quad_arr_clean)
            q_cv = (q_std / q_mean) * 100 if q_mean != 0 else np.nan
            return q_range, q_std, q_cv
        return np.nan, np.nan, np.nan

    st.subheader("Intra-Quadrant Variability Comparison")

    # Build summary table
    variability_rows = []
    for cond in ["LUMP", "NOLUMP"]:
        r, s, c = compute_metrics(summary.get(cond, {}))
        variability_rows.append(
            {
                "Condition": cond,
                "Range (Max - Min)": f"{r:.1f}",
                "Standard Deviation": f"{s:.1f}",
                "Coefficient of Variation (CV)": f"{c:.2f} %",
            }
        )

    # Display as table
    st.table(pd.DataFrame(variability_rows))

    # === STEP 6: Heatmaps ===
    def grid(data_dict):
        return np.array(
            [
                [data_dict.get("Q2", np.nan), data_dict.get("Q1", np.nan)],
                [data_dict.get("Q3", np.nan), data_dict.get("Q4", np.nan)],
            ]
        )

    vmin = 0
    vmax = 60000
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    for i, cond in enumerate(["LUMP", "NOLUMP"]):
        avg_dict = {
            q: summary[cond].get(q, {}).get("avg", np.nan)
            for q in ["Q1", "Q2", "Q3", "Q4"]
        }
        data_grid = grid(avg_dict)
        labels = np.array(
            [
                [f"Q2\n{data_grid[0,0]:.1f}", f"Q1\n{data_grid[0,1]:.1f}"],
                [f"Q3\n{data_grid[1,0]:.1f}", f"Q4\n{data_grid[1,1]:.1f}"],
            ]
        )
        sns.heatmap(
            data_grid,
            annot=labels,
            fmt="",
            cmap="YlOrRd",
            vmin=vmin,
            vmax=vmax,
            xticklabels=False,
            yticklabels=False,
            cbar=True,
            ax=axs[i],
        )
        axs[i].set_title(f"{cond} - Sensor D")

    st.pyplot(fig)
