from concurrent.futures import (
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)
from typing import Callable, TypeVar


T = TypeVar("T")
R = TypeVar("R")


def run_io_tasks(
    tasks: list[Callable[[], T]],
) -> list[T]:
    """
    Execute I/O-oriented tasks concurrently using threads.

    Threads are suitable for tasks that spend time waiting
    for I/O such as files, APIs, or network operations.
    """

    with ThreadPoolExecutor(
        max_workers=min(8, max(1, len(tasks)))
    ) as executor:

        futures = [
            executor.submit(task)
            for task in tasks
        ]

        return [
            future.result()
            for future in futures
        ]


def run_cpu_tasks(
    function: Callable[[T], R],
    inputs: list[T],
) -> list[R]:
    """
    Execute CPU-intensive tasks using processes.

    Separate processes can use multiple CPU cores and
    avoid the limitation of Python's GIL for CPU-bound work.
    """

    if not inputs:
        return []

    with ProcessPoolExecutor() as executor:

        return list(
            executor.map(
                function,
                inputs,
            )
        )


def cpu_square(number: int) -> int:
    """
    Small CPU-task example.

    This function is intentionally defined at module level
    so it can be serialized by multiprocessing.
    """

    return number * number