import os
import subprocess

import uvicorn
from typing import Any, AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference
from starlette.responses import HTMLResponse
from router import language, gen, version, versionGroup, ability, pokemon, game

from conf.env import settings


async def run_database_migrations():
    """Run database migrations by calling alembic."""
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except subprocess.CalledProcessError as e:
        # logger.error(f"Failed to run database migrations: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    await run_database_migrations()

    yield


app = FastAPI(title="pokemonle api", lifespan=lifespan)

api = APIRouter(prefix="/api")
api.include_router(language.router)
api.include_router(gen.router)
api.include_router(version.router)
api.include_router(versionGroup.router)
api.include_router(ability.router)
api.include_router(pokemon.router)
api.include_router(game.router)

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scalar", include_in_schema=False)
async def scalar_html() -> HTMLResponse:
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('index.html', scope)
        return response


app.mount("/", SPAStaticFiles(directory="dist", html=True), name="static")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
