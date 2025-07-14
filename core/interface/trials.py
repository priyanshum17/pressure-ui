import streamlit as st
import time
from pathlib import Path
from core.config.setting import settings
from core.utils.generator import filename_generator
from core.logging.logger import VernierFSRLogger


def run_trials(config):
    st.title("Run Trials")

    filenames = filename_generator(
        config["num_trials"],
        config["num_locations"],
        config["lump_options"]
    )

    # Get current trial index from URL query param
    trial_index = int(st.query_params().get("trial", [0])[0])

    if trial_index >= len(filenames):
        st.success("All trials completed.")
        return

    trial_name = filenames[trial_index]
    base_dir = Path(settings.DATA_DIRECTORY) / config["directory"]
    trial_dir = base_dir / trial_name
    trial_dir.mkdir(parents=True, exist_ok=True)

    st.subheader(f"Trial {trial_index + 1} of {len(filenames)}: {trial_name}")

    if st.button("Start This Trial", use_container_width=True):
        try:
            logger = VernierFSRLogger()
        except Exception as e:
            st.error(f"Logger initialization failed: {e}")
            _show_next_button(trial_index + 1)
            return

        progress = st.progress(0, text="Running logger...")
        start_time = time.time()

        try:
            logger.run(
                duration_seconds=config["duration"],
                start_delay=config["delay"],
                save_dir=trial_dir,
                file_stem=trial_name
            )

            for t in range(config["duration"]):
                elapsed = time.time() - start_time
                progress.progress(
                    min(elapsed / config["duration"], 1.0),
                    text=f"Time left: {config['duration'] - int(elapsed)}s"
                )
                time.sleep(1)

            progress.empty()
            st.success(f"Trial {trial_name} completed.")

        except Exception as e:
            progress.empty()
            st.error(f"Trial failed with error: {e}")

        _show_next_button(trial_index + 1)


def _show_next_button(next_index: int):
    st.markdown("---")
    if st.button("Next Trial", use_container_width=True):
        st.query_params(trial=str(next_index))
        st.rerun()
