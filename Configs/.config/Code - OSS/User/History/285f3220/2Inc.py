import openai
import json
import argparse
SETTINGS_FILE = 'settings.json'

parser = argparse.ArgumentParser(description="TerminalGPT")
parser.add_argument('-t', '--token', help="Token")