import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Careers",
  description:
    "Explore career opportunities at Kigali Public Library and join a team dedicated to learning, culture, innovation, and community development.",
};

export default function CareersPage() {
  const principles = [
    {
      title: "Meaningful Work",
      description:
        "Every role contributes to expanding access to knowledge, learning opportunities, and community engagement across Rwanda.",
    },
    {
      title: "Collaborative Culture",
      description:
        "Work alongside professionals who are passionate about education, innovation, culture, and public service.",
    },
    {
      title: "Professional Growth",
      description:
        "Develop your skills through continuous learning, new challenges, and opportunities to make a lasting impact.",
    },
  ];

  const qualities = [
    "Passion for Learning",
    "Service Excellence",
    "Integrity",
    "Collaboration",
    "Innovation",
    "Community Impact",
  ];

  return (
    <main className="bg-white text-primary font-light">
      {/* HERO */}
      <section className="py-16 md:py-24 lg:py-32 px-6 border-b border-custom-gray">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl tracking-tight font-semibold mb-8">
            Careers
          </h1>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-2xl leading-relaxed max-w-4xl mx-auto text-gray-700">
            Join a team committed to expanding access to knowledge,
            learning, culture, and community engagement across Rwanda.
          </p>
        </div>
      </section>

      {/* WHY WORK WITH US */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="mb-16 md:mb-24">
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight text-center">
              Why Work With Us
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-12 md:gap-16">
            {principles.map((item) => (
              <div key={item.title}>
                <div className="w-12 h-0.5 bg-secondary mb-6" />

                <h3 className="text-xl md:text-2xl font-semibold mb-4">
                  {item.title}
                </h3>

                <p className="text-gray-600 leading-relaxed">
                  {item.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CURRENT OPPORTUNITIES */}
      <section className="bg-primary text-white py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-5xl mx-auto text-center">
          <p className="text-secondary uppercase tracking-[0.2em] text-xs mb-4">
            OPPORTUNITIES
          </p>

          <h2 className="text-3xl md:text-5xl font-semibold tracking-tight mb-10">
            Current Vacancies
          </h2>

          <p className="text-lg md:text-xl text-white/80 leading-relaxed max-w-3xl mx-auto">
            There are currently no open positions at Kigali Public Library.
            We encourage interested candidates to check back regularly for
            future opportunities.
          </p>
        </div>
      </section>

      {/* WHAT WE LOOK FOR */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-12 gap-10 md:gap-16">
            <div className="md:col-span-4">
              <p className="text-accent uppercase tracking-[0.2em] text-xs mb-4">
                OUR VALUES
              </p>

              <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
                What We Look For
              </h2>
            </div>

            <div className="md:col-span-8">
              <div className="flex flex-wrap gap-4">
                {qualities.map((quality) => (
                  <div
                    key={quality}
                    className="
                      px-5 py-3
                      border border-custom-gray
                      bg-[#F6F8F7]
                      text-gray-700
                      uppercase
                      tracking-wide
                      text-sm
                    "
                  >
                    {quality}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TALENT POOL */}
      <section className="border-y border-custom-gray py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-12 gap-10 md:gap-16">
          <div className="md:col-span-4">
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
              Stay Connected
            </h2>
          </div>

          <div className="md:col-span-8 text-lg md:text-xl text-gray-700 leading-relaxed">
            Even when there are no current vacancies, we welcome expressions
            of interest from individuals who are passionate about libraries,
            education, learning, culture, and community development.
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-semibold tracking-tight mb-8">
            Interested in Working With Us?
          </h2>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-xl text-gray-700 leading-relaxed mb-10">
            For future opportunities and recruitment inquiries,
            please contact us.
          </p>

          <a
            href="mailto:careers@kpl.rw"
            className="
              inline-flex
              items-center
              bg-primary
              text-white
              px-8
              py-4
              uppercase
              tracking-[0.15em]
              text-sm
              transition-colors
              duration-300
              hover:bg-accent
            "
          >
            recruitment@kplonline.org
          </a>
        </div>
      </section>
    </main>
  );
}