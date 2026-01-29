from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from vindex.api.dependencies import get_repository
from vindex.core.exceptions import VehicleNotFoundError
from vindex.repository.vehicle import VehicleRepository
from vindex.schemas.vehicle import VehicleCreate, VehicleResponse, VehicleUpdate

router = APIRouter(prefix="/vehicle", tags=["vehicles"])


@router.get("", response_model=list[VehicleResponse])
def list_vehicles(repo: Annotated[VehicleRepository, Depends(get_repository)]) -> list[VehicleResponse]:
    vehicles = repo.get_all()
    return [VehicleResponse.model_validate(v) for v in vehicles]


@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(data: VehicleCreate, repo: Annotated[VehicleRepository, Depends(get_repository)]) -> VehicleResponse:
    vehicle = repo.create(data)
    return VehicleResponse.model_validate(vehicle)


@router.get("/{vin}", response_model=VehicleResponse)
def get_vehicle(vin: str, repo: Annotated[VehicleRepository, Depends(get_repository)]) -> VehicleResponse:
    vehicle = repo.get_by_vin(vin)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find vehicle with VIN '{vin}'",
        )
    return VehicleResponse.model_validate(vehicle)


@router.put("/{vin}", response_model=VehicleResponse)
def update_vehicle(vin: str, data: VehicleUpdate, repo: Annotated[VehicleRepository, Depends(get_repository)]) -> VehicleResponse:
    try:
        vehicle = repo.update(vin, data)
        return VehicleResponse.model_validate(vehicle)
    except VehicleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find vehicle with VIN '{vin}'",
        )


@router.delete("/{vin}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vin: str, repo: Annotated[VehicleRepository, Depends(get_repository)]) -> Response:
    try:
        repo.delete(vin)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except VehicleNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cannot find vehicle with VIN '{vin}'",
        )