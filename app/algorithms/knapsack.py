from app.models import Delivery


def optimize_capacity(
    deliveries: list[Delivery],
    capacity: float,
) -> list[Delivery]:
    """
    Select deliveries with maximum priority
    without exceeding the available vehicle capacity.

    Uses 0/1 Knapsack dynamic programming.
    """

    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    if not deliveries or capacity == 0:
        return []

    # DP works with integer capacities.
    capacity_limit = int(capacity)

    dp: list[list[int]] = [
        [0] * (capacity_limit + 1)
        for _ in range(len(deliveries) + 1)
    ]

    for i in range(1, len(deliveries) + 1):

        delivery = deliveries[i - 1]

        weight = int(delivery.weight)
        priority = delivery.priority

        for current_capacity in range(
            capacity_limit + 1
        ):

            # Do not select the delivery.
            dp[i][current_capacity] = dp[
                i - 1
            ][current_capacity]

            # Select the delivery if it fits.
            if weight <= current_capacity:

                selected_value = (
                    dp[i - 1][
                        current_capacity - weight
                    ]
                    + priority
                )

                dp[i][current_capacity] = max(
                    dp[i][current_capacity],
                    selected_value,
                )

    # Reconstruct selected deliveries.
    selected: list[Delivery] = []

    current_capacity = capacity_limit

    for i in range(len(deliveries), 0, -1):

        if dp[i][current_capacity] != dp[
            i - 1
        ][current_capacity]:

            delivery = deliveries[i - 1]

            selected.append(delivery)

            current_capacity -= int(
                delivery.weight
            )

    selected.reverse()

    return selected