import streamlit as st
import time
from pathlib import Path
from core.config.setting import settings
from core.utils.generator import filename_generator
from core.logging.logger import VernierFSRLogger

def run_trials(config):
    st.title("🔬 Run Trials")
    st.markdown("Here is the list of all generated trials. Run them one by one.")

    filenames = filename_generator(
        config["num_trials"],
        config["num_locations"],
        config["lump_options"]
    )

    st.info(f"**Total Trials Generated:** {len(filenames)}")

    # Create a container for each trial to keep the layout clean
    for i, trial_name in enumerate(filenames):
        with st.container():
            st.subheader(f"Trial {i + 1}: {trial_name}")
            
            # Use columns for a more organized layout
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(
                    f"**Directory:** `{config['directory']}/{trial_name}`<br>"
                    f"**Duration:** `{config['duration']}s`  **Delay:** `{config['delay']}s`",
                    unsafe_allow_html=True
                )
            
            with col2:
                # Use a unique key for each button to avoid conflicts
                if st.button(f"Run Trial", key=f"run_{trial_name}", use_container_width=True):
                    base_dir = Path(settings.DATA_DIRECTORY) / config["directory"]
                    trial_dir = base_dir / trial_name
                    trial_dir.mkdir(parents=True, exist_ok=True)

                    try:
                        # Set use_mock=True for testing without a physical Arduino
                        logger = VernierFSRLogger(use_mock=False) 
                    except Exception as e:
                        st.error(f"Logger initialization failed for {trial_name}: {e}")
                        continue

                    # Use an empty placeholder for the progress bar
                    progress_placeholder = st.empty()
                    start_time = time.time()

                    try:
                        logger.run(
                            duration_seconds=config["duration"],
                            start_delay=config["delay"],
                            save_dir=trial_dir,
                            file_stem=trial_name
                        )

                        # Update the progress bar in the placeholder
                        for t in range(config["duration"]):
                            elapsed = time.time() - start_time
                            progress_value = min(elapsed / config["duration"], 1.0)
                            progress_placeholder.progress(
                                progress_value,
                                text=f"⏳ Running {trial_name}... {int(elapsed)}/ {config['duration']}s"
                            )
                            time.sleep(1)
                        
                        progress_placeholder.empty()
                        st.success(f"✅ Trial {trial_name} completed successfully.")

                    except Exception as e:
                        progress_placeholder.empty()
                        st.error(f"❌ Trial {trial_name} failed: {e}")

            st.markdown("<hr>", unsafe_allow_html=True)
