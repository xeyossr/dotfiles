import openai
import json
import argparse
import os
SETTINGS_FILE = 'settings.json'

parser = argparse.ArgumentParser(description="TerminalGPT")
parser.add_argument('-t', '--token', help="Token")
args = parser.parse_args()

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump({}, settings_file, indent=4)

