from app.models import Delivery


def merge_sort_deliveries(
    deliveries: list[Delivery],
) -> list[Delivery]:
    """
    Sort deliveries by:
    1. Highest priority first
    2. Earliest deadline first

    Uses the Divide-and-Conquer Merge Sort algorithm.
    """

    if len(deliveries) <= 1:
        return deliveries.copy()

    middle = len(deliveries) // 2

    left = merge_sort_deliveries(
        deliveries[:middle]
    )

    right = merge_sort_deliveries(
        deliveries[middle:]
    )

    return _merge(left, right)


def _merge(
    left: list[Delivery],
    right: list[Delivery],
) -> list[Delivery]:

    result: list[Delivery] = []

    left_index = 0
    right_index = 0

    while (
        left_index < len(left)
        and right_index < len(right)
    ):

        left_delivery = left[left_index]
        right_delivery = right[right_index]

        if _comes_before(
            left_delivery,
            right_delivery,
        ):
            result.append(left_delivery)
            left_index += 1

        else:
            result.append(right_delivery)
            right_index += 1

    result.extend(
        left[left_index:]
    )

    result.extend(
        right[right_index:]
    )

    return result


def _comes_before(
    first: Delivery,
    second: Delivery,
) -> bool:
    """
    Returns True when first delivery should appear
    before second delivery.
    """

    if first.priority != second.priority:
        return first.priority > second.priority

    return first.deadline < second.deadline