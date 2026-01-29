import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from vindex.core.database import get_db
from vindex.main import app
from vindex.models.vehicle import Base


@pytest.fixture
def valid_vehicle_data() -> dict:
    return {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Toyota",
        "description": "A reliable car",
        "horse_power": 203,
        "model_name": "Camry",
        "model_year": 2020,
        "purchase_price": 19999.99,
        "fuel_type": "gasoline",
    }


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
