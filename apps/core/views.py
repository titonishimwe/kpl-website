from django.shortcuts import render, redirect
from django.contrib import messages
from .models import MembershipApplication, RoomReservation, Event, BookArrival
from .forms import MembershipApplicationForm, RoomReservationForm


def home(request):
    events = Event.objects.filter(is_featured=True)
    if not events.exists():
        events = [
            {
                "title": "Storytime",
                "date_text": "November 14, 9:30–9:50 a.m.",
                "location": "Kid's Zone",
                "link": "#",
            },
            {
                "title": "Read a loud session",
                "date_text": "November 14, 10:00–10:30 a.m.",
                "location": "Conference Room",
                "link": "#",
            },
            {
                "title": "Book Club Meeting",
                "date_text": "November 15, 2:00–3:00 p.m.",
                "location": "Meeting Room 1",
                "link": "#",
            },
            {
                "title": "Author Talk: Jane Doe",
                "date_text": "November 16, 6:00–7:30 p.m.",
                "location": "Auditorium",
                "link": "#",
            },
        ]

    # Sample books fallback
    default_books = [
        {"title": "A Thousand Splendid Suns", "cover": "images/covers/athousand.jpg"},
        {"title": "Jacaranda", "cover": "images/covers/jacaranda.jpg"},
        {"title": "Dream Count", "cover": "images/covers/dreamcount.webp"},
        {"title": "The Richest Man in Babylon", "cover": "images/covers/richestman.jpeg"},
        {"title": "Rich Dad Poor Dad", "cover": "images/covers/richdad.jpg"},
    ]

    adult_books = list(BookArrival.objects.filter(category="adult"))
    if not adult_books:
        adult_books = default_books

    teen_books = list(BookArrival.objects.filter(category="teens"))
    if not teen_books:
        teen_books = [
            {"title": "Diary of a Wimpy Kid", "cover": "images/covers/wimpykid.jpg"},
            {"title": "The Odyssey", "cover": "images/covers/odyssey.jpg"},
            {"title": "A Thousand Splendid Suns", "cover": "images/covers/athousand.jpg"},
            {"title": "Dream Count", "cover": "images/covers/dreamcount.webp"},
        ]

    kid_books = list(BookArrival.objects.filter(category="kids"))
    if not kid_books:
        kid_books = [
            {"title": "Sulwe", "cover": "images/covers/sulwe.jpeg"},
            {"title": "Diary of a Wimpy Kid", "cover": "images/covers/wimpykid.jpg"},
            {"title": "Dock", "cover": "images/covers/dock.jpeg"},
            {"title": "Jacaranda", "cover": "images/covers/jacaranda.jpg"},
        ]

    quick_links = [
        {
            "href": "/membership/",
            "icon": "images/icons/card.svg",
            "title": "Get a library card",
            "external": False,
        },
        {
            "href": "https://kplonline.overdrive.com/",
            "icon": "images/icons/digital.svg",
            "title": "Digital Library",
            "external": True,
        },
        {
            "href": "/spaces/reserve/",
            "icon": "images/icons/room.svg",
            "title": "Reserve a Room",
            "external": False,
        },
        {
            "href": "/events/",
            "icon": "images/icons/events.svg",
            "title": "Events",
            "external": False,
        },
    ]

    carousel_slides = [
        {"image": "images/events/jacaranda.png", "alt": "Jacaranda Event", "title": "Jacaranda Cultural Night"},
        {"image": "images/bg/firstlady.jpg", "alt": "First Lady Event", "title": "First Lady Community Session"},
    ]

    context = {
        "events": events,
        "adult_books": adult_books,
        "teen_books": teen_books,
        "kid_books": kid_books,
        "quick_links": quick_links,
        "carousel_slides": carousel_slides,
    }
    return render(request, "core/home.html", context)


def about(request):
    values = [
        {
            "title": "Inclusion",
            "text": "We ensure equal access to knowledge, programs, and opportunities that promote human and social development.",
        },
        {
            "title": "Quality Services",
            "text": "We deliver impactful educational, cultural, and community services that create measurable value.",
        },
        {
            "title": "Integrity",
            "text": "We uphold transparency, accountability, and ethical conduct in all our engagements.",
        },
        {
            "title": "Adaptability",
            "text": "We embrace innovation and technology to remain relevant in an evolving global landscape.",
        },
        {
            "title": "Collaboration",
            "text": "We cultivate partnerships that amplify impact and accelerate transformative change.",
        },
    ]
    return render(request, "core/about.html", {"values": values})


def careers(request):
    principles = [
        {
            "title": "Meaningful Work",
            "description": "Every role contributes to expanding access to knowledge, learning opportunities, and community engagement across Rwanda.",
        },
        {
            "title": "Collaborative Culture",
            "description": "Work alongside professionals who are passionate about education, innovation, culture, and public service.",
        },
        {
            "title": "Professional Growth",
            "description": "Develop your skills through continuous learning, new challenges, and opportunities to make a lasting impact.",
        },
    ]
    qualities = [
        "Passion for Learning",
        "Service Excellence",
        "Integrity",
        "Collaboration",
        "Innovation",
        "Community Impact",
    ]
    return render(request, "core/careers.html", {
        "principles": principles,
        "qualities": qualities,
    })


def privacy(request):
    return render(request, "core/privacy.html")


