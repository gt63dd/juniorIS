from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class DropConfig:
    """Configuration for the limited inventory drop."""

    drop_start: datetime


DEFAULT_DROP_START = datetime(2026, 3, 1, 15, 0, 0, tzinfo=timezone.utc)


DEFAULT_CONFIG = DropConfig(drop_start=DEFAULT_DROP_START)
