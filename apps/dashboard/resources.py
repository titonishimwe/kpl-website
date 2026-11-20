"""Content types managed through the dashboard's generic list / add / edit / delete screens.

To make another model editable, add a Resource here; the URLs, sidebar entry and
screens come from this table.
"""
from dataclasses import dataclass, field

from django.forms import modelform_factory

from apps.core.models import ClosedDay, Event, HomeSlide, ImpactStat, Space, StaffPick

from .forms import StyledModelForm


@dataclass
class Resource:
    slug: str
    model: type
    title: str            # plural, for headings and the sidebar
    singular: str
    icon: str             # Bootstrap Icons name
    fields: list
    columns: list         # (attribute, heading)
    search: list = field(default_factory=list)
    filters: list = field(default_factory=list)   # model fields with choices / booleans
    help: str = ""
    public_url: str = ""  # where the content appears on the site

    def form_class(self):
        return modelform_factory(self.model, form=StyledModelForm, fields=self.fields)


RESOURCES = {
    r.slug: r
    for r in [
        Resource(
            slug="events",
            model=Event,
            title="Events",
            singular="event",
            icon="calendar-event",
            fields=["title", "description", "event_date", "date_text", "location", "link", "image", "is_featured"],
            columns=[("title", "Title"), ("event_date", "Date"), ("date_text", "Time shown"), ("location", "Location"), ("is_featured", "On homepage")],
            search=["title", "location", "description"],
            filters=["is_featured"],
            help="Events dated today or later appear on the Events page. Tick “featured” to show one on the homepage.",
            public_url="/events/",
        ),
        Resource(
            slug="spaces",
            model=Space,
            title="Spaces & Rooms",
            singular="space",
            icon="door-open",
            fields=["name", "category", "capacity_label", "description", "image", "half_day_rate", "full_day_rate", "is_active", "order"],
            columns=[("image", ""), ("name", "Name"), ("category", "Type"), ("capacity_label", "Capacity"), ("half_day_rate", "Half day"), ("full_day_rate", "Full day"), ("is_active", "Bookable")],
            search=["name", "description"],
            filters=["category", "is_active"],
            help="Bookable spaces appear on the Meeting Rooms and Discussion Rooms pages and in the reservation form.",
            public_url="/spaces/",
        ),
        Resource(
            slug="staff-picks",
            model=StaffPick,
            title="Staff Picks",
            singular="staff pick",
            icon="bookmark-star",
            fields=["title", "author", "category", "cover_image", "note", "recommended_by", "is_active", "order", "added_on"],
            columns=[("cover_image", ""), ("title", "Title"), ("author", "Author"), ("category", "Shelf"), ("recommended_by", "Recommended by"), ("added_on", "Added"), ("is_active", "On homepage")],
            search=["title", "author", "recommended_by"],
            filters=["category", "is_active"],
            help="Refresh every two weeks: untick “Show on homepage” on older picks and add new ones.",
            public_url="/",
        ),
        Resource(
            slug="impact",
            model=ImpactStat,
            title="Impact Figures",
            singular="impact figure",
            icon="graph-up-arrow",
            fields=["value", "label", "icon", "order", "is_active"],
            columns=[("value", "Figure"), ("label", "Label"), ("icon", "Icon"), ("order", "Order"), ("is_active", "On homepage")],
            search=["label"],
            help="The “Our Impact” section on the homepage appears once at least one figure is shown.",
            public_url="/",
        ),
        Resource(
            slug="slides",
            model=HomeSlide,
            title="Homepage Slides",
            singular="slide",
            icon="images",
            fields=["title", "caption", "image", "link", "is_active", "order"],
            columns=[("image", ""), ("title", "Title"), ("caption", "Caption"), ("order", "Order"), ("is_active", "On homepage")],
            search=["title", "caption"],
            help="Slides rotate in the “What’s Happening at the Library” carousel. Landscape images work best.",
            public_url="/",
        ),
        Resource(
            slug="closures",
            model=ClosedDay,
            title="Closure Days",
            singular="closure day",
            icon="calendar-x",
            fields=["date", "reason"],
            columns=[("date", "Date"), ("reason", "Reason")],
            search=["reason"],
            help="On these dates the website shows the library as closed.",
        ),
    ]
}
