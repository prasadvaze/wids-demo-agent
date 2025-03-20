from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Secret Agent API",
        description="API for demoing the multi-agent killer",
        version="0.1.0",
    )

    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}

    return app
