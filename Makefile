# Makefile

# Define the paths to your server and client files
SERVER_FILE = app/server.py
CLIENT_FILE = app/client.py

# Define the name for your Docker image
IMAGE_NAME = my-fastapi-app

# Define the path to your test folder
TEST_FOLDER = tests

# Define virtual environment
VENV = venv

.PHONY: run-server run-client build-image run-tests setup

run-server:
	$(VENV)/bin/python $(SERVER_FILE)

run-client:
	$(VENV)/bin/python $(CLIENT_FILE)

build-image:
	docker build -t $(IMAGE_NAME) .

run-tests:
	$(VENV)/bin/python -m unittest discover $(TEST_FOLDER)

setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

clean:
	rm -rf $(VENV)

help:
	@echo "Available make targets:"
	@echo "  run-server       - Start the server"
	@echo "  run-client       - Run the client"
	@echo "  build-image      - Build Docker image"
	@echo "  run-tests        - Run unit tests"
	@echo "  setup            - Set up virtual environment and install requirements"
	@echo "  clean            - Clean up virtual environment"
	@echo "  help             - Display this help message"
