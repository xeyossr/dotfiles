import openai
import json
import argparse
import os
SETTINGS_FILE = 'settings.json'

def checkjson():
    with open(SETTINGS_FILE, 'r') as settings_file:
        token = settings_file['token']

if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, 'w') as settings_file:
        json.dump({}, settings_file, indent=4)

checkjson()
if not token:
    yourtoken = input("API KEY >")

parser = argparse.ArgumentParser(description="TerminalGPT")
parser.add_argument('-t', '--token', help="Token")
args = parser.parse_args()