from dataclasses import dataclass

from app.models import DeliveryProblem


@dataclass
class AlgorithmDecision:
    """Represents one algorithm selected for the problem."""

    name: str
    reason: str
    score: int


class AlgorithmSelector:
    """
    Automatically selects suitable algorithms based on
    the characteristics of the delivery problem.
    """

    def analyze(
        self,
        problem: DeliveryProblem
    ) -> list[AlgorithmDecision]:

        decisions: list[AlgorithmDecision] = []

        delivery_count = problem.delivery_count
        vehicle_count = problem.vehicle_count

        # -------------------------------------------------
        # 1. SHORTEST PATH
        # -------------------------------------------------

        if problem.has_weighted_graph:

            score = 70

            if len(problem.roads) >= delivery_count:
                score += 10

            decisions.append(
                AlgorithmDecision(
                    name="Dijkstra",
                    reason=(
                        "The road network contains weighted edges, "
                        "so shortest paths between delivery locations "
                        "can be calculated efficiently."
                    ),
                    score=min(score, 100),
                )
            )

        # -------------------------------------------------
        # 2. GREEDY
        # -------------------------------------------------

        if vehicle_count > 0:

            score = 60

            if problem.has_priorities:
                score += 15

            if problem.has_capacity_constraint:
                score += 15

            decisions.append(
                AlgorithmDecision(
                    name="Greedy",
                    reason=(
                        "Multiple vehicles and capacity constraints "
                        "make fast priority-based assignment useful."
                    ),
                    score=min(score, 100),
                )
            )

        # -------------------------------------------------
        # 3. DYNAMIC PROGRAMMING
        # -------------------------------------------------

        if problem.has_capacity_constraint:

            score = 65

            if problem.has_priorities:
                score += 15

            # DP is particularly practical for smaller
            # capacity values.
            max_capacity = max(
                (
                    vehicle.capacity
                    for vehicle in problem.vehicles
                ),
                default=0,
            )

            if max_capacity <= 20:
                score += 15

            decisions.append(
                AlgorithmDecision(
                    name="Dynamic Programming",
                    reason=(
                        "Vehicles have limited capacity and "
                        "deliveries have different priorities, "
                        "making 0/1 Knapsack suitable for selecting "
                        "valuable deliveries."
                    ),
                    score=min(score, 100),
                )
            )

        # -------------------------------------------------
        # 4. BACKTRACKING
        # -------------------------------------------------

        if (
            problem.has_deadlines
            and delivery_count <= 8
        ):

            score = 70

            if problem.has_priorities:
                score += 10

            decisions.append(
                AlgorithmDecision(
                    name="Backtracking",
                    reason=(
                        "The problem contains deadline constraints "
                        "and the delivery set is small enough to "
                        "explore feasible sequences."
                    ),
                    score=min(score, 100),
                )
            )

        # -------------------------------------------------
        # 5. BRANCH AND BOUND
        # -------------------------------------------------

        if delivery_count <= 10:

            score = 65

            if problem.has_deadlines:
                score += 10

            if problem.has_weighted_graph:
                score += 10

            decisions.append(
                AlgorithmDecision(
                    name="Branch and Bound",
                    reason=(
                        "The delivery set is small enough for "
                        "exact search with pruning, while the "
                        "lower-bound calculation can eliminate "
                        "unpromising routes."
                    ),
                    score=min(score, 100),
                )
            )

        # Highest-scoring algorithms first.
        return sorted(
            decisions,
            key=lambda decision: decision.score,
            reverse=True,
        )

    def select_primary(
        self,
        problem: DeliveryProblem
    ) -> AlgorithmDecision:

        decisions = self.analyze(problem)

        if not decisions:
            raise ValueError(
                "No suitable algorithm was identified."
            )

        return decisions[0]