from dataclasses import dataclass, field

from app.models.delivery import Delivery


@dataclass
class Vehicle:
    vehicle_id: str
    capacity: float
    start_location: str
    vehicle_type: str
    deliveries: list[Delivery] = field(default_factory=list)

    @property
    def used_capacity(self) -> float:
        return sum(delivery.weight for delivery in self.deliveries)

    @property
    def remaining_capacity(self) -> float:
        return self.capacity - self.used_capacity

    def can_accept(self, delivery: Delivery) -> bool:
        return self.remaining_capacity >= delivery.weight

    def assign_delivery(self, delivery: Delivery) -> bool:
        if not self.can_accept(delivery):
            return False

        self.deliveries.append(delivery)
        return True

    def __str__(self) -> str:
        return (
            f"{self.vehicle_id} - {self.vehicle_type} "
            f"({self.used_capacity}/{self.capacity} kg)"
        )