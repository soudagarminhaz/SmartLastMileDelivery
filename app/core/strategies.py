from abc import ABC, abstractmethod
from typing import Any

from app.models import DeliveryProblem
from app.algorithms import (
    WeightedGraph,
    dijkstra,
    greedy_assign,
    optimize_capacity,
)


class OptimizationStrategy(ABC):
    """Abstract strategy for optimization algorithms."""

    @abstractmethod
    def execute(
        self,
        problem: DeliveryProblem,
    ) -> Any:
        """Execute the optimization strategy."""
        raise NotImplementedError


class ShortestPathStrategy(
    OptimizationStrategy
):
    """Strategy using Dijkstra's algorithm."""

    def execute(
        self,
        problem: DeliveryProblem,
    ) -> dict[str, object]:

        graph = WeightedGraph()
        graph.add_roads(problem.roads)

        results: dict[str, object] = {}

        for delivery in problem.deliveries:

            try:

                result = dijkstra(
                    graph,
                    "DEPOT",
                    delivery.destination,
                )

                results[
                    delivery.delivery_id
                ] = result

            except ValueError:
                continue

        return results


class GreedyStrategy(
    OptimizationStrategy
):
    """Strategy using greedy vehicle assignment."""

    def execute(
        self,
        problem: DeliveryProblem,
    ) -> dict:

        return greedy_assign(
            problem.deliveries,
            problem.vehicles,
        )


class CapacityStrategy(
    OptimizationStrategy
):
    """Strategy using Dynamic Programming."""

    def execute(
        self,
        problem: DeliveryProblem,
    ) -> list:

        if not problem.vehicles:
            return []

        largest_vehicle = max(
            problem.vehicles,
            key=lambda vehicle: vehicle.capacity,
        )

        return optimize_capacity(
            problem.deliveries,
            largest_vehicle.capacity,
        )
class BacktrackingStrategy(
    OptimizationStrategy
):
    """Strategy using Backtracking."""

    def execute(
        self,
        problem: DeliveryProblem,
    ) -> object:

        from app.algorithms import (
            find_feasible_route,
        )

        graph = WeightedGraph()
        graph.add_roads(problem.roads)

        # Backtracking is exponential, so use a
        # small delivery subset.
        deliveries = problem.deliveries[:6]

        return find_feasible_route(
            graph,
            "DEPOT",
            deliveries,
        )


class BranchAndBoundStrategy(
    OptimizationStrategy
):
    """Strategy using Branch and Bound."""

    def execute(
        self,
        problem: DeliveryProblem,
    ) -> object:

        from app.algorithms import (
            branch_and_bound,
        )

        graph = WeightedGraph()
        graph.add_roads(problem.roads)

        # Branch and Bound is also exponential in
        # the worst case.
        deliveries = problem.deliveries[:6]

        return branch_and_bound(
            graph,
            "DEPOT",
            deliveries,
        )