def spaces_overview(request):
    spaces = [
        {
            "title": "MEETING ROOMS",
            "url": "core:meeting_rooms",
            "description": "Flexible spaces designed for meetings, discussions, workshops, training sessions, and professional engagements.",
        },
        {
            "title": "DISCUSSION ROOMS",
            "url": "core:discussion_rooms",
            "description": "Comfortable spaces for study groups, mentoring sessions, brainstorming meetings, and collaborative work.",
        },
        {
            "title": "EVENT SPACES",
            "url": "core:reserve_room",
            "description": "Versatile venues suitable for conferences, public talks, book launches, exhibitions, and community events.",
        },
    ]
    return render(request, "core/spaces.html", {"spaces": spaces})


def meeting_rooms(request):
    rooms = [
        {
            "title": "Small Meeting Room",
            "capacity": "4–10 Participants",
            "description": "Suitable for interviews, consultations, private meetings, and focused discussions.",
        },
        {
            "title": "Medium Meeting Room",
            "capacity": "10–25 Participants",
            "description": "Designed for workshops, training sessions, collaborative meetings, and professional engagements.",
        },
        {
            "title": "Large Meeting Room",
            "capacity": "25–50 Participants",
            "description": "Ideal for presentations, stakeholder meetings, board sessions, and larger group discussions.",
        },
    ]
    return render(request, "core/meeting_rooms.html", {"rooms": rooms})


def discussion_rooms(request):
    rooms = ["Grey Room", "Blue Room", "Red Room"]
    uses = [
        "Study Groups",
        "Mentoring Sessions",
        "Interviews",
        "Collaborative Work",
        "Brainstorming Meetings",
        "Small Team Discussions",
    ]
    return render(request, "core/discussion_rooms.html", {
        "rooms": rooms,
        "uses": uses,
    })


def reserve_room(request):
    if request.method == "POST":
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            messages.success(
                request,
                f"Thank you, {reservation.name}! Your reservation request for {reservation.space_type} on {reservation.reservation_date} has been received. Our team will contact you shortly."
            )
            return redirect("core:reserve_room")
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = RoomReservationForm()

    return render(request, "core/reserve_room.html", {"form": form})


def membership(request):
    submitted = False
    if request.method == "POST":
        form = MembershipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            messages.success(
                request,
                f"Thank you, {application.first_name}! Your membership application for '{application.get_membership_type_display()}' has been successfully submitted."
            )
            submitted = True
            form = MembershipApplicationForm()
        else:
            messages.error(request, "Please correct the errors in the application form.")
    else:
        form = MembershipApplicationForm()

    membership_options = [
        {"value": "children_annual", "label": "Children Annual (Under 12)", "monthly": "—", "annual": "7,500 RWF"},
        {"value": "student_monthly", "label": "Secondary & Undergraduate Students", "monthly": "1,500 RWF", "annual": "12,000 RWF"},
        {"value": "adult_monthly", "label": "Adults & Postgraduate Students", "monthly": "2,500 RWF", "annual": "20,000 RWF"},
        {"value": "internet_monthly", "label": "Internet Café Only (13+)", "monthly": "10,000 RWF", "annual": "—"},
    ]

    benefits = [
        {
            "title": "Borrow Books",
            "description": "Borrow up to 3 books with annual memberships and up to 2 books with monthly memberships.",
            "icon": "bi-book",
        },
        {
            "title": "Digital Library",
            "description": "Access educational, research, and digital learning resources.",
            "icon": "bi-hdd-network",
        },
        {
            "title": "Unlimited Wi-Fi",
            "description": "Stay connected while studying, reading, or collaborating.",
            "icon": "bi-wifi",
        },
        {
            "title": "Internet Café",
            "description": "Access internet services and online learning opportunities.",
            "icon": "bi-display",
        },
    ]

    return render(request, "core/membership.html", {
        "form": form,
        "submitted": submitted,
        "membership_options": membership_options,
        "benefits": benefits,
    })


def events_view(request):
    events = Event.objects.all()
    if not events.exists():
        events = [
            {
                "title": "Storytime",
                "date_text": "November 14, 9:30–9:50 a.m.",
                "location": "Kid's Zone",
                "description": "Engaging interactive storytelling session for kids and families.",
                "link": "#",
            },
            {
                "title": "Read a loud session",
                "date_text": "November 14, 10:00–10:30 a.m.",
                "location": "Conference Room",
                "description": "Immersive group reading designed to build confidence and vocabulary.",
                "link": "#",
            },
            {
                "title": "Book Club Meeting",
                "date_text": "November 15, 2:00–3:00 p.m.",
                "location": "Meeting Room 1",
                "description": "Monthly book discussion and literary critique with fellow book lovers.",
                "link": "#",
            },
            {
                "title": "Author Talk: Jane Doe",
                "date_text": "November 16, 6:00–7:30 p.m.",
                "location": "Auditorium",
                "description": "Exclusive author conversation, Q&A, and book signing.",
                "link": "#",
            },
            {
                "title": "Jacaranda Cultural Night",
                "date_text": "December 5, 5:00–8:00 p.m.",
                "location": "Rooftop Terrace",
                "description": "Celebration of Rwandan arts, poetry, music, and creative writing.",
                "link": "#",
            },
        ]
    return render(request, "core/events.html", {"events": events})


# Error Handlers (Sections 79.3, 79.4, 79.5)
def custom_404(request, exception=None):
    return render(request, "404.html", status=404)


def custom_403(request, exception=None):
    return render(request, "403.html", status=403)


def custom_500(request):
    return render(request, "500.html", status=500)
