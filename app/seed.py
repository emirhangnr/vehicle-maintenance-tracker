"""Load fictional sample data for local development and demos.

Usage: python -m app.seed

All plates, brands and models are made up. Dates are relative to today so the
reminder screens always show upcoming and overdue examples.
"""

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models  # noqa: F401  (registers tables on Base.metadata)
from app.database import Base, SessionLocal, engine
from app.models import MaintenanceRecord, Vehicle


def build_sample_vehicles(today: date) -> list[Vehicle]:
    def days(n: int) -> date:
        return today + timedelta(days=n)

    return [
        Vehicle(
            plate="34 ABC 123", brand="Örnek Marka", model="Model A", year=2019, current_km=84500,
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_type="Yağ değişimi", service_date=days(-200), odometer_km=72000,
                    cost=Decimal("1850.00"), notes="Motor yağı ve yağ filtresi değişti.",
                    next_due_date=days(-15), next_due_km=82000,
                ),
                MaintenanceRecord(
                    maintenance_type="Fren", service_date=days(-90), odometer_km=80000,
                    cost=Decimal("3200.00"), next_due_date=days(275), next_due_km=110000,
                ),
            ],
        ),
        Vehicle(
            plate="06 XYZ 456", brand="Deneme Otomotiv", model="Kompakt", year=2021, current_km=41200,
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_type="Periyodik bakım", service_date=days(-340), odometer_km=30000,
                    cost=Decimal("4750.00"), next_due_date=days(20), next_due_km=45000,
                ),
            ],
        ),
        Vehicle(
            plate="35 DEF 789", brand="Kurgu Motor", model="Hafif Ticari", year=2017, current_km=152300,
            maintenance_records=[
                MaintenanceRecord(
                    maintenance_type="Lastik", service_date=days(-400), odometer_km=120000,
                    cost=Decimal("9600.00"), notes="Dört lastik yenilendi.",
                    next_due_date=days(-35), next_due_km=150000,
                ),
                MaintenanceRecord(
                    maintenance_type="Yağ değişimi", service_date=days(-60), odometer_km=145000,
                    cost=Decimal("2100.00"), next_due_date=days(120), next_due_km=155000,
                ),
            ],
        ),
        Vehicle(plate="16 KLM 321", brand="Örnek Marka", model="Model B", year=2024, current_km=8900),
    ]


def seed(db: Session, today: date | None = None) -> int:
    """Insert sample vehicles if the database has none. Returns the number of vehicles added."""
    if db.scalar(select(Vehicle.id).limit(1)) is not None:
        return 0
    vehicles = build_sample_vehicles(today or date.today())
    db.add_all(vehicles)
    db.commit()
    return len(vehicles)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as session:
        added = seed(session)
    print(f"Seed complete: {added} vehicles added." if added else "Database already has data; seed skipped.")
