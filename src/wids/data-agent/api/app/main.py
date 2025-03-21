import os
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import (
    RegisterTortoise,
    tortoise_exception_handlers,
)
from app import create_application
from app.routes import chat_router, ping_router
from app.dependencies.db import register_orm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cool.api")


@asynccontextmanager
async def lifespan_test(app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        os.environ.get("DATABASE_TEST_URL", "sqlite://:memory:"),
        app_modules={"models": ["app.models.tortoise"]},
        testing=True,
        connection_label="models",
    )
    async with RegisterTortoise(
        app=app, config=config, generate_schemas=True, _create_db=True
    ):
        yield

    await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up...")
    if getattr(app.state, "testing", None):
        async with lifespan_test(app) as _:
            yield
    else:
        async with register_orm(app):
            yield
    logger.info("Shutting down...")


app = create_application(
    lifespan_handler=lifespan,
    exception_handlers=tortoise_exception_handlers(),
    routes=[chat_router, ping_router],
)
