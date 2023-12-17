"""Asyncronhous background thread

Made to run a certain function continuously between a 
set period of time
"""

from time import sleep
from threading import Thread
from typing import Callable, Any, Iterable, Mapping

class BackgroundThread(Thread):
    """Background Assynchronous thread

    Runs a function in the background on a set timer. Can be edited
    to support float timers

    Attributes:
        fn_to_run (Callable): Function to run

        time_between_runs (int): Time in seconds of how often the
        `fn_to_run` should be ran

        running (bool): Flag of if the thread is being ran
    """

    fn_to_run: Callable
    time_between_runs: int
    running: bool

    # pylint: disable=R0913
    def __init__(
        self,
        fn_to_run: Callable,
        time_between_runs: int,
        group: None = None,
        target: Callable[..., object] | None = None,
        name: str | None = None,
        args: Iterable[Any] = ..., # pyright: ignore
        kwargs: Mapping[str, Any] | None = None,
        *,
        daemon: bool | None = None
    ) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.fn_to_run = fn_to_run
        self.time_between_runs = time_between_runs
        self.running = False

    def start(self) -> None:
        """Start running thread"""
        self.running = True
        return super().start()

    def run(self) -> None:
        """Main thread execution"""
        while self.running:
            self.fn_to_run()
            sleep(self.time_between_runs)

    def stop(self) -> None:
        """Signal thread to stop executing"""
        self.running = False
