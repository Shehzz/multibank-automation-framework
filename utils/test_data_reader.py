import os
import json

# Path to test_data.json
BASE_DIR = os.getcwd()
TEST_DATA_PATH = os.path.join(BASE_DIR, "config/test_data.json")

def load_test_data():
    """Load test_data.json file and return as a dictionary."""
    if not os.path.exists(TEST_DATA_PATH):
        raise FileNotFoundError(f"Test data file not found at: {TEST_DATA_PATH}")

    with open(TEST_DATA_PATH, "r") as file:
        return json.load(file)

TEST_DATA = load_test_data()
