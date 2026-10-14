from dataclasses import dataclass, field

from app.algorithms import (
    WeightedGraph,
    dijkstra,
    greedy_assign,
    optimize_capacity,
    find_feasible_route,
    branch_and_bound,
    merge_sort_deliveries,
)

from app.core import (
    AlgorithmSelector,
    ProblemValidator,
)

from app.models import Delivery, DeliveryProblem


@dataclass
class OptimizationResult:
    """Stores the complete optimization result."""

    selected_algorithms: list[str] = field(
        default_factory=list
    )

    prioritized_deliveries: list[Delivery] = field(
        default_factory=list
    )

    assignments: dict[str, list[Delivery]] = field(
        default_factory=dict
    )

    shortest_paths: dict[str, object] = field(
        default_factory=dict
    )

    capacity_selection: list[Delivery] = field(
        default_factory=list
    )

    backtracking_route: list[Delivery] = field(
        default_factory=list
    )

    branch_bound_route: list[Delivery] = field(
        default_factory=list
    )

    messages: list[str] = field(
        default_factory=list
    )


class DeliveryOptimizer:
    """Coordinates validation, selection and optimization."""

    def __init__(self) -> None:
        self.selector = AlgorithmSelector()
        self.validator = ProblemValidator()

    def optimize(
        self,
        problem: DeliveryProblem,
    ) -> OptimizationResult:

        # 1. Validate input
        self.validator.validate(problem)

        # 2. Analyze the problem
        decisions = self.selector.analyze(problem)

        if not decisions:
            raise ValueError(
                "No suitable algorithms found."
            )

        # 3. Create result object
        result = OptimizationResult()

        # 4. Store selected algorithms
        result.selected_algorithms = [
            decision.name
            for decision in decisions
        ]

        # =================================================
        # DIVIDE AND CONQUER
        # =================================================

        if problem.deliveries:

            result.prioritized_deliveries = (
                merge_sort_deliveries(
                    problem.deliveries
                )
            )

            result.messages.append(
                "Deliveries prioritized using "
                "Divide and Conquer Merge Sort."
            )

        # =================================================
        # GRAPH
        # =================================================

        graph = WeightedGraph()
        graph.add_roads(problem.roads)

        # =================================================
        # GREEDY
        # =================================================

        if any(
            decision.name == "Greedy"
            for decision in decisions
        ):

            assignments = greedy_assign(
                result.prioritized_deliveries,
                problem.vehicles,
            )

            result.assignments = assignments

            result.messages.append(
                "Greedy vehicle assignment completed."
            )

        # =================================================
        # DIJKSTRA
        # =================================================

        if any(
            decision.name == "Dijkstra"
            for decision in decisions
        ):

            for delivery in problem.deliveries:

                try:

                    shortest_path = dijkstra(
                        graph,
                        "DEPOT",
                        delivery.destination,
                    )

                    result.shortest_paths[
                        delivery.delivery_id
                    ] = shortest_path

                except ValueError:

                    result.messages.append(
                        f"No path found for "
                        f"{delivery.delivery_id}."
                    )

            result.messages.append(
                "Shortest paths calculated using Dijkstra."
            )

        # =================================================
        # DYNAMIC PROGRAMMING
        # =================================================

        if any(
            decision.name == "Dynamic Programming"
            for decision in decisions
        ):

            if problem.vehicles:

                largest_vehicle = max(
                    problem.vehicles,
                    key=lambda vehicle: vehicle.capacity,
                )

                selected = optimize_capacity(
                    problem.deliveries,
                    largest_vehicle.capacity,
                )

                result.capacity_selection = selected

                result.messages.append(
                    "Capacity optimization completed "
                    "using Dynamic Programming."
                )

        # =================================================
        # BACKTRACKING
        # =================================================

        if any(
            decision.name == "Backtracking"
            for decision in decisions
        ):

            deliveries = problem.deliveries[:6]

            try:

                route = find_feasible_route(
                    graph,
                    "DEPOT",
                    deliveries,
                )

                result.backtracking_route = (
                    route.route
                )

                result.messages.append(
                    "Feasible route found using Backtracking."
                )

            except ValueError:

                result.messages.append(
                    "Backtracking could not find "
                    "a feasible route."
                )

        # =================================================
        # BRANCH AND BOUND
        # =================================================

        if any(
            decision.name == "Branch and Bound"
            for decision in decisions
        ):

            deliveries = problem.deliveries[:6]

            try:

                route = branch_and_bound(
                    graph,
                    "DEPOT",
                    deliveries,
                )

                result.branch_bound_route = (
                    route.route
                )

                result.messages.append(
                    "Optimized route found using "
                    "Branch and Bound."
                )

            except ValueError:

                result.messages.append(
                    "Branch and Bound could not find "
                    "a feasible route."
                )

        return result