from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.api_v1.api import api_router
from .core.config import settings
from .db.session import session_db

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f'{settings.API_V1_STR}/openapi.json'
)


@app.on_event('startup')
def on_startup() -> None:
    session_db()


@app.get('/ping')
def pong() -> dict[str, str]:
    return {'ping': 'pong!'}


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
