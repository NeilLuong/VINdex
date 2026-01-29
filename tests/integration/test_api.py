class TestPostVehicle:
    def test_creates_and_returns_201(self, client, valid_vehicle_data):
        # Act
        response = client.post("/vehicle", json=valid_vehicle_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["vin"] == valid_vehicle_data["vin"]
        assert data["purchase_price"] == "19999.99"


class TestGetAllVehicles:
    def test_returns_list(self, client, valid_vehicle_data):
        # Arrange
        client.post("/vehicle", json=valid_vehicle_data)

        # Act
        response = client.get("/vehicle")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1


class TestGetVehicleByVin:
    def test_returns_correct_vehicle(self, client, valid_vehicle_data):
        # Arrange
        client.post("/vehicle", json=valid_vehicle_data)

        # Act
        response = client.get(f"/vehicle/{valid_vehicle_data['vin']}")

        # Assert
        assert response.status_code == 200
        assert response.json()["vin"] == valid_vehicle_data["vin"]


class TestPutVehicle:
    def test_updates_fields(self, client, valid_vehicle_data):
        # Arrange
        client.post("/vehicle", json=valid_vehicle_data)
        update_data = {
            "manufacturer_name": "Updated Toyota",
            "description": "Updated description",
            "horse_power": 250,
            "model_name": "Camry Sport",
            "model_year": 2022,
            "purchase_price": 29999.99,
            "fuel_type": "hybrid",
        }

        # Act
        response = client.put(f"/vehicle/{valid_vehicle_data['vin']}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["manufacturer_name"] == "Updated Toyota"
        assert data["horse_power"] == 250


class TestDeleteVehicle:
    def test_returns_204(self, client, valid_vehicle_data):
        # Arrange
        client.post("/vehicle", json=valid_vehicle_data)

        # Act
        response = client.delete(f"/vehicle/{valid_vehicle_data['vin']}")

        # Assert
        assert response.status_code == 204


class TestErrorResponses:
    def test_invalid_json_returns_400(self, client):
        # Act
        response = client.post(
            "/vehicle",
            content="{invalid json}",
            headers={"Content-Type": "application/json"},
        )

        # Assert
        assert response.status_code == 400

    def test_invalid_vin_length_returns_422(self, client, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["vin"] = "SHORT"

        # Act
        response = client.post("/vehicle", json=valid_vehicle_data)

        # Assert
        assert response.status_code == 422

    def test_duplicate_vin_returns_409(self, client, valid_vehicle_data):
        # Arrange
        client.post("/vehicle", json=valid_vehicle_data)

        # Act
        response = client.post("/vehicle", json=valid_vehicle_data)

        # Assert
        assert response.status_code == 409


class TestVinCaseInsensitivity:
    def test_lookup_is_case_insensitive(self, client, valid_vehicle_data):
        # Arrange
        valid_vehicle_data["vin"] = "abc123def456ghi78"
        client.post("/vehicle", json=valid_vehicle_data)

        # Act
        response = client.get("/vehicle/ABC123DEF456GHI78")

        # Assert
        assert response.status_code == 200
        assert response.json()["vin"] == "ABC123DEF456GHI78"
