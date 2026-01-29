import pytest
from pydantic import ValidationError

from vindex.schemas.vehicle import VehicleCreate


class TestVehicleCreate:
    def test_valid_data_creates_vehicle(self, valid_vehicle_data: dict) -> None:
        vehicle = VehicleCreate(**valid_vehicle_data)

        assert vehicle.vin == "1HGBH41JXMN109186"
        assert vehicle.manufacturer_name == "Toyota"
        assert vehicle.fuel_type == "gasoline"

    def test_vin_normalization(self, valid_vehicle_data: dict) -> None:
        valid_vehicle_data["vin"] = "1hgbh41jxmn109186"
        vehicle = VehicleCreate(**valid_vehicle_data)

        assert vehicle.vin == "1HGBH41JXMN109186"

    def test_invalid_vin_too_short(self, valid_vehicle_data: dict) -> None:
        valid_vehicle_data["vin"] = "1HGBH41JXMN10918"
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(**valid_vehicle_data)

        errors = exc_info.value.errors()
        assert errors[0]["loc"] == ("vin",)
        assert errors[0]["msg"] == "ensure this value has at least 17 characters"
