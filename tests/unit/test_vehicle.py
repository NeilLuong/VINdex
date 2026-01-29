from decimal import Decimal

import pytest
from pydantic import ValidationError

from vindex.schemas.vehicle import VehicleCreate, VehicleResponse, dollars_to_cents


class TestDollarsToCents:
    def test_converts_correctly(self):
        # Arrange
        dollars = 19999.99

        # Act
        cents = dollars_to_cents(dollars)

        # Assert
        assert cents == 1999999


class TestVinNormalization:
    def test_normalized_to_uppercase(self, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["vin"] = "abc123def456ghi78"

        # Act
        vehicle = VehicleCreate(**valid_vehicle_data)

        # Assert
        assert vehicle.vin == "ABC123DEF456GHI78"


class TestHorsePowerValidation:
    def test_rejects_zero(self, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["horse_power"] = 0

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            VehicleCreate(**valid_vehicle_data)
        assert any(e["loc"] == ("horse_power",) for e in exc_info.value.errors())

    def test_accepts_one(self, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["horse_power"] = 1

        # Act
        vehicle = VehicleCreate(**valid_vehicle_data)

        # Assert
        assert vehicle.horse_power == 1


class TestModelYearValidation:
    def test_allows_zero(self, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["model_year"] = 0

        # Act
        vehicle = VehicleCreate(**valid_vehicle_data)

        # Assert
        assert vehicle.model_year == 0


class TestResponseSerialization:
    def test_serializes_cents_to_dollars(self):
        # Arrange
        response = VehicleResponse(
            vin="1HGBH41JXMN109186",
            manufacturer_name="Toyota",
            description="Test",
            horse_power=203,
            model_name="Camry",
            model_year=2020,
            purchase_price=1999999,
            fuel_type="gasoline",
        )

        # Act
        data = response.model_dump()

        # Assert
        assert data["purchase_price"] == Decimal("19999.99")
