import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Meeting Rooms",
  description:
    "Explore meeting rooms available at Kigali Public Library.",
};

export default function MeetingRoomsPage() {
  const rooms = [
    {
      title: "Small Meeting Room",
      capacity: "4–10 Participants",
      description:
        "Suitable for interviews, consultations, private meetings, and focused discussions.",
    },
    {
      title: "Medium Meeting Room",
      capacity: "10–25 Participants",
      description:
        "Designed for workshops, training sessions, collaborative meetings, and professional engagements.",
    },
    {
      title: "Large Meeting Room",
      capacity: "25–50 Participants",
      description:
        "Ideal for presentations, stakeholder meetings, board sessions, and larger group discussions.",
    },
  ];

  return (
    <main className="bg-white text-primary font-light">
      {/* HERO */}
      <section className="py-16 md:py-24 px-6 border-b border-custom-gray">
        <div className="max-w-5xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-semibold tracking-tight mb-8">
            Meeting Rooms
          </h1>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-2xl text-gray-700 leading-relaxed">
            Professional meeting spaces designed for collaboration,
            planning, presentations, and productive discussions.
          </p>
        </div>
      </section>

      {/* ROOMS */}
      <section className="py-16 md:py-24 px-6">
        <div className="max-w-7xl mx-auto grid md:grid-cols-3 gap-10">
          {rooms.map((room) => (
            <article key={room.title}>
              <div className="aspect-[4/3] bg-custom-gray border border-custom-gray mb-6" />

              <h2 className="text-2xl font-semibold mb-2">
                {room.title}
              </h2>

              <p className="text-accent uppercase tracking-wide text-sm mb-4">
                {room.capacity}
              </p>

              <p className="text-gray-600 leading-relaxed">
                {room.description}
              </p>
            </article>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 border-t border-custom-gray">
        <div className="max-w-4xl mx-auto text-center">
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