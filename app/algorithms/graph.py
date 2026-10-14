from collections import defaultdict
from app.models import Road


class WeightedGraph:
    """Represents the delivery road network."""

    def __init__(self) -> None:
        self.adjacency: dict[str, list[tuple[str, float]]] = defaultdict(list)

    def add_road(self, road: Road) -> None:
        self.adjacency[road.source].append(
            (road.destination, road.distance)
        )

        self.adjacency[road.destination].append(
            (road.source, road.distance)
        )

    def add_roads(self, roads: list[Road]) -> None:
        for road in roads:
            self.add_road(road)

    def neighbors(self, location: str) -> list[tuple[str, float]]:
        return self.adjacency.get(location, [])

    def locations(self) -> list[str]:
        return list(self.adjacency.keys())

    def __contains__(self, location: str) -> bool:
        return location in self.adjacency

    def __str__(self) -> str:
        lines = []

        for location, neighbors in self.adjacency.items():
            connections = ", ".join(
                f"{destination} ({distance} km)"
                for destination, distance in neighbors
            )

            lines.append(
                f"{location}: {connections}"
            )

        return "\n".join(lines)