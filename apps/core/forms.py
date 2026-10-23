from django import forms
from .models import MembershipApplication, RoomReservation


class MembershipApplicationForm(forms.ModelForm):
    # Honeypot field
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    terms_confirmed = forms.BooleanField(
        required=True,
        label="I confirm that the information provided is accurate and I agree to abide by Kigali Public Library membership policies and borrowing regulations.",
    )

    class Meta:
        model = MembershipApplication
        exclude = ["status", "created_at"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name *"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name *"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "id_passport": forms.TextInput(attrs={"class": "form-control", "placeholder": "National ID / Passport *"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number *"}),
            "alt_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Alternative Phone Number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address *"}),
            "alt_email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Alternative Email Address"}),
            "village": forms.TextInput(attrs={"class": "form-control", "placeholder": "Village"}),
            "sector": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sector"}),
            "district": forms.TextInput(attrs={"class": "form-control", "placeholder": "District"}),
            "province": forms.TextInput(attrs={"class": "form-control", "placeholder": "Province"}),
            "guardian_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Parent / Guardian Name *"}),
            "guardian_relationship": forms.TextInput(attrs={"class": "form-control", "placeholder": "Relationship *"}),
            "guardian_id": forms.TextInput(attrs={"class": "form-control", "placeholder": "Parent / Guardian ID *"}),
            "guardian_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Parent / Guardian Phone *"}),
            "membership_type": forms.Select(attrs={"class": "form-select"}),
            "payment_method": forms.RadioSelect(attrs={"class": "form-check-input"}),
            "document": forms.FileInput(attrs={"class": "form-control", "accept": ".pdf,.jpg,.jpeg,.png"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return cleaned_data


class RoomReservationForm(forms.ModelForm):
    class Meta:
        model = RoomReservation
        exclude = ["status", "created_at"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name *"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email Address *"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number *"}),
            "organization": forms.TextInput(attrs={"class": "form-control", "placeholder": "Organization / Company (optional)"}),
            "space_type": forms.Select(attrs={"class": "form-select"}),
            "reservation_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "duration": forms.Select(attrs={"class": "form-select"}),
            "attendees_count": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "purpose": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Briefly describe your event or meeting purpose..."}),
        }
