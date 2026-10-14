from dataclasses import dataclass, field

from app.models.delivery import Delivery
from app.models.vehicles import Vehicle
from app.models.road import Road


@dataclass
class DeliveryProblem:
    deliveries: list[Delivery] = field(default_factory=list)
    vehicles: list[Vehicle] = field(default_factory=list)
    roads: list[Road] = field(default_factory=list)

    @property
    def delivery_count(self) -> int:
        return len(self.deliveries)

    @property
    def vehicle_count(self) -> int:
        return len(self.vehicles)

    @property
    def has_capacity_constraint(self) -> bool:
        return any(
            vehicle.capacity > 0
            for vehicle in self.vehicles
        )

    @property
    def has_deadlines(self) -> bool:
        return any(
            delivery.deadline > 0
            for delivery in self.deliveries
        )

    @property
    def has_priorities(self) -> bool:
        return any(
            delivery.priority > 0
            for delivery in self.deliveries
        )

    @property
    def has_weighted_graph(self) -> bool:
        return any(
            road.distance > 0
            for road in self.roads
        )