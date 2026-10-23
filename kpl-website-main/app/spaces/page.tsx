import Link from "next/link";

export default function MeetingSpacesPage() {
  const spaces = [
    {
      title: "MEETING ROOMS",
      href: "/spaces/meeting-rooms",
      description:
        "Flexible spaces designed for meetings, discussions, workshops, training sessions, and professional engagements.",
    },
    {
      title: "DISCUSSION ROOMS",
      href: "/spaces/discussion-rooms",
      description:
        "Comfortable spaces for study groups, mentoring sessions, brainstorming meetings, and collaborative work.",
    },
    {
      title: "EVENT SPACES",
      href: "/spaces/event-spaces",
      description:
        "Versatile venues suitable for conferences, public talks, book launches, exhibitions, and community events.",
    },
  ];

  return (
    <main className="bg-white text-primary font-light">
      {/* HERO */}
      <section className="py-16 md:py-24 lg:py-32 px-6 border-b border-custom-gray">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl tracking-tight font-semibold mb-6 md:mb-10">
            Meeting & Event Spaces
          </h1>

          <div className="w-24 md:w-32 h-0.5 bg-secondary mx-auto mb-6 md:mb-10" />

          <p className="text-lg sm:text-xl md:text-2xl leading-relaxed max-w-4xl mx-auto text-gray-700">
            Flexible spaces designed for meetings, discussions,
            workshops, training sessions, conferences, and community
            events.
          </p>
        </div>
      </section>

      {/* SPACE CATEGORIES */}
      <section className="py-16 md:py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8 md:gap-12">
            {spaces.map((space) => (
              <Link
                key={space.title}
                href={space.href}
                className="
                  group
                  block
                  border
                  border-custom-gray
                  bg-white
                  transition-all
                  duration-300
                  hover:border-accent
                  hover:-translate-y-1
                "
              >
                {/* Placeholder Image */}
                <div className="aspect-[4/3] bg-custom-gray flex items-center justify-center">
                  <span
                    className="
                      text-sm
                      uppercase
                      tracking-[0.25em]
                      text-gray-500
                      text-center
                      px-4
                      transition-colors
                      duration-300
                      group-hover:text-accent
                    "
                  >
                    {space.title}
                  </span>
                </div>

                {/* Content */}
                <div className="p-8">
                  <h2 className="text-xl md:text-2xl font-semibold mb-4">
                    {space.title}
                  </h2>

                  <div className="w-12 h-0.5 bg-secondary mb-6 transition-all duration-300 group-hover:w-20" />

                  <p className="text-gray-600 leading-relaxed mb-8">
                    {space.description}
                  </p>

                  <span className="inline-flex items-center gap-2 text-accent uppercase tracking-[0.15em] text-sm font-medium">
                    Explore

                    <span className="transition-transform duration-300 group-hover:translate-x-1">
                      →
                    </span>
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* IMPORTANT INFORMATION */}
      <section className="bg-[#F6F8F7] py-16 md:py-20 px-6 border-y border-custom-gray">
        <div className="max-w-4xl mx-auto">
          <p className="text-accent uppercase tracking-[0.2em] text-xs mb-4">
            IMPORTANT INFORMATION
          </p>

          <div className="space-y-4 text-gray-700 leading-relaxed">
            <p>
              Room reservations are subject to availability.
            </p>

            <p>
              Additional conditions may apply depending on the type of
              space requested and the nature of the activity.
            </p>

            <p>
              Please contact the library for further information regarding
              room availability and reservations.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-2xl md:text-4xl lg:text-5xl font-semibold tracking-tight mb-8">
            Reserve a Space
          </h2>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-xl text-gray-700 leading-relaxed mb-10">
            Whether you need a meeting room, a discussion room,
            or an event venue, our spaces are available to support
            your next activity.
          </p>

          <Link
            href="/reserve-room"
            className="
              inline-flex
              items-center
              bg-primary
              text-white
              px-8
              py-4
              uppercase
              tracking-wide
              text-sm
              transition-colors
              duration-300
              hover:bg-accent
            "
          >
            Reserve a Room
          </Link>
        </div>
      </section>
    </main>
  );
}