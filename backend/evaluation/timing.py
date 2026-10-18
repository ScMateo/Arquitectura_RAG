"""Non-invasive instrumentation (PLAN_VALIDACION.md §9, Option A).

Measures per-stage latency and resource usage from the evaluation runner
without modifying the application code: the runner wraps the collaborators it
builds with timing decorators and samples CPU/RAM with psutil.
"""

from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from typing import Any

import psutil  # type: ignore[import-untyped]


class StageTimer:
    """Acumula duraciones por etapa nombrada."""

    def __init__(self) -> None:
        self._durations: dict[str, list[float]] = {}

    @contextmanager
    def measure(self, label: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self._durations.setdefault(label, []).append(time.perf_counter() - start)

    def record(self, label: str, duration: float) -> None:
        self._durations.setdefault(label, []).append(duration)

    def durations(self, label: str) -> list[float]:
        return list(self._durations.get(label, []))

    def reset(self) -> None:
        self._durations.clear()


class ResourceMonitor:
    """Muestrea CPU y RAM del proceso en un hilo durante una fase."""

    def __init__(self, interval: float = 0.1) -> None:
        self._interval = interval
        self._process = psutil.Process()
        self._thread: threading.Thread | None = None
        self._running = False
        self.peak_rss_mb = 0.0
        self.cpu_seconds = 0.0
        self.wall_seconds = 0.0

    def _sample(self) -> None:
        while self._running:
            rss = self._process.memory_info().rss / (1024 * 1024)
            self.peak_rss_mb = max(self.peak_rss_mb, rss)
            time.sleep(self._interval)

    def start(self) -> None:
        self.peak_rss_mb = self._process.memory_info().rss / (1024 * 1024)
        self.cpu_seconds = sum(self._process.cpu_times()[:2])
        self.wall_seconds = time.perf_counter()
        self._running = True
        self._thread = threading.Thread(target=self._sample, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._running = False
        if self._thread is not None:
            self._thread.join(timeout=1.0)
        self.wall_seconds = time.perf_counter() - self.wall_seconds
        self.cpu_seconds = sum(self._process.cpu_times()[:2]) - self.cpu_seconds

    @property
    def cpu_percent(self) -> float:
        if self.wall_seconds <= 0:
            return 0.0
        return 100.0 * self.cpu_seconds / self.wall_seconds


def instrument(timer: StageTimer, target: Any, attribute: str, label: str) -> None:
    """Envuelve un método del colaborador para medir su duración (Option A)."""
    original = getattr(target, attribute)

    def wrapper(*args, **kwargs):
        with timer.measure(label):
            return original(*args, **kwargs)

    setattr(target, attribute, wrapper)
