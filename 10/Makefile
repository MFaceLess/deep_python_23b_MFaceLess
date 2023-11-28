PYTHON := python3
VENV_DIR := venv
SETUP_FILE := setup.py
TEST_FILE := test_cjson.py
TEST_PERFORMANCE_FILE := test_performance.py


all: venv install test

venv:
	$(PYTHON) -m venv $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && $(MAKE) install-dependencies

install:
	. $(VENV_DIR)/bin/activate && $(PYTHON) $(SETUP_FILE) install

install-dependencies:
	$(VENV_DIR)/bin/pip install -r requirements.txt

test:
	. $(VENV_DIR)/bin/activate && $(PYTHON) -m unittest $(TEST_FILE)

test_performance:
	. $(VENV_DIR)/bin/activate && $(PYTHON) $(TEST_PERFORMANCE_FILE)

clear:
	rm -rf $(VENV_DIR)
	rm -rf build
	rm -rf __pycache__
	rm -rf dist
	rm -rf cjons.egg-info