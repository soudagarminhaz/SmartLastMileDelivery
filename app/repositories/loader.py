import csv
from pathlib import Path

from app.models import Delivery, Vehicle, Road, DeliveryProblem


class DataLoader:
    """Loads delivery optimization data from CSV files."""

    def __init__(self, data_directory: str | Path):
        self.data_directory = Path(data_directory)

    def load_deliveries(self) -> list[Delivery]:
        file_path = self.data_directory / "deliveries.csv"

        deliveries: list[Delivery] = []

        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                delivery = Delivery(
                    delivery_id=row["delivery_id"],
                    destination=row["destination"],
                    weight=float(row["weight"]),
                    priority=int(row["priority"]),
                    deadline=int(row["deadline"]),
                )

                deliveries.append(delivery)

        return deliveries

    def load_vehicles(self) -> list[Vehicle]:
        file_path = self.data_directory / "vehicles.csv"

        vehicles: list[Vehicle] = []

        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                vehicle = Vehicle(
                    vehicle_id=row["vehicle_id"],
                    capacity=float(row["capacity"]),
                    start_location=row["start_location"],
                    vehicle_type=row["vehicle_type"],
                )

                vehicles.append(vehicle)

        return vehicles

    def load_roads(self) -> list[Road]:
        file_path = self.data_directory / "roads.csv"

        roads: list[Road] = []

        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                road = Road(
                    source=row["source"],
                    destination=row["destination"],
                    distance=float(row["distance"]),
                )

                roads.append(road)

        return roads

    def load_problem(self) -> DeliveryProblem:
        return DeliveryProblem(
            deliveries=self.load_deliveries(),
            vehicles=self.load_vehicles(),
            roads=self.load_roads(),
        )