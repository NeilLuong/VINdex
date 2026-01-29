from fastapi import FastAPI

from vindex.api.routes import router

app = FastAPI(
    title="VINdex",
)

app.include_router(router)