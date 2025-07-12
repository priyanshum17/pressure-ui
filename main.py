import streamlit as st
from core.logger import run_logger_session
from core.directory import ensure_subdirectory
import os

def initialize_session_state():
    if "trial_configs" not in st.session_state:
        st.session_state.trial_configs = []
    if "current_trial_index" not in st.session_state:
        st.session_state.current_trial_index = 0
    if "experiment_running" not in st.session_state:
        st.session_state.experiment_running = False

def input_form():
    st.title("PreSure Trial Setup Interface")

    with st.form("presure_form"):
        directory = st.text_input("Directory Name", placeholder="Enter the directory name")
        num_trials = st.number_input("Number of Trials", min_value=1, value=1, step=1)
        num_locations = st.number_input("Number of Locations", min_value=1, value=1, step=1)
        lump_options = st.multiselect(
            "Select trial types to include:",
            options=["Lump", "No Lump"],
            default=["Lump", "No Lump"],
        )
        with st.expander("Advanced Settings"):
            duration = st.slider("Logging Duration (seconds)", min_value=10, max_value=120, value=30, step=1)
            delay = st.slider("Start Delay (seconds)", min_value=0, max_value=10, value=0, step=1)

        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted:
            if not lump_options:
                st.warning("Please select at least one option for trial type.")
                return
            
            st.session_state.experiment_running = True
            st.session_state.current_trial_index = 0
            st.session_state.trial_configs = []
            
            for trial_no in range(1, num_trials + 1):
                for loc_no in range(1, num_locations + 1):
                    for lump_type in lump_options:
                        trial_name = f"{trial_no}_{loc_no}_{lump_type.replace(' ', '')}"
                        st.session_state.trial_configs.append({
                            "name": trial_name,
                            "duration": duration,
                            "delay": delay,
                            "base_directory": directory
                        })

def trial_runner():
    if not st.session_state.experiment_running or not st.session_state.trial_configs:
        return

    idx = st.session_state.current_trial_index
    if idx >= len(st.session_state.trial_configs):
        st.success("All trials completed!")
        st.session_state.experiment_running = False
        if st.button("Start New Experiment"):
            st.session_state.clear()
        return

    trial = st.session_state.trial_configs[idx]
    st.subheader(f"Upcoming Trial: {trial['name']}")
    
    if st.button(f"Start Trial {idx + 1} of {len(st.session_state.trial_configs)}", key=f"start_{idx}"):
        with st.spinner(f"Running trial: {trial['name']}..."):
            try:
                if not os.path.exists(trial['base_directory']):
                    os.makedirs(trial['base_directory'])

                trial_dir = ensure_subdirectory(trial['base_directory'], trial['name'])
                
                run_logger_session(
                    duration=trial['duration'],
                    delay=trial['delay'],
                    experiment_name=trial_dir 
                )
                st.success(f"Trial {trial['name']} completed and data saved in '{trial_dir}'.")
                st.session_state.current_trial_index += 1

            except Exception as e:
                st.error(f"An error occurred during the trial: {e}")

def main():
    initialize_session_state()

    if not st.session_state.experiment_running:
        input_form()
    else:
        trial_runner()
        if st.button("Reset and Start Over"):
            st.session_state.clear()

if __name__ == "__main__":
    main()
