from dataclasses import dataclass


@dataclass
class Delivery:
    delivery_id: str
    destination: str
    weight: float
    priority: int
    deadline: int

    def is_high_priority(self) -> bool:
        return self.priority >= 8

    def __str__(self) -> str:
        return (
            f"{self.delivery_id} -> {self.destination} "
            f"(Weight: {self.weight} kg, "
            f"Priority: {self.priority}, "
            f"Deadline: {self.deadline} min)"
        )