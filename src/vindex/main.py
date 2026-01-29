from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from vindex.api.routes import router
from vindex.core.database import engine
from vindex.core.exceptions import VehicleAlreadyExistsError, VehicleNotFoundError
from vindex.models.vehicle import Base

app = FastAPI(title="VINdex")

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if error.get("type") == "json_invalid":
            return JSONResponse(status_code=400, content={"detail": "Invalid JSON"})
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@app.exception_handler(VehicleNotFoundError)
async def vehicle_not_found_handler(request: Request, exc: VehicleNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Vehicle with VIN '{exc.vin}' not found"},
    )


@app.exception_handler(VehicleAlreadyExistsError)
async def vehicle_already_exists_handler(
    request: Request, exc: VehicleAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={"detail": f"Vehicle with VIN '{exc.vin}' already exists"},
    )
