from decimal import Decimal
from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator


def dollars_to_cents(v: Any) -> int:
    return int(Decimal(str(v)) * 100)


class VehicleCreate(BaseModel):
    vin: Annotated[str, Field(min_length=17, max_length=17)]
    manufacturer_name: Annotated[str, Field(max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(max_length=100)]
    model_year: Annotated[int, Field(ge=0)]
    purchase_price: int
    fuel_type: Annotated[str, Field(max_length=20)]

    @field_validator("vin", mode="before")
    @classmethod
    def normalize_vin(cls, v: str) -> str:
        if isinstance(v, str):
            return v.upper()
        return v

    @field_validator("purchase_price", mode="before")
    @classmethod
    def convert_price(cls, v: Any) -> int:
        return dollars_to_cents(v)


class VehicleUpdate(BaseModel):
    manufacturer_name: Annotated[str, Field(max_length=100)]
    description: str
    horse_power: Annotated[int, Field(gt=0)]
    model_name: Annotated[str, Field(max_length=100)]
    model_year: Annotated[int, Field(ge=0)]
    purchase_price: int
    fuel_type: Annotated[str, Field(max_length=20)]

    @field_validator("purchase_price", mode="before")
    @classmethod
    def convert_price(cls, v: Any) -> int:
        return dollars_to_cents(v)


class VehicleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    vin: str
    manufacturer_name: str
    description: str
    horse_power: int
    model_name: str
    model_year: int
    purchase_price: int
    fuel_type: str

    @field_serializer("purchase_price")
    def cents_to_dollars(self, v: int) -> Decimal:
        return Decimal(v) / 100
