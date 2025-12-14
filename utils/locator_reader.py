import os
import json

# Path to locators.json
BASE_DIR = os.getcwd()
LOCATORS_PATH = os.path.join(BASE_DIR, "resources/locators/locators.json")

def load_locators():
    """Load locators.json file and return as a dictionary."""
    if not os.path.exists(LOCATORS_PATH):
        raise FileNotFoundError(f"Locators file not found at: {LOCATORS_PATH}")

    with open(LOCATORS_PATH, "r") as file:
        return json.load(file)

LOCATORS = load_locators()
