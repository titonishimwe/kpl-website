from datetime import datetime
import zoneinfo

from django.db import DatabaseError

from .models import ClosedDay, SiteSettings


def _format_time(t):
    """08:00 -> '8:00 AM'."""
    return t.strftime("%I:%M %p").lstrip("0")


def _load_settings():
    try:
        return SiteSettings.load()
    except DatabaseError:
        # Tables not migrated yet (first deploy, management commands): fall back to defaults.
        return SiteSettings()


def site_settings(request):
    """Contact details, hours and homepage content that staff edit in the dashboard."""
    site = _load_settings()
    site.weekday_hours = f"{_format_time(site.weekday_open)} – {_format_time(site.weekday_close)}"
    site.weekend_hours = f"{_format_time(site.weekend_open)} – {_format_time(site.weekend_close)}"
    return {"site": site}


def library_status(request):
    now = datetime.now(zoneinfo.ZoneInfo("Africa/Kigali"))
    site = _load_settings()

    try:
        closed_today = ClosedDay.objects.filter(date=now.date()).first()
    except DatabaseError:
        closed_today = None

    if closed_today:
        return {
            "library_status": {
                "is_open": False,
                "status": f"Closed today{': ' + closed_today.reason if closed_today.reason else ''}",
                "hours": "Closed",
                "current_year": now.year,
            }
        }

    # weekday(): Monday is 0, Sunday is 6
    if now.weekday() in (5, 6):
        open_t, close_t = site.weekend_open, site.weekend_close
    else:
        open_t, close_t = site.weekday_open, site.weekday_close

    is_open = open_t <= now.time() < close_t
    return {
        "library_status": {
            "is_open": is_open,
            "status": "We are currently open." if is_open else "We are currently closed.",
            "hours": f"{_format_time(open_t)} – {_format_time(close_t)}",
            "current_year": now.year,
        }
    }
