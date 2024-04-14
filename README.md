# nixpkgs-voting

This is a very early prototype of a nixpkgs-voting prototype. We plan to implement a bunch of different poll techniques and allow for anonymous voting.

Right now this is not usable yet

the rough design document:

- polls have certain options:
    - mode (public, anonymous, userspecified)
        - in public mode, every ballot is logged with the github id of the voter
        - in anonymous, the public data is scrapped, the poll id is a hash of the poll id, the voter id and a secret value for anonymization
        - in userspecified, voters can opt in to add their pulic information to the ballot
    - eligable voters
        - everyone
        - the nixos foundation board
        - maintainers from nixpkgs
        - people with 3 commits in the last year
        - custom (poll creator can specify list)
    - optional end date
        - the date when the poll will be closed and votes cannot be added/changed anymore
    - listed
        - if the poll should be listed in the global list of polls
        - maybe we restrict this at a later point to not spam the front page?
    - poll mode
        - polls have different modes (berber is the expert on that)
        - for the start we just have one or two simple modes:
            - yes/no/no-answer
            - choose one of x
            -

- storage ideas:
    - polls will be persisted in a file based structure:
        - $pollid/poll.json (for the poll settings)
        - $pollid/ballots/$ballotid.json (the ballotid is the anonymized id)
    - users should be able to download a tarball of the poll data if they have the link to the poll
    -
- there should be links to a poll (maybe embedable?)
- authorization should be via github app.
