from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from vindex.core.database import SessionLocal
from vindex.repository.vehicle import VehicleRepository


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(db: Annotated[Session, Depends(get_db)]) -> VehicleRepository:
    return VehicleRepository(db)