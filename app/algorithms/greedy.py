from app.models import Delivery, Vehicle


def greedy_assign(
    deliveries: list[Delivery],
    vehicles: list[Vehicle],
) -> dict[str, list[Delivery]]:
    """
    Assign deliveries to vehicles using a greedy strategy.

    The highest-priority deliveries are considered first.
    Each delivery is assigned to the vehicle that:
    - can accommodate it
    - leaves the least unused capacity after assignment
    """

    assignments: dict[str, list[Delivery]] = {
        vehicle.vehicle_id: []
        for vehicle in vehicles
    }

    # Highest priority deliveries are considered first.
    ordered_deliveries = sorted(
        deliveries,
        key=lambda delivery: (
            -delivery.priority,
            delivery.deadline,
        ),
    )

    for delivery in ordered_deliveries:

        suitable_vehicles = [
            vehicle
            for vehicle in vehicles
            if vehicle.can_accept(delivery)
        ]

        if not suitable_vehicles:
            continue

        # Best-fit greedy choice:
        # choose the vehicle that leaves
        # the smallest remaining capacity.
        selected_vehicle = min(
            suitable_vehicles,
            key=lambda vehicle: (
                vehicle.remaining_capacity
                - delivery.weight
            ),
        )

        selected_vehicle.assign_delivery(delivery)

        assignments[
            selected_vehicle.vehicle_id
        ].append(delivery)

    return assignments