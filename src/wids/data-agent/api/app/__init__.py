import os

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.routes import ping


def create_application() -> FastAPI:
    app = FastAPI(
        title="Secret Agent API",
        description="API for demoing the multi-agent killer",
        version="0.1.0",
    )

    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

    app.include_router(ping.router)

    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}

    return app
