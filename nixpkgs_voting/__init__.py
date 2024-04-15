import uvicorn
from fastapi import Depends, FastAPI
from fastapi_sso.sso.base import OpenID

from .auth import add_authentication, get_logged_user
from .polls import Poll, get_poll_by_id, get_public_polls


def main() -> None:
    app = FastAPI()

    app = add_authentication(app)

    @app.get("/")  # TODO: return a web interface here
    async def root(user: OpenID = Depends(get_logged_user)) -> OpenID:
        return user

    @app.get("/polls")
    async def get_polls() -> list:
        return get_public_polls()

    @app.post("/polls")
    async def create_poll(poll: Poll) -> Poll:
        poll.save()
        return poll

    @app.get("/polls/{poll_id}")
    async def get_poll(poll_id: str) -> Poll:
        return get_poll_by_id(poll_id)

    uvicorn.run(app=app, host="127.0.0.1", port=5000)


if __name__ == "__main__":
    main()
