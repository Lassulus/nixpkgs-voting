from typing import Any

from .base import BaseBallotClass, BasePollClass


class Poll(BasePollClass):
    def __init__(self) -> None:
        super().__init__(poll_type="yesno")

    def get_results(self) -> dict[str, Any]:
        yes = 0
        no = 0
        for ballot in self.ballots:
            if ballot.data["vote"] == "yes":
                yes += 1
            elif ballot.data["vote"] == "no":
                no += 1
        return {
            "yes": yes,
            "no": no,
            "winner": "yes" if yes > no else "no",
            "total": yes + no,
            "ratio_yes": yes / (yes + no),
            "ratio_no": no / (yes + no),
        }


class Ballot(BaseBallotClass):
    def vote(self, data: dict[str, Any]) -> None:
        if data["vote"] in ["yes", "no"]:
            self.data = data
        else:
            raise ValueError("Vote must be either 'yes' or 'no'")
