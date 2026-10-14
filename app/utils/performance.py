import time
from contextlib import contextmanager
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar


T = TypeVar("T")


def measure_time(
    function: Callable[..., T],
) -> Callable[..., T]:
    """
    Decorator that measures the execution time
    of a function.
    """

    @wraps(function)
    def wrapper(
        *args: Any,
        **kwargs: Any,
    ) -> T:

        start = time.perf_counter()

        result = function(
            *args,
            **kwargs,
        )

        end = time.perf_counter()

        elapsed = end - start

        print(
            f"[TIMER] {function.__name__}: "
            f"{elapsed:.6f} seconds"
        )

        return result

    return wrapper


@contextmanager
def performance_timer(
    operation_name: str,
) -> Iterator[None]:
    """
    Context manager for measuring the execution
    time of a block of code.
    """

    start = time.perf_counter()

    try:
        yield

    finally:

        end = time.perf_counter()

        elapsed = end - start

        print(
            f"[CONTEXT TIMER] {operation_name}: "
            f"{elapsed:.6f} seconds"
        )
        