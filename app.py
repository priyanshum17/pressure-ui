import streamlit as st
from core.interface.form import input_form
from core.interface.trials import run_trials
from core.interface.charts import display_charts
from pathlib import Path

def main():
    # Use session state to manage the current page and configuration
    if "page" not in st.session_state:
        st.session_state.page = "setup"
    if "config" not in st.session_state:
        st.session_state.config = None

    # Page navigation logic
    if st.session_state.page == "setup":
        config = input_form()
        if config:
            st.session_state.config = config
            st.session_state.page = "trials"
            st.rerun()
    
    elif st.session_state.page == "trials":
        if st.session_state.config:
            run_trials(st.session_state.config)
            if st.button("Analyze Results", use_container_width=True):
                st.session_state.page = "analysis"
                st.rerun()
        else:
            st.warning("No configuration found. Please go back to the setup page.")
            if st.button("Go to Setup"):
                st.session_state.page = "setup"
                st.rerun()

    elif st.session_state.page == "analysis":
        if st.session_state.config:
            data_dir = Path("data") / st.session_state.config["directory"]
            display_charts(data_dir)
        else:
            st.warning("No configuration found. Please go back to the setup page.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Back to Trials", use_container_width=True):
                st.session_state.page = "trials"
                st.rerun()
        with col2:
            if st.button("Return to Setup", use_container_width=True):
                st.session_state.page = "setup"
                st.session_state.config = None # Reset config
                st.rerun()

if __name__ == "__main__":
    main()
