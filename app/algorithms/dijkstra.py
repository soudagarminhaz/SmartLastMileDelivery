import heapq

from app.algorithms.graph import WeightedGraph


class DijkstraResult:
    """Stores the result of a shortest-path calculation."""

    def __init__(
        self,
        distance: float,
        path: list[str]
    ) -> None:
        self.distance = distance
        self.path = path

    def __str__(self) -> str:
        route = " -> ".join(self.path)

        return (
            f"Route: {route}\n"
            f"Distance: {self.distance:.2f} km"
        )


def dijkstra(
    graph: WeightedGraph,
    start: str,
    target: str
) -> DijkstraResult:

    if start not in graph:
        raise ValueError(
            f"Unknown starting location: {start}"
        )

    if target not in graph:
        raise ValueError(
            f"Unknown target location: {target}"
        )

    distances: dict[str, float] = {
        location: float("inf")
        for location in graph.locations()
    }

    previous: dict[str, str | None] = {
        location: None
        for location in graph.locations()
    }

    distances[start] = 0

    priority_queue: list[tuple[float, str]] = [
        (0, start)
    ]

    while priority_queue:

        current_distance, current = heapq.heappop(
            priority_queue
        )

        if current_distance > distances[current]:
            continue

        if current == target:
            break

        for neighbor, weight in graph.neighbors(current):

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    if distances[target] == float("inf"):
        raise ValueError(
            f"No route exists from {start} to {target}"
        )

    path = _reconstruct_path(
        previous,
        start,
        target
    )

    return DijkstraResult(
        distance=distances[target],
        path=path
    )


def _reconstruct_path(
    previous: dict[str, str | None],
    start: str,
    target: str
) -> list[str]:

    path: list[str] = []
    current: str | None = target

    while current is not None:
        path.append(current)

        if current == start:
            break

        current = previous[current]

    path.reverse()

    return path