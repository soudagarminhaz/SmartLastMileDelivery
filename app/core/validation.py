from app.models import DeliveryProblem


class ValidationError(ValueError):
    """Raised when the delivery problem is invalid."""


class ProblemValidator:
    """Validates delivery optimization input."""

    def validate(
        self,
        problem: DeliveryProblem,
    ) -> None:

        self._validate_deliveries(problem)
        self._validate_vehicles(problem)
        self._validate_roads(problem)

    def _validate_deliveries(
        self,
        problem: DeliveryProblem,
    ) -> None:

        delivery_ids: set[str] = set()

        for delivery in problem.deliveries:

            if not delivery.delivery_id:
                raise ValidationError(
                    "Delivery ID cannot be empty."
                )

            if delivery.delivery_id in delivery_ids:
                raise ValidationError(
                    f"Duplicate delivery ID: "
                    f"{delivery.delivery_id}"
                )

            delivery_ids.add(
                delivery.delivery_id
            )

            if not delivery.destination:
                raise ValidationError(
                    f"Destination missing for "
                    f"{delivery.delivery_id}."
                )

            if delivery.weight <= 0:
                raise ValidationError(
                    f"Weight must be greater than zero "
                    f"for {delivery.delivery_id}."
                )

            if delivery.priority < 1:
                raise ValidationError(
                    f"Priority must be at least 1 "
                    f"for {delivery.delivery_id}."
                )

            if delivery.deadline <= 0:
                raise ValidationError(
                    f"Deadline must be greater than zero "
                    f"for {delivery.delivery_id}."
                )

    def _validate_vehicles(
        self,
        problem: DeliveryProblem,
    ) -> None:

        vehicle_ids: set[str] = set()

        for vehicle in problem.vehicles:

            if not vehicle.vehicle_id:
                raise ValidationError(
                    "Vehicle ID cannot be empty."
                )

            if vehicle.vehicle_id in vehicle_ids:
                raise ValidationError(
                    f"Duplicate vehicle ID: "
                    f"{vehicle.vehicle_id}"
                )

            vehicle_ids.add(
                vehicle.vehicle_id
            )

            if vehicle.capacity <= 0:
                raise ValidationError(
                    f"Vehicle capacity must be "
                    f"greater than zero for "
                    f"{vehicle.vehicle_id}."
                )

            if not vehicle.start_location:
                raise ValidationError(
                    f"Start location missing for "
                    f"{vehicle.vehicle_id}."
                )

    def _validate_roads(
        self,
        problem: DeliveryProblem,
    ) -> None:

        for road in problem.roads:

            if not road.source:
                raise ValidationError(
                    "Road source cannot be empty."
                )

            if not road.destination:
                raise ValidationError(
                    "Road destination cannot be empty."
                )

            if road.distance <= 0:
                raise ValidationError(
                    f"Road distance must be greater "
                    f"than zero: "
                    f"{road.source} -> "
                    f"{road.destination}"
                )