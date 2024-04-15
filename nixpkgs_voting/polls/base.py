import importlib
import json
import os
import uuid
from abc import ABC, abstractmethod
from hashlib import sha3_256
from pathlib import Path
from typing import Any

from pydantic import BaseModel


def ballot_id(poll_id: uuid.UUID, github_id: int) -> str:
    secret_key = os.environ["BALLOT_SECRET_KEY"]
    return sha3_256(f"{secret_key}{poll_id}{str(github_id)}".encode()).hexdigest()


class BaseBallotClass(BaseModel, ABC):
    id: str | None = None
    poll_id: uuid.UUID
    data: dict[str, Any] | None = None

    def calculate_id(self, github_id: int) -> None:
        self.id = ballot_id(self.poll_id, github_id)

    def save(self) -> None:
        if self.id is None:
            raise ValueError("Ballot ID not set")
        if self.data is None:
            raise ValueError("Ballot data not set")

        poll_directory = (
            Path(os.environ["POLL_DIRECTORY"]) / str(self.poll_id) / "ballots"
        )
        ballot_file = poll_directory / f"{self.id}.json"
        ballot_file.parent.mkdir(parents=True, exist_ok=True)
        ballot_file.write_text(self.model_dump_json())

    @abstractmethod
    def vote(self, data: dict[str, Any]) -> None:
        pass


class BasePollClass(BaseModel, ABC):
    id: uuid.UUID = uuid.uuid4()
    poll_data: dict = {}
    poll_type: str

    def __init__(self, poll_type: str):
        super().__init__(poll_type=poll_type)

    def save(self) -> None:
        poll_directory = Path(os.environ["POLL_DIRECTORY"])
        poll_file = poll_directory / f"{self.id}.json"
        poll_file.write_text(self.model_dump_json())

    @property
    def ballots(self) -> dict[str, BaseBallotClass]:
        ballots = {}
        ballots_directory = (
            Path(os.environ["POLL_DIRECTORY"]) / str(self.id) / "ballots"
        )
        for ballot_file in ballots_directory.iterdir():
            ballot_module = importlib.import_module(
                f"nixpkgs_voting.polls.{self.poll_type}"
            )
            ballot_data = json.loads(ballot_file.read_text())
            ballot = ballot_module.Ballot(**ballot_data)
            ballots[ballot.id] = ballot
        return ballots

    @ballots.setter
    def ballots(self, ballots: dict) -> None:
        for ballot in ballots:
            ballots[ballot].save()
