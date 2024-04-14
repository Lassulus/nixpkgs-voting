import datetime
import os

from fastapi import FastAPI, HTTPException, Request, Response, Security
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyCookie
from fastapi_sso.sso.base import OpenID
from fastapi_sso.sso.github import GithubSSO
from jose import jwt


async def get_logged_user(cookie: str = Security(APIKeyCookie(name="token"))) -> OpenID:
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # secret key for signing cookies
    """Get user's JWT stored in cookie 'token', parse it and return the user's OpenID."""
    try:
        claims = jwt.decode(cookie, key=JWT_SECRET_KEY, algorithms=["HS256"])
        return OpenID(**claims["pld"])
    except Exception as error:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        ) from error


def add_authentication(app: FastAPI) -> FastAPI:
    GITHUB_CLIENT_ID = os.environ["GITHUB_CLIENT_ID"]
    GITHUB_CLIENT_SECRET = os.environ["GITHUB_CLIENT_SECRET"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # secret key for signing cookies

    sso = GithubSSO(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_uri="http://localhost:5000/auth/callback",
        allow_insecure_http=True,
    )

    @app.get("/auth/login")
    async def auth_init() -> RedirectResponse:
        """Initialize auth and redirect"""
        with sso:
            return await sso.get_login_redirect()

    @app.get("/auth/logout")
    async def logout() -> Response:
        """Forget the user's session."""
        response = RedirectResponse(url="/prot")
        response.delete_cookie(key="token")
        return response

    @app.get("/auth/callback")
    async def auth_callback(request: Request) -> RedirectResponse:
        """Verify login"""
        with sso:
            openid = await sso.verify_and_process(request)
            if not openid:
                raise HTTPException(status_code=401, detail="Authentication failed")
        # Create a JWT with the user's OpenID
        expiration = datetime.datetime.now(tz=datetime.UTC) + datetime.timedelta(days=1)
        token = jwt.encode(
            {"pld": openid.dict(), "exp": expiration, "sub": openid.id},
            key=JWT_SECRET_KEY,
            algorithm="HS256",
        )
        response = RedirectResponse(url="/")
        response.set_cookie(
            key="token", value=token, expires=expiration
        )  # This cookie will make sure we know the user
        return response

    return app
