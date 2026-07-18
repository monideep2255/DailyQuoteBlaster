#!/usr/bin/env python3
"""Single-shot send entrypoint for GitHub Actions cron.

The original scheduler.py runs an infinite loop and sleeps until 07:00 and 21:00.
GitHub Actions runs once per trigger, so this entrypoint sends once and exits.

Daylight saving is handled without a paid scheduler: the workflow fires at all
candidate UTC times for 7 AM and 9 PM Eastern, and this script only sends when
the current America/New_York hour actually matches. On every other trigger it
exits quietly. That keeps sends correct across EST and EDT.

Usage:
    python run_scheduled.py            # auto-detect slot from Eastern time
    python run_scheduled.py morning    # force morning send (manual/testing)
    python run_scheduled.py evening    # force evening send (manual/testing)
"""

import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from logger import get_logger
from scheduler import send_morning_quotes, send_evening_quotes

logger = get_logger(__name__)

EASTERN = ZoneInfo("America/New_York")
MORNING_HOUR = 7
EVENING_HOUR = 21


def resolve_slot(arg):
    """Return 'morning', 'evening', or None based on the arg or Eastern time."""
    if arg in ("morning", "evening"):
        return arg
    hour = datetime.now(EASTERN).hour
    if hour == MORNING_HOUR:
        return "morning"
    if hour == EVENING_HOUR:
        return "evening"
    return None


def main():
    arg = sys.argv[1].lower() if len(sys.argv) > 1 else "auto"
    slot = resolve_slot(arg)

    if slot is None:
        now = datetime.now(EASTERN).strftime("%Y-%m-%d %H:%M %Z")
        logger.info(f"No send slot for current Eastern time ({now}); exiting without sending.")
        return 0

    logger.info(f"Running single-shot {slot} send.")
    if slot == "morning":
        ok = send_morning_quotes()
    else:
        ok = send_evening_quotes()

    logger.info(f"{slot} send finished, success={ok}")
    # Exit 0 even when there are no subscribers; a no-op is not a failure.
    return 0


if __name__ == "__main__":
    sys.exit(main())
