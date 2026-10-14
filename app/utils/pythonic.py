from collections.abc import Callable, Iterator

from app.models import Delivery


def high_priority_deliveries(
    deliveries: list[Delivery],
    minimum_priority: int = 8,
) -> list[Delivery]:
    """Return deliveries meeting the priority threshold."""

    return [
        delivery
        for delivery in deliveries
        if delivery.priority >= minimum_priority
    ]


def delivery_weights(
    deliveries: list[Delivery],
) -> dict[str, float]:
    """Create a delivery-to-weight dictionary."""

    return {
        delivery.delivery_id: delivery.weight
        for delivery in deliveries
    }


def delivery_destinations(
    deliveries: list[Delivery],
) -> Iterator[str]:
    """
    Lazily generate delivery destinations.

    Generators avoid creating the complete result
    in memory at once.
    """

    for delivery in deliveries:
        yield delivery.destination


def filter_deliveries(
    deliveries: list[Delivery],
    condition: Callable[[Delivery], bool],
) -> list[Delivery]:
    """
    Higher-order function.

    Accepts another function as an argument.
    """

    return list(
        filter(condition, deliveries)
    )


def calculate_total_weight(
    deliveries: list[Delivery],
) -> float:
    """Pure function that calculates total delivery weight."""

    return sum(
        delivery.weight
        for delivery in deliveries
    )


def calculate_average_priority(
    deliveries: list[Delivery],
) -> float:
    """Pure function for average priority."""

    if not deliveries:
        return 0.0

    return sum(
        delivery.priority
        for delivery in deliveries
    ) / len(deliveries)
