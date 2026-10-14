from app.algorithms.dijkstra import dijkstra
from app.algorithms.graph import WeightedGraph
from app.models import Delivery


class BranchBoundResult:
    """Stores the best route found using Branch and Bound."""

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


def branch_and_bound(
    graph: WeightedGraph,
    start: str,
    deliveries: list[Delivery],
) -> BranchBoundResult:

    if not deliveries:
        return BranchBoundResult([], 0.0)

    best_route: list[Delivery] = []
    best_distance = float("inf")

    def calculate_lower_bound(
        current_location: str,
        remaining: list[Delivery],
        current_distance: float,
    ) -> float:

        if not remaining:
            return current_distance

        lower_bound = current_distance

        location = current_location

        # Add the cheapest known path to each
        # remaining delivery.
        for delivery in remaining:

            try:
                result = dijkstra(
                    graph,
                    location,
                    delivery.destination,
                )

            except ValueError:
                return float("inf")

            lower_bound += result.distance
            location = delivery.destination

        return lower_bound

    def branch(
        current_location: str,
        remaining: list[Delivery],
        current_route: list[Delivery],
        current_distance: float,
    ) -> None:

        nonlocal best_route
        nonlocal best_distance

        # A complete solution has been found.
        if not remaining:

            if current_distance < best_distance:

                best_distance = current_distance
                best_route = current_route.copy()

            return

        # Calculate a lower bound for this branch.
        lower_bound = calculate_lower_bound(
            current_location,
            remaining,
            current_distance,
        )

        # Prune this branch if it cannot improve
        # the current best solution.
        if lower_bound >= best_distance:
            return

        for delivery in remaining:

            try:
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

            # Deadline constraint.
            if new_distance > delivery.deadline:
                continue

            current_route.append(delivery)

            new_remaining = [
                item
                for item in remaining
                if item.delivery_id
                != delivery.delivery_id
            ]

            branch(
                delivery.destination,
                new_remaining,
                current_route,
                new_distance,
            )

            current_route.pop()

    branch(
        start,
        deliveries,
        [],
        0.0,
    )

    if not best_route:
        raise ValueError(
            "No feasible delivery sequence found."
        )

    return BranchBoundResult(
        route=best_route,
        distance=best_distance,
    )
