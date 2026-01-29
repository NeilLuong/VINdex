from sqlalchemy import String, Text, Numeric
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Vehicle(Base):
    __tablename__ = "vehicle"
    vin: Mapped[str] = mapped_column(String(17), primary_key=True)
    manufacturer_name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    horse_power: Mapped[int]
    model_name: Mapped[str] = mapped_column(String(100))
    model_year: Mapped[int]
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    fuel_type: Mapped[str] = mapped_column(String(20))