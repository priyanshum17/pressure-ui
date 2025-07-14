
# User Manual

Welcome to the PreSure User Manual. This guide will explain how to use the application to run trials and collect data.

## Screenshots                                                                                                                                                         │
| Setup Page | Trials Page | Analysis Page |
|:----------:|:-----------:|:-------------:|
| ![Setup Page](/docs/assets/setup.png) | ![Trials Page](/docs/assets/trials.png) | ![Analysis Page](/docs/assets/analysis.png) |


## Starting the Application

To start the application, open your terminal (or Command Prompt), navigate to the `pressure-ui` directory, and run the following command:

```
streamlit run app.py
```

The application will open in your web browser.

## Setting Up a Trial

When you first launch the application, you will see the **PreSure Trial Setup** form. Here, you can configure the parameters for your experiment.

-   **Directory Name:** Enter a name for the folder where your trial data will be saved.
-   **Number of Trials:** Specify how many times you want to run the experiment.
-   **Number of Locations:** Set the number of different locations or positions you will be testing.
-   **Trial Types:** Select the types of trials you want to run (e.g., with or without a lump).
-   **Advanced Settings:**
    -   **Logging Duration:** Adjust the slider to set the duration (in seconds) for each trial.
    -   **Start Delay:** Set a delay (in seconds) before each trial begins.

Once you have filled out the form, click the **Submit** button to proceed.

## Running a Trial

After submitting the trial setup, you will be taken to the **Run Trials** screen. Here, you will see a summary of the trial you are about to run.

1.  **Start the Trial:** Click the **Start This Trial** button to begin the data logging process.
2.  **Monitor Progress:** A progress bar will show the remaining time for the trial.
3.  **Trial Completion:** Once the trial is finished, a "Trial completed" message will appear.

## Moving to the Next Trial

After a trial is complete, a **Next Trial** button will appear. Click this button to proceed to the next trial in your experiment. The application will automatically advance to the next configuration until all trials have been completed.

## Mock Data Mode

If you are running the application without an Arduino connected, it will automatically switch to **Mock Data Mode**. In this mode, the application will generate simulated sensor data, allowing you to test the interface and workflow without a physical device.

## Data Analysis

All data collected during the trials will be saved in the directory you specified in the setup form. The data is stored in CSV format, which can be easily opened with spreadsheet software like Excel or Google Sheets for further analysis.

If you have any questions or need further assistance, please feel free to reach out.
