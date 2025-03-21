from fastapi import FastAPI, APIRoute
from starlette.types import Lifespan
from starlette.exceptions import ExceptionHandler


def create_application(
    lifespan_handler: Lifespan | None = None,
    exception_handlers: dict[int, ExceptionHandler] | None = None,
    routes: list[APIRoute] | None = None,
) -> FastAPI:
    app = FastAPI(
        title="Secret Agent API",
        description="API for demoing the multi-agent killer",
        version="0.1.0",
        lifespan=lifespan_handler,
        exception_handlers=exception_handlers,
    )

    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}

    if routes:
        for route in routes:
            app.include_router(route)

    return app
