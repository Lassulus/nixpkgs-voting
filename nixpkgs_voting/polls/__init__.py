import importlib
import json
import os
from pathlib import Path

from . import yesno

# add all poll/ballot types here
Poll = yesno.Poll
Ballot = yesno.Ballot


def get_public_polls() -> list:
    poll_directory = Path(os.environ["POLL_DIRECTORY"])
    polls = []
    for poll_id in poll_directory.iterdir():
        poll_file = poll_id / "poll.json"
        if poll_file.exists():
            poll_data = json.loads(poll_file.read_text())
            poll_module = importlib.import_module(
                f"nixpkgs_voting.polls.{poll_data['type']}"
            )
            poll = poll_module.Poll(**poll_data)
            polls.append(poll)
    return polls


def get_poll_by_id(id: str) -> Poll:
    poll_directory = Path(os.environ["POLL_DIRECTORY"])
    poll_file = poll_directory / id / "poll.json"
    poll_data = json.loads(poll_file.read_text())
    poll_module = importlib.import_module(f"nixpkgs_voting.polls.{poll_data['type']}")
    poll = poll_module.Poll(**poll_data)
    return poll
