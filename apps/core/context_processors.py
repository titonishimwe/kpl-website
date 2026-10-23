from datetime import datetime
import zoneinfo

CLOSED_DATES = ["2025-01-01", "2025-07-04", "2026-01-01", "2026-07-04"]

LIBRARY_SCHEDULE = {
    "weekday": {
        "open": 8,
        "close": 20,
        "label": "8:00 AM – 8:00 PM",
    },
    "weekend": {
        "open": 8,
        "close": 17,
        "label": "8:00 AM – 5:00 PM",
    },
}


def library_status(request):
    try:
        kigali_tz = zoneinfo.ZoneInfo("Africa/Kigali")
    except Exception:
        kigali_tz = None

    if kigali_tz:
        now = datetime.now(kigali_tz)
    else:
        now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")

    if date_str in CLOSED_DATES:
        return {
            "library_status": {
                "is_open": False,
                "status": "Closed today",
                "hours": "Closed",
            }
        }

    # weekday(): Monday is 0, Sunday is 6
    is_weekend = now.weekday() in (5, 6)
    schedule = LIBRARY_SCHEDULE["weekend"] if is_weekend else LIBRARY_SCHEDULE["weekday"]

    current_hour = now.hour
    is_open = schedule["open"] <= current_hour < schedule["close"]
    status_text = "We are currently open." if is_open else "We are currently closed."

    return {
        "library_status": {
            "is_open": is_open,
            "status": status_text,
            "hours": schedule["label"],
            "current_year": now.year,
        }
    }
