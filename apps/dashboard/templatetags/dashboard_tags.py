import datetime

from django import template
from django.db.models import fields as model_fields
from django.db.models.fields.files import FieldFile
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.safestring import mark_safe

register = template.Library()

STATUS_STYLES = {
    "pending": "warning",
    "approved": "success",
    "confirmed": "success",
    "rejected": "danger",
    "cancelled": "secondary",
}


@register.simple_tag
def cell(obj, attr):
    """Render one column of a generic list row."""
    display = getattr(obj, f"get_{attr}_display", None)
    value = display() if callable(display) else getattr(obj, attr, "")

    if isinstance(value, bool):
        if value:
            return mark_safe('<span class="badge rounded-pill bg-success-subtle text-success-emphasis">Yes</span>')
        return mark_safe('<span class="badge rounded-pill text-bg-light text-secondary border">No</span>')
    if isinstance(value, FieldFile):
        if value:
            return format_html('<img src="{}" alt="" class="dash-thumb">', value.url)
        return mark_safe('<span class="dash-thumb dash-thumb-empty"><i class="bi bi-image"></i></span>')
    if isinstance(value, datetime.datetime):
        return value.strftime("%d %b %Y, %H:%M")
    if isinstance(value, datetime.date):
        return value.strftime("%d %b %Y")
    if value in ("", None):
        return mark_safe('<span class="text-body-tertiary">—</span>')
    text = str(value)
    return text if len(text) <= 70 else text[:67] + "…"


@register.simple_tag
def status_badge(obj):
    style = STATUS_STYLES.get(obj.status, "secondary")
    return format_html(
        '<span class="badge rounded-pill status-badge bg-{}-subtle text-{}-emphasis">{}</span>',
        style, style, obj.get_status_display(),
    )


@register.simple_tag(takes_context=True)
def query_with(context, **kwargs):
    """Current query string with some parameters replaced (for pagination and filters)."""
    params = context["request"].GET.copy()
    for key, value in kwargs.items():
        if value in (None, ""):
            params.pop(key, None)
        else:
            params[key] = value
    return "?" + urlencode(params, doseq=True) if params else "?"


@register.filter
def field_choices(model, name):
    """Choices for a filter dropdown: the field's choices, or Yes/No for booleans."""
    f = model._meta.get_field(name)
    if isinstance(f, model_fields.BooleanField):
        return [("1", "Yes"), ("0", "No")]
    return [(str(k), v) for k, v in f.choices]


@register.filter
def field_label(model, name):
    return model._meta.get_field(name).verbose_name.capitalize()


@register.filter
def get_item(mapping, key):
    return mapping.get(key)


@register.simple_tag
def pending_counts():
    """Badges for the sidebar: requests waiting for staff action."""
    from apps.core.models import MembershipApplication, RoomReservation

    return {
        "applications": MembershipApplication.objects.filter(status="pending").count(),
        "reservations": RoomReservation.objects.filter(status="pending").count(),
    }
