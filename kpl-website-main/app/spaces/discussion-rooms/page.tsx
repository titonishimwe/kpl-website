import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
    title: "Discussion Rooms",
    description:
        "Explore discussion rooms at Kigali Public Library. Ideal for study groups, mentoring sessions, interviews, and collaborative work.",
};

export default function DiscussionRoomsPage() {
    const rooms = ["Grey Room", "Blue Room", "Red Room"];

    const uses = [
        "Study Groups",
        "Mentoring Sessions",
        "Interviews",
        "Collaborative Work",
        "Brainstorming Meetings",
        "Small Team Discussions",
    ];

    return (
        <main className="bg-white text-primary font-light">
            {/* HERO */}
            <section className="py-16 md:py-24 lg:py-32 px-6 border-b border-custom-gray">
                <div className="max-w-5xl mx-auto text-center">
                    <h1 className="text-4xl md:text-5xl lg:text-6xl tracking-tight font-semibold mb-6 md:mb-10">
                        Discussion Rooms
                    </h1>

                    <div className="w-24 md:w-32 h-0.5 bg-secondary mx-auto mb-6 md:mb-10" />

                    <p className="text-lg sm:text-xl md:text-2xl leading-relaxed max-w-3xl mx-auto text-gray-700">
                        Private discussion spaces designed for study groups,
                        mentoring sessions, interviews, and collaborative work.
                    </p>

                    <p className="mt-8 text-accent uppercase tracking-[0.15em] text-sm">
                        Capacity: 4 Participants
                    </p>
                </div>
            </section>
            {/* ROOMS */}
            <section className="py-8 md:py-16 px-6">
                <div className="max-w-7xl mx-auto">
                    <div className="grid md:grid-cols-3 gap-8 md:gap-12">
                        {rooms.map((room) => (
                            <article
                                key={room}
                                className="border border-custom-gray bg-white"
                            >
                                <div className="aspect-4/3 bg-custom-gray flex items-center justify-center">
                                    <span className="text-sm uppercase tracking-[0.25em] text-gray-500 text-center px-4">
                                        {room}
                                    </span>
                                </div>

                                <div className="p-8">
                                    <h3 className="text-xl md:text-2xl font-semibold mb-4">
                                        {room}
                                    </h3>

                                    <div className="w-12 h-0.5 bg-secondary mb-6" />
                                </div>
                            </article>
                        ))}
                    </div>
                </div>
            </section>

            {/* PRICING */}
            <section className="bg-primary text-white py-16 md:py-24 lg:py-32 px-6">
                <div className="max-w-5xl mx-auto text-center">

                    <p className="text-secondary uppercase tracking-[0.2em] text-xs mb-4">
                        RATES
                    </p>

                    <h2 className="text-3xl md:text-5xl font-semibold tracking-tight mb-16">
                        Discussion Room Pricing
                    </h2>

                    <div className="grid md:grid-cols-2 gap-12">

                        <div>
                            <p className="uppercase tracking-[0.2em] text-white/90 text-sm mb-6">
                                Half Day
                            </p>

                            <p className="text-3xl md:text-5xl font-light">
                                5,000
                            </p>

                            <p className="mt-3 text-secondary">
                                RWF
                            </p>
                        </div>

                        <div>
                            <p className="uppercase tracking-[0.2em] text-white/90 text-sm mb-6">
                                Full Day
                            </p>

                            <p className="text-3xl md:text-5xl font-light">
                                10,000
                            </p>

                            <p className="mt-3 text-secondary">
                                RWF
                            </p>
                        </div>

                    </div>

                </div>
            </section>

            {/* IDEAL FOR */}
            <section className="py-16 md:py-24 px-6">
                <div className="max-w-5xl mx-auto text-center">
                    <p className="text-accent uppercase tracking-[0.2em] text-xs mb-4">
                        IDEAL FOR
                    </p>

                    <h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold tracking-tight mb-12">
                        Common Uses
                    </h2>

                    <div className="flex flex-wrap justify-center gap-4">
                        {uses.map((use) => (
                            <div
                                key={use}
                                className="
            px-6 py-3
            border border-custom-gray
            bg-[#F6F8F7]
            text-gray-700
            uppercase
            tracking-wide
            text-sm
          "
                            >
                                {use}
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            <section className=" text-white py-16 px-6">
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