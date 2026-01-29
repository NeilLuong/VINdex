from sqlalchemy import select
from sqlalchemy.orm import Session

from vindex.core.exceptions import VehicleAlreadyExistsError, VehicleNotFoundError
from vindex.models.vehicle import Vehicle
from vindex.schemas.vehicle import VehicleCreate, VehicleUpdate


class VehicleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all(self) -> list[Vehicle]:
        stmt = select(Vehicle)
        return list(self.session.scalars(stmt).all())

    def get_by_vin(self, vin: str) -> Vehicle | None:
        stmt = select(Vehicle).where(Vehicle.vin == vin.upper())
        return self.session.scalars(stmt).first()

    def create(self, data: VehicleCreate) -> Vehicle:
        if self.get_by_vin(data.vin) is not None:
            raise VehicleAlreadyExistsError(data.vin)
        vehicle = Vehicle(
            vin=data.vin,
            manufacturer_name=data.manufacturer_name,
            description=data.description,
            horse_power=data.horse_power,
            model_name=data.model_name,
            model_year=data.model_year,
            purchase_price=data.purchase_price,
            fuel_type=data.fuel_type,
        )
        self.session.add(vehicle)
        self.session.commit()
        self.session.refresh(vehicle)
        return vehicle

    def update(self, vin: str, data: VehicleUpdate) -> Vehicle:
        vehicle = self.get_by_vin(vin)
        if vehicle is None:
            raise VehicleNotFoundError(vin)

        vehicle.manufacturer_name = data.manufacturer_name
        vehicle.description = data.description
        vehicle.horse_power = data.horse_power
        vehicle.model_name = data.model_name
        vehicle.model_year = data.model_year
        vehicle.purchase_price = data.purchase_price
        vehicle.fuel_type = data.fuel_type

        self.session.commit()
        self.session.refresh(vehicle)
        return vehicle

    def delete(self, vin: str) -> None:
        vehicle = self.get_by_vin(vin)
        if vehicle is None:
            raise VehicleNotFoundError(vin)

        self.session.delete(vehicle)
        self.session.commit()
