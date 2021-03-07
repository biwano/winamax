#!venv/bin/python
import argparse
from winamax import Winamax
import json

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("--type", default=None)

args = parser.parse_args()


class Cli:
    def __init__(self, args):
        self.args = args
        self.winamax = Winamax()

    def update_cache(self, **kwargs):
        cache = args.type
        func = getattr(self.winamax, f"get_{cache}")
        with open(f'./storage/{cache}.json', 'w') as outfile:
            json.dump(func(), outfile, indent=4)

winamax=Winamax()

cli = Cli(args)
getattr(cli, args.action)()


