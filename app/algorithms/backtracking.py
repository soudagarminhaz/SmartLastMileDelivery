from app.algorithms.graph import WeightedGraph
from app.models import Delivery


class BacktrackingResult:
    """Stores the best feasible delivery sequence."""

    def __init__(
        self,
        route: list[Delivery],
        distance: float,
    ) -> None:
        self.route = route
        self.distance = distance

    def __str__(self) -> str:
        destinations = " -> ".join(
            delivery.destination
            for delivery in self.route
        )

        return (
            f"Route: {destinations}\n"
            f"Distance: {self.distance:.2f} km"
        )


def find_feasible_route(
    graph: WeightedGraph,
    start: str,
    deliveries: list[Delivery],
) -> BacktrackingResult:

    if not deliveries:
        return BacktrackingResult([], 0.0)

    best_route: list[Delivery] = []
    best_distance = float("inf")

    def backtrack(
        current_location: str,
        remaining: list[Delivery],
        current_route: list[Delivery],
        current_distance: float,
    ) -> None:

        nonlocal best_route
        nonlocal best_distance

        # -----------------------------------------
        # Base case
        # -----------------------------------------

        if not remaining:

            if current_distance < best_distance:

                best_distance = current_distance
                best_route = current_route.copy()

            return

        # -----------------------------------------
        # Pruning
        # -----------------------------------------

        if current_distance >= best_distance:
            return

        # -----------------------------------------
        # Explore possible next deliveries
        # -----------------------------------------

        for delivery in remaining:

            try:

                from app.algorithms.dijkstra import dijkstra

                result = dijkstra(
                    graph,
                    current_location,
                    delivery.destination,
                )

            except ValueError:
                continue

            new_distance = (
                current_distance
                + result.distance
            )

            # -------------------------------------
            # Deadline check
            # -------------------------------------

            if new_distance > delivery.deadline:
                continue

            current_route.append(delivery)

            new_remaining = [
                item
                for item in remaining
                if item.delivery_id
                != delivery.delivery_id
            ]

            backtrack(
                delivery.destination,
                new_remaining,
                current_route,
                new_distance,
            )

            current_route.pop()

    backtrack(
        start,
        deliveries,
        [],
        0.0,
    )

    if not best_route:
        raise ValueError(
            "No feasible delivery sequence found."
        )

    return BacktrackingResult(
        route=best_route,
        distance=best_distance,
    )