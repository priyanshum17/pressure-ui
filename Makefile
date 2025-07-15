# Makefile for the Pressure UI project

.PHONY: all install test run clean

# Default target
all: install

# Install dependencies
install:
	@echo "Installing dependencies..."
	@pip install -r requirements.txt

# Run tests
test:
	@echo "Running tests..."
	@pytest

# Run the Streamlit application
run:
	@echo "Starting the application..."
	@streamlit run app.py

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@rm -rf .pytest_cache
