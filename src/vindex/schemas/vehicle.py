from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


class VehicleCreate(BaseModel):
    vin: Annotated[str, Field(min_length=17, max_length=17)]
    manufacturer_name: Annotated[str, Field(max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(max_length=100)]
    model_year: Annotated[int, Field(ge=0)]
    purchase_price: Annotated[Decimal, Field(ge=0)]
    fuel_type: Annotated[str, Field(max_length=20)]

    @field_validator("vin", mode="before")
    @classmethod
    def normalize_vin(cls, v: str) -> str:
        if isinstance(v, str):
            return v.upper()
        return v


class VehicleUpdate(BaseModel):
    manufacturer_name: Annotated[str, Field(max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(max_length=100)]
    model_year: Annotated[int, Field(ge=0)]
    purchase_price: Annotated[Decimal, Field(ge=0)]
    fuel_type: Annotated[str, Field(max_length=20)]


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vin: str
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: Decimal
    fuel_type: str