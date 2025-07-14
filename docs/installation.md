
# Installation Guide

This guide will walk you through the process of setting up the PreSure application on your computer. No prior programming experience is required.

## Step 1: Install Python

Python is the programming language that powers PreSure. To install it, follow these steps:

1.  **Download Python:** Visit the official [Python website](https://www.python.org/downloads/) and download the latest version for your operating system (Windows, macOS, or Linux).
2.  **Run the Installer:** Open the downloaded file and follow the on-screen instructions. **Important:** On Windows, make sure to check the box that says "Add Python to PATH."

## Step 2: Install Git

Git is a tool that helps manage and download the project's source code. Here’s how to install it:

1.  **Download Git:** Go to the [Git website](https://git-scm.com/downloads) and download the version for your operating system.
2.  **Run the Installer:** Open the downloaded file and follow the on-screen instructions, accepting the default settings.

## Step 3: Download the PreSure Application

Now, you will download the PreSure application using Git.

1.  **Open the Terminal (or Command Prompt):**
    *   **Windows:** Press the Windows key, type `cmd`, and press Enter.
    *   **macOS:** Open the Launchpad and search for "Terminal."
2.  **Clone the Repository:** In the terminal, type the following command and press Enter:

    ```
    git clone https://github.com/your-username/pressure-ui.git
    ```

    This will create a new folder named `pressure-ui` on your computer.

## Step 4: Install Dependencies

Next, you need to install the additional libraries that PreSure relies on.

1.  **Navigate to the Project Directory:** In the terminal, type the following command and press Enter:

    ```
    cd pressure-ui
    ```

2.  **Install the Libraries:** Run the following command to install the required libraries:

    ```
    pip install -r requirements.txt
    ```

## Step 5: Run the Application

Once the installation is complete, you can run the application.

1.  **Launch the App:** In the terminal, run the following command:

    ```
    streamlit run app.py
    ```

2.  **Access the Interface:** The application will open in your web browser automatically. If it doesn't, you can access it at the URL displayed in the terminal (usually `http://localhost:8501`).

## Troubleshooting

- **Command Not Found:** If you see a "command not found" error, it likely means that Python or Git was not installed correctly. Make sure to follow the installation steps carefully.
- **Permission Denied:** If you encounter a "permission denied" error, you may need to run the terminal as an administrator (on Windows) or use `sudo` (on macOS and Linux).

If you run into any issues, please don't hesitate to reach out for help.
