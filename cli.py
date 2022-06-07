#!venv/bin/python
import argparse
from winamax import Winamax
from winamax import utils
import json

parser = argparse.ArgumentParser()
parser.add_argument("action")
parser.add_argument("--type", default=None)
parser.add_argument("--sport_id", default=None)
parser.add_argument("--category_id", default=None)
parser.add_argument("--tournament_id", default=None)
parser.add_argument("--match_id", default=None)
parser.add_argument("--outcome_id", default=None)
parser.add_argument("--check_id", default=None)

args = parser.parse_args()


class Cli:
    def __init__(self, args):
        self.args = args
        self.winamax = Winamax()

    def update_sports(self, **kwargs):
        self.winamax.update_sports()

    def update_next_tournament(self, **kwargs):
        self.winamax.update_next_tournament()

    def update_tournament(self, **kwargs):
        self.winamax.update_tournament(args.sport_id, args.category_id, args.tournament_id)

    def check_match(self, **kwargs):
        print(self.winamax.check_match(args.match_id, Winamax.get_check(args.check_id)))

    def delete_match_marks(self, **kwargs):
        print(self.winamax.delete_match_marks(args.match_id))

    def bet(self, **kwargs):
        print(self.winamax.bet(args.outcome_id))

    def send_mail(self):
        utils.send_mail("coucou", 
            """
            Coucou

            Hello lala
        """)

    def test(self, **kwargs):
        self.winamax.test()

    def purge(self, **kwargs):
        self.winamax.purge()

    """
    def take_outcomes_snapshot(self, **kwargs):
        self.winamax.take_outcomes_snapshot()

    def clean_outcome_history(self, **kwargs):
        self.winamax.clean_outcome_history()
    """



cli = Cli(args)
getattr(cli, args.action)()


