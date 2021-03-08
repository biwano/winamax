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
        self.winamax.update_cache()

    def take_outcomes_snapshot(self, **kwargs):
        self.winamax.take_outcomes_snapshot()

    def clean_outcome_history(self, **kwargs):
        self.winamax.clean_outcome_history()


cli = Cli(args)
getattr(cli, args.action)()


