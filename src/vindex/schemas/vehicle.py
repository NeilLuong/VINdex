from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Vin = Annotated[str, Field(min_length=17, max_length=17, pattern=r"^[A-HJ-NPR-Z0-9]{17}$")]

FuelType = Literal["gasoline", "diesel", "electric", "hybrid"]

class VehicleCreate(BaseModel):
    vin: Vin
    manufacturer_name: Annotated[str, Field(min_length=1, max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(min_length=1, max_length=100)]
    model_year: Annotated[int, Field(ge=1886, le=2100)]
    purchase_price: Annotated[Decimal, Field(ge=0, decimal_places=2)]
    fuel_type: FuelType

    @field_validator("vin", mode="before")
    @classmethod
    def normalize_vin(cls, v: str) -> str:
        if (isinstance(v, str)):
            return v.upper()
        return v
    
class VehicleUpdate(BaseModel):    
    manufacturer_name: Annotated[str, Field(min_length=1, max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(min_length=1, max_length=100)]
    model_year: Annotated[int, Field(ge=0)]
    purchase_price: Annotated[Decimal, Field(ge=0, decimal_places=2)]
    fuel_type: FuelType


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vin: Vin
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: Decimal
    fuel_type: FuelType