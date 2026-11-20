from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from apps.core.models import MembershipApplication, RoomReservation, SiteSettings


class BootstrapMixin:
    """Give every widget the right Bootstrap class and HTML5 input type."""

    def _style_fields(self):
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault("class", "form-check-input")
            elif isinstance(w, (forms.Select, forms.SelectMultiple)):
                w.attrs.setdefault("class", "form-select")
            elif isinstance(w, forms.RadioSelect):
                w.attrs.setdefault("class", "form-check-input")
            else:
                w.attrs.setdefault("class", "form-control")
            if isinstance(w, forms.DateInput):
                w.input_type = "date"
                w.format = "%Y-%m-%d"
            elif isinstance(w, forms.TimeInput):
                w.input_type = "time"
                w.format = "%H:%M"
            elif isinstance(w, forms.Textarea):
                w.attrs.setdefault("rows", 4)


class StyledModelForm(BootstrapMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ReviewForm(StyledModelForm):
    """Status and internal notes on an application or reservation."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["staff_notes"].widget.attrs["rows"] = 3
        self.fields["staff_notes"].widget.attrs["placeholder"] = "Visible to staff only"


class ApplicationReviewForm(ReviewForm):
    class Meta:
        model = MembershipApplication
        fields = ["status", "staff_notes"]


class ReservationReviewForm(ReviewForm):
    class Meta:
        model = RoomReservation
        fields = ["status", "staff_notes"]


class SiteSettingsForm(StyledModelForm):
    class Meta:
        model = SiteSettings
        exclude = ["updated_at"]
        widgets = {
            "weekday_open": forms.TimeInput(),
            "weekday_close": forms.TimeInput(),
            "weekend_open": forms.TimeInput(),
            "weekend_close": forms.TimeInput(),
            "hero_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    # Grouped for the settings page layout.
    SECTIONS = [
        ("Homepage", "house", ["hero_title", "hero_subtitle", "hero_image", "announcement"]),
        ("Contact information", "telephone", ["phone", "email", "address_line1", "address_line2", "map_url", "recruitment_email"]),
        ("Opening hours", "clock", ["weekday_open", "weekday_close", "weekend_open", "weekend_close"]),
        ("Social media", "share", ["facebook_url", "instagram_url", "x_url", "youtube_url"]),
    ]

    def clean(self):
        cleaned = super().clean()
        for day in ("weekday", "weekend"):
            o, c = cleaned.get(f"{day}_open"), cleaned.get(f"{day}_close")
            if o and c and o >= c:
                self.add_error(f"{day}_close", "Closing time must be after opening time.")
        return cleaned

    def sections(self):
        for title, icon, names in self.SECTIONS:
            yield title, icon, [self[name] for name in names]


class StaffUserCreationForm(BootstrapMixin, UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True
        self._style_fields()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user
