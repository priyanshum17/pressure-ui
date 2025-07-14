import streamlit as st

def input_form():
    st.title("PreSure Trial Setup")

    with st.form("trial_input_form"):
        directory = st.text_input("Directory Name", placeholder="Enter the directory name")
        num_trials = st.number_input("Number of Trials", min_value=1, value=1, step=1)
        num_locations = st.number_input("Number of Locations", min_value=1, value=1, step=1)
        lump_options = st.multiselect(
            "Select trial types:",
            options=["LUMP", "NOLUMP"],
            default=["LUMP", "NOLUMP"]
        )
        with st.expander("Advanced Settings"):
            duration = st.slider("Logging Duration (seconds)", min_value=10, max_value=120, value=30)
            delay = st.slider("Start Delay (seconds)", min_value=0, max_value=10, value=0)

        submitted = st.form_submit_button("Submit", use_container_width=True)

        if submitted:
            if not directory.strip():
                st.warning("Please enter a directory name before proceeding.")
                return None

            st.subheader("Submitted Input")
            st.write(f"Directory: {directory}")
            st.write(f"Trials: {num_trials}")
            st.write(f"Locations: {num_locations}")
            st.write(f"Trial Types: {lump_options}")
            st.write(f"Duration: {duration} seconds")
            st.write(f"Delay: {delay} seconds")

            return {
                "directory": directory,
                "num_trials": num_trials,
                "num_locations": num_locations,
                "lump_options": lump_options,
                "duration": duration,
                "delay": delay,
            }

    return None