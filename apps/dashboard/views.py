import csv
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View

from apps.core.models import (
    Event, HomeSlide, ImpactStat, MembershipApplication, RoomReservation, SiteSettings, StaffPick,
)

from . import reports
from .forms import ApplicationReviewForm, ReservationReviewForm, SiteSettingsForm, StaffUserCreationForm
from .resources import RESOURCES

User = get_user_model()
PAGE_SIZE = 25


# ---------------------------------------------------------------- access

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Logged-in, active staff only. Anonymous users go to the login page; others get 403."""

    login_url = "accounts:login"

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_staff


class SuperuserRequiredMixin(StaffRequiredMixin):
    def test_func(self):
        return self.request.user.is_active and self.request.user.is_superuser


def _parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def _mark_reviewed(obj, user):
    obj.reviewed_by = user
    obj.reviewed_at = timezone.now()


def _pdf_response(content, filename, inline=True):
    response = HttpResponse(content, content_type="application/pdf")
    response["Content-Disposition"] = f'{"inline" if inline else "attachment"}; filename="{filename}"'
    return response


# ---------------------------------------------------------------- overview

def _add_months(d, n):
    y, m = divmod(d.month - 1 + n, 12)
    return d.replace(year=d.year + y, month=m + 1, day=1)


def _month_series(qs, date_lookup, months=12):
    """Counts per month for the last `months` months (oldest first), including empty months.

    `date_lookup` is the field path to compare with dates, e.g. "created_at__date" or "reservation_date".
    """
    start = _add_months(timezone.localdate().replace(day=1), -(months - 1))
    field = date_lookup.split("__")[0]
    counts = {
        row["m"].strftime("%Y-%m"): row["n"]
        for row in qs.filter(**{f"{date_lookup}__gte": start})
        .annotate(m=TruncMonth(field)).values("m").annotate(n=Count("id"))
    }
    labels, values = [], []
    for i in range(months):
        month = _add_months(start, i)
        labels.append(month.strftime("%b %Y"))
        values.append(counts.get(month.strftime("%Y-%m"), 0))
    return labels, values


class DashboardHomeView(StaffRequiredMixin, View):
    def get(self, request):
        today = timezone.localdate()
        month_start = today.replace(day=1)
        last_month_start = (month_start - timedelta(days=1)).replace(day=1)

        apps_qs = MembershipApplication.objects.all()
        res_qs = RoomReservation.objects.all()
        app_status = dict(apps_qs.values_list("status").annotate(n=Count("id")))
        res_status = dict(res_qs.values_list("status").annotate(n=Count("id")))

        this_month = apps_qs.filter(created_at__date__gte=month_start).count()
        last_month = apps_qs.filter(created_at__date__gte=last_month_start, created_at__date__lt=month_start).count()

        labels, app_series = _month_series(apps_qs, "created_at__date")
        _, res_series = _month_series(res_qs, "reservation_date")

        type_labels = dict(MembershipApplication.MEMBERSHIP_CHOICES)
        by_type = [
            (type_labels.get(k, k).split(" (")[0], n)
            for k, n in apps_qs.values_list("membership_type").annotate(n=Count("id")).order_by("-n")
        ]
        by_space = list(res_qs.values_list("space_type").annotate(n=Count("id")).order_by("-n")[:6])

        # Things staff should act on.
        site = SiteSettings.load()
        attention = []
        if app_status.get("pending"):
            attention.append(("person-vcard", f"{app_status['pending']} membership application(s) waiting for review",
                              reverse("dashboard:applications") + "?status=pending"))
        if res_status.get("pending"):
            attention.append(("calendar-check", f"{res_status['pending']} reservation request(s) waiting for confirmation",
                              reverse("dashboard:reservations") + "?status=pending"))
        latest_pick = StaffPick.objects.filter(is_active=True).order_by("-added_on").first()
        if not latest_pick:
            attention.append(("bookmark-star", "No Staff Picks yet: the homepage is showing sample books",
                              reverse("dashboard:resource_add", args=["staff-picks"])))
        elif (today - latest_pick.added_on).days > 14:
            attention.append(("bookmark-star", f"Staff Picks last updated {(today - latest_pick.added_on).days} days ago (due every two weeks)",
                              reverse("dashboard:resource_list", args=["staff-picks"])))
        if not ImpactStat.objects.filter(is_active=True).exists():
            attention.append(("graph-up-arrow", "Add impact figures to show the “Our Impact” section on the homepage",
                              reverse("dashboard:resource_add", args=["impact"])))
        if not site.hero_image:
            attention.append(("image", "Upload a homepage cover photo of readers and activities at the library",
                              reverse("dashboard:settings")))
        if not Event.objects.filter(event_date__gte=today).exists():
            attention.append(("calendar-event", "No upcoming events are published",
                              reverse("dashboard:resource_add", args=["events"])))

        context = {
            "stats": {
                "applications_total": apps_qs.count(),
                "applications_pending": app_status.get("pending", 0),
                "members_approved": app_status.get("approved", 0),
                "applications_this_month": this_month,
                "applications_change": this_month - last_month,
                "reservations_pending": res_status.get("pending", 0),
                "reservations_upcoming": res_qs.filter(reservation_date__gte=today, status="confirmed").count(),
                "events_upcoming": Event.objects.filter(event_date__gte=today).count(),
                "users_total": User.objects.count(),
            },
            "chart": {
                "labels": labels,
                "applications": app_series,
                "reservations": res_series,
                "type_labels": [t for t, _ in by_type],
                "type_values": [n for _, n in by_type],
                "space_labels": [s for s, _ in by_space],
                "space_values": [n for _, n in by_space],
            },
            "attention": attention,
            "recent_applications": apps_qs.order_by("-created_at")[:6],
            "upcoming_reservations": res_qs.filter(reservation_date__gte=today).exclude(status="cancelled")
            .order_by("reservation_date")[:6],
            "upcoming_events": Event.objects.filter(event_date__gte=today).order_by("event_date")[:5],
            "content_counts": {
                "Staff Picks": StaffPick.objects.filter(is_active=True).count(),
                "Impact figures": ImpactStat.objects.filter(is_active=True).count(),
                "Homepage slides": HomeSlide.objects.filter(is_active=True).count(),
            },
        }
        return render(request, "dashboard/home.html", context)


# ---------------------------------------------------------------- membership applications

def _filtered_applications(request):
    qs = MembershipApplication.objects.select_related("reviewed_by")
    g = request.GET
    summary = []
    if q := g.get("q", "").strip():
        qs = qs.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q)
            | Q(phone__icontains=q) | Q(id_passport__icontains=q)
        )
        summary.append(f'search "{q}"')
    if (status := g.get("status")) in dict(MembershipApplication.STATUS_CHOICES):
        qs = qs.filter(status=status)
        summary.append(f"status: {dict(MembershipApplication.STATUS_CHOICES)[status]}")
    if (mtype := g.get("type")) in dict(MembershipApplication.MEMBERSHIP_CHOICES):
        qs = qs.filter(membership_type=mtype)
        summary.append(f"type: {dict(MembershipApplication.MEMBERSHIP_CHOICES)[mtype]}")
    if d_from := _parse_date(g.get("from")):
        qs = qs.filter(created_at__date__gte=d_from)
        summary.append(f"from {d_from:%d %b %Y}")
    if d_to := _parse_date(g.get("to")):
        qs = qs.filter(created_at__date__lte=d_to)
        summary.append(f"to {d_to:%d %b %Y}")
    text = "Filters: " + ", ".join(summary) if summary else "All applications"
    return qs.order_by("-created_at"), text


class ApplicationListView(StaffRequiredMixin, View):
    def get(self, request):
        qs, filter_summary = _filtered_applications(request)
        page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
        return render(request, "dashboard/applications/list.html", {
            "page": page,
            "total": qs.count(),
            "filter_summary": filter_summary,
            "status_choices": MembershipApplication.STATUS_CHOICES,
            "type_choices": MembershipApplication.MEMBERSHIP_CHOICES,
        })

    def post(self, request):
        """Bulk status change for the ticked applications."""
        status = request.POST.get("bulk_status")
        ids = request.POST.getlist("selected")
        if status in dict(MembershipApplication.STATUS_CHOICES) and ids:
            n = MembershipApplication.objects.filter(pk__in=ids).update(
                status=status, reviewed_by=request.user, reviewed_at=timezone.now()
            )
            messages.success(request, f"{n} application(s) marked as {dict(MembershipApplication.STATUS_CHOICES)[status].lower()}.")
        else:
            messages.warning(request, "Select at least one application and an action.")
        return redirect(request.get_full_path())


class ApplicationDetailView(StaffRequiredMixin, View):
    def get(self, request, pk):
        app = get_object_or_404(MembershipApplication, pk=pk)
        return render(request, "dashboard/applications/detail.html", {
            "app": app, "form": ApplicationReviewForm(instance=app),
        })

    def post(self, request, pk):
        app = get_object_or_404(MembershipApplication, pk=pk)
        form = ApplicationReviewForm(request.POST, instance=app)
        if quick := request.POST.get("quick_status"):
            # One-click Approve / Reject buttons keep the existing notes.
            form = ApplicationReviewForm({"status": quick, "staff_notes": app.staff_notes}, instance=app)
        if form.is_valid():
            app = form.save(commit=False)
            _mark_reviewed(app, request.user)
            app.save()
            messages.success(request, f"Application from {app.first_name} {app.last_name} is now {app.get_status_display().lower()}.")
            return redirect("dashboard:application_detail", pk=app.pk)
        return render(request, "dashboard/applications/detail.html", {"app": app, "form": form})


class ApplicationReportView(StaffRequiredMixin, View):
    """PDF of the applications matching the current list filters."""

    def get(self, request):
        qs, filter_summary = _filtered_applications(request)
        pdf = reports.membership_report(qs, filter_summary, request.user)
        return _pdf_response(pdf, f"kpl-membership-applications-{timezone.localdate():%Y%m%d}.pdf")


class ApplicationPdfView(StaffRequiredMixin, View):
    def get(self, request, pk):
        app = get_object_or_404(MembershipApplication.objects.select_related("reviewed_by"), pk=pk)
        pdf = reports.application_detail_pdf(app, request.user)
        return _pdf_response(pdf, f"kpl-application-{app.pk}.pdf")


class ApplicationCsvView(StaffRequiredMixin, View):
    def get(self, request):
        qs, _ = _filtered_applications(request)
        response = HttpResponse(content_type="text/csv; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="kpl-membership-applications-{timezone.localdate():%Y%m%d}.csv"'
        response.write("﻿")  # so Excel opens it as UTF-8
        w = csv.writer(response)
        w.writerow(["ID", "First name", "Last name", "Date of birth", "Gender", "ID / Passport", "Phone", "Email",
                    "District", "Province", "Membership", "Payment", "Status", "Submitted", "Staff notes"])
        for a in qs:
            w.writerow([a.pk, a.first_name, a.last_name, a.dob, a.get_gender_display(), a.id_passport, a.phone,
                        a.email, a.district, a.province, a.get_membership_type_display(),
                        a.get_payment_method_display(), a.get_status_display(),
                        timezone.localtime(a.created_at).strftime("%Y-%m-%d %H:%M"), a.staff_notes])
        return response


# ---------------------------------------------------------------- reservations

def _filtered_reservations(request):
    qs = RoomReservation.objects.select_related("reviewed_by")
    g = request.GET
    summary = []
    if q := g.get("q", "").strip():
        qs = qs.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(phone__icontains=q)
                       | Q(organization__icontains=q) | Q(space_type__icontains=q))
        summary.append(f'search "{q}"')
    if (status := g.get("status")) in dict(RoomReservation.STATUS_CHOICES):
        qs = qs.filter(status=status)
        summary.append(f"status: {dict(RoomReservation.STATUS_CHOICES)[status]}")
    when = g.get("when", "upcoming")
    today = timezone.localdate()
    if when == "upcoming":
        qs = qs.filter(reservation_date__gte=today).order_by("reservation_date", "created_at")
        summary.append("upcoming")
    elif when == "past":
        qs = qs.filter(reservation_date__lt=today).order_by("-reservation_date")
        summary.append("past")
    else:
        qs = qs.order_by("-reservation_date")
    text = "Reservations: " + ", ".join(summary) if summary else "All reservations"
    return qs, text, when


class ReservationListView(StaffRequiredMixin, View):
    def get(self, request):
        qs, filter_summary, when = _filtered_reservations(request)
        page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
        return render(request, "dashboard/reservations/list.html", {
            "page": page, "total": qs.count(), "when": when,
            "status_choices": RoomReservation.STATUS_CHOICES,
        })


class ReservationDetailView(StaffRequiredMixin, View):
    def get(self, request, pk):
        res = get_object_or_404(RoomReservation, pk=pk)
        clashes = RoomReservation.objects.filter(
            space_type=res.space_type, reservation_date=res.reservation_date
        ).exclude(pk=res.pk).exclude(status="cancelled")
        return render(request, "dashboard/reservations/detail.html", {
            "res": res, "form": ReservationReviewForm(instance=res), "clashes": clashes,
        })

    def post(self, request, pk):
        res = get_object_or_404(RoomReservation, pk=pk)
        data = request.POST
        if quick := data.get("quick_status"):
            data = {"status": quick, "staff_notes": res.staff_notes}
        form = ReservationReviewForm(data, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            _mark_reviewed(res, request.user)
            res.save()
            messages.success(request, f"Reservation for {res.name} is now {res.get_status_display().lower()}.")
            return redirect("dashboard:reservation_detail", pk=res.pk)
        return render(request, "dashboard/reservations/detail.html", {"res": res, "form": form, "clashes": []})


class ReservationReportView(StaffRequiredMixin, View):
    def get(self, request):
        qs, filter_summary, _ = _filtered_reservations(request)
        pdf = reports.reservations_report(qs, filter_summary, request.user)
        return _pdf_response(pdf, f"kpl-reservations-{timezone.localdate():%Y%m%d}.pdf")


# ---------------------------------------------------------------- generic content screens

def _resource(slug):
    try:
        return RESOURCES[slug]
    except KeyError:
        raise Http404("Unknown section")


class ResourceListView(StaffRequiredMixin, View):
    def get(self, request, slug):
        res = _resource(slug)
        qs = res.model.objects.all()
        if (q := request.GET.get("q", "").strip()) and res.search:
            cond = Q()
            for f in res.search:
                cond |= Q(**{f"{f}__icontains": q})
            qs = qs.filter(cond)
        active_filters = {}
        for f in res.filters:
            value = request.GET.get(f)
            if value not in (None, ""):
                field = res.model._meta.get_field(f)
                qs = qs.filter(**{f: value == "1" if field.get_internal_type() == "BooleanField" else value})
                active_filters[f] = value
        page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
        return render(request, "dashboard/resource_list.html", {
            "res": res, "page": page, "total": qs.count(), "active_filters": active_filters,
        })


class ResourceFormView(StaffRequiredMixin, View):
    template = "dashboard/resource_form.html"

    def _get(self, slug, pk):
        res = _resource(slug)
        obj = get_object_or_404(res.model, pk=pk) if pk else None
        return res, obj

    def get(self, request, slug, pk=None):
        res, obj = self._get(slug, pk)
        return render(request, self.template, {"res": res, "obj": obj, "form": res.form_class()(instance=obj)})

    def post(self, request, slug, pk=None):
        res, obj = self._get(slug, pk)
        form = res.form_class()(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            saved = form.save()
            messages.success(request, f"{res.singular.capitalize()} “{saved}” {'updated' if obj else 'added'}.")
            if "save_add" in request.POST:
                return redirect("dashboard:resource_add", slug=slug)
            return redirect("dashboard:resource_list", slug=slug)
        messages.error(request, "Please fix the highlighted fields.")
        return render(request, self.template, {"res": res, "obj": obj, "form": form})


class ResourceDeleteView(StaffRequiredMixin, View):
    def get(self, request, slug, pk):
        res = _resource(slug)
        obj = get_object_or_404(res.model, pk=pk)
        return render(request, "dashboard/confirm_delete.html", {"res": res, "obj": obj})

    def post(self, request, slug, pk):
        res = _resource(slug)
        obj = get_object_or_404(res.model, pk=pk)
        name = str(obj)
        obj.delete()
        messages.success(request, f"{res.singular.capitalize()} “{name}” deleted.")
        return redirect("dashboard:resource_list", slug=slug)


# ---------------------------------------------------------------- site settings

class SiteSettingsView(StaffRequiredMixin, View):
    def get(self, request):
        return render(request, "dashboard/settings.html", {"form": SiteSettingsForm(instance=SiteSettings.load())})

    def post(self, request):
        form = SiteSettingsForm(request.POST, request.FILES, instance=SiteSettings.load())
        if form.is_valid():
            form.save()
            messages.success(request, "Website settings saved. Changes are live on the site.")
            return redirect("dashboard:settings")
        messages.error(request, "Please fix the highlighted fields.")
        return render(request, "dashboard/settings.html", {"form": form})


# ---------------------------------------------------------------- staff users (superusers only)

class UserListView(SuperuserRequiredMixin, View):
    def get(self, request):
        qs = User.objects.order_by("-is_superuser", "-is_staff", "username")
        if q := request.GET.get("q", "").strip():
            qs = qs.filter(Q(username__icontains=q) | Q(email__icontains=q)
                           | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        if request.GET.get("role") == "staff":
            qs = qs.filter(is_staff=True)
        page = Paginator(qs, PAGE_SIZE).get_page(request.GET.get("page"))
        return render(request, "dashboard/users.html", {"page": page, "total": qs.count(), "form": StaffUserCreationForm()})

    def post(self, request):
        form = StaffUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Staff account “{user.username}” created. They can sign in and use the dashboard.")
            return redirect("dashboard:users")
        qs = User.objects.order_by("-is_superuser", "-is_staff", "username")
        page = Paginator(qs, PAGE_SIZE).get_page(1)
        messages.error(request, "The new account could not be created. See the form below.")
        return render(request, "dashboard/users.html", {"page": page, "total": qs.count(), "form": form, "show_form": True})


class UserToggleView(SuperuserRequiredMixin, View):
    FIELDS = {"staff": "is_staff", "active": "is_active"}

    def post(self, request, pk, what):
        user = get_object_or_404(User, pk=pk)
        field = self.FIELDS.get(what)
        if not field:
            raise Http404
        if user == request.user:
            messages.error(request, "You can’t change your own access.")
        elif user.is_superuser:
            messages.error(request, "Superuser accounts can only be changed in the Django admin.")
        else:
            setattr(user, field, not getattr(user, field))
            user.save(update_fields=[field])
            state = "granted" if getattr(user, field) else "removed"
            label = "Dashboard access" if field == "is_staff" else "Account access"
            messages.success(request, f"{label} {state} for {user.username}.")
        return redirect("dashboard:users")
