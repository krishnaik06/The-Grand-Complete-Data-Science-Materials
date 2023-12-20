from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from ._core._eventloop import get_async_backend
from .abc import CapacityLimiter

T_Retval = TypeVar("T_Retval")


async def run_sync(
    func: Callable[..., T_Retval],
    *args: object,
    cancellable: bool = False,
    limiter: CapacityLimiter | None = None,
) -> T_Retval:
    """
    Call the given function with the given arguments in a worker thread.

    If the ``cancellable`` option is enabled and the task waiting for its completion is
    cancelled, the thread will still run its course but its return value (or any raised
    exception) will be ignored.

    :param func: a callable
    :param args: positional arguments for the callable
    :param cancellable: ``True`` to allow cancellation of the operation
    :param limiter: capacity limiter to use to limit the total amount of threads running
        (if omitted, the default limiter is used)
    :return: an awaitable that yields the return value of the function.

    """
    return await get_async_backend().run_sync_in_worker_thread(
        func, args, cancellable=cancellable, limiter=limiter
    )


def current_default_thread_limiter() -> CapacityLimiter:
    """
    Return the capacity limiter that is used by default to limit the number of
    concurrent threads.

    :return: a capacity limiter object

    """
    return get_async_backend().current_default_thread_limiter()
