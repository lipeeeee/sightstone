# Async background thread to run a certain function periodically

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
        
        started (bool): Flag of if the thread was ever started
    """

    fn_to_run: Callable
    time_between_runs: int
    running: bool
    started: bool

    # pylint: disable=R0913
    def __init__(
        self,
        fn_to_run: Callable,
        time_between_runs: int,
        description: str | None = None,
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
        self.description = description
        self.running = False
        self.started = False

    def start(self) -> None:
        """Start running thread"""
        self.running = True
        self.started = True
        super().start()

    def run(self) -> None:
        """Main thread execution"""
        while self.running:
            print(f"THREADING >> RAN: {self.fn_to_run if not self.description else self.description} \
with timeout: {self.time_between_runs}")
            self.fn_to_run()
            sleep(self.time_between_runs)

    def stop(self) -> None:
        """Signal thread to stop executing"""
        self.running = False
