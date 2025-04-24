import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from router import language, gen, version, versionGroup, ability, pokemon, game

api = FastAPI(title="pokemonle api")
api.include_router(language.router)
api.include_router(gen.router)
api.include_router(version.router)
api.include_router(versionGroup.router)
api.include_router(ability.router)
api.include_router(pokemon.router)
api.include_router(game.router)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/", include_in_schema=False)
async def index() -> str:
    return "Hello Pokemonle"

class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        if response.status_code == 404:
            response = await super().get_response('index.html', scope)
        return response

app = FastAPI()
app.mount("/api", api)
app.mount("/", SPAStaticFiles(directory="dist", html=True), name="static")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9000)
