import streamlit as st


def input_form():
    """
    Displays a styled form for trial setup.
    """
    st.set_page_config(layout="wide", page_title="PreSure Trial Setup", page_icon="🧪")

    st.title("🧪 PreSure Trial Setup")
    st.markdown("Configure the parameters for your experimental trials below.")

    with st.form("trial_input_form"):
        st.subheader("Basic Configuration")

        col1, col2 = st.columns(2)
        with col1:
            directory = st.text_input(
                "📁 Directory Name",
                placeholder="e.g., Experiment_Alpha",
                help="Name of the main folder to store all trial data.",
            )
            num_trials = st.number_input(
                "🔄 Number of Trials",
                min_value=1,
                value=1,
                step=1,
                help="How many times to repeat the experiment for each location and type.",
            )
        with col2:
            num_locations = st.number_input(
                "📍 Number of Locations",
                min_value=1,
                value=1,
                step=1,
                help="How many different sensor positions will be tested.",
            )
            lump_options = st.multiselect(
                "🧊 Select Trial Types",
                options=["LUMP", "NOLUMP"],
                default=["LUMP", "NOLUMP"],
                help="Select the conditions you want to test.",
            )

        st.subheader("Advanced Settings")
        with st.expander("Adjust timing and delay settings", expanded=True):
            col1_adv, col2_adv = st.columns(2)
            with col1_adv:
                duration = st.slider(
                    "⏱️ Logging Duration (seconds)",
                    min_value=5,
                    max_value=120,
                    value=10,
                    help="How long to record data for each trial.",
                )
            with col2_adv:
                delay = st.slider(
                    "⏳ Start Delay (seconds)",
                    min_value=0,
                    max_value=10,
                    value=2,
                    help="A countdown before the logging begins.",
                )

        st.markdown("---")
        submitted = st.form_submit_button("✅ Start Setup", use_container_width=True)

        if submitted:
            if not directory.strip():
                st.warning("⚠️ Please enter a directory name before proceeding.")
                return None

            # Store the configuration in a dictionary
            config = {
                "directory": directory,
                "num_trials": num_trials,
                "num_locations": num_locations,
                "lump_options": lump_options,
                "duration": duration,
                "delay": delay,
            }

            st.success("Configuration saved! Proceeding to trial execution.")
            st.balloons()

            return config

    return None
