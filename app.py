from core.interface.form import input_form
from core.interface.trials import run_trials
from core.logging.logger import VernierFSRLogger



def main():
    config = input_form()
    if config:
        run_trials(config)

if __name__ == "__main__":
    main()
