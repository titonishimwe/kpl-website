import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About",
  description:
    "Learn about Kigali Public Library, our mission, vision, values, and commitment to providing access to knowledge, culture, innovation, and lifelong learning opportunities across Rwanda.",
};
export default function AboutPage() {
  return (
    <div className="bg-white text-gray-900 font-light">

      {/* HERO */}
      <section className="py-16 md:py-24 lg:py-32 px-6 border-b border-gray-200">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl tracking-tight font-semibold mb-6 md:mb-10">
            Kigali Public Library
          </h1>

          <div className="w-24 md:w-32 h-0.5 bg-secondary mx-auto mb-6 md:mb-10" />

          <p className="text-lg sm:text-xl md:text-2xl leading-relaxed max-w-3xl md:max-w-4xl mx-auto text-gray-700">
            A national hub for learning, culture, and innovation
            committed to ensuring fair access to knowledge,
            creativity, and opportunity for all communities.
          </p>

          <p className="mt-6 md:mt-10 text-sm md:text-lg text-gray-500 tracking-wide">
            Kacyiru · Kigali · Rwanda
          </p>
        </div>
      </section>



      {/* WHO WE ARE */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-12 gap-10 md:gap-16">

          <div className="md:col-span-4">
            <h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold tracking-tight">
              Who We Are
            </h2>
          </div>

          <div className="md:col-span-8 space-y-6 md:space-y-8 text-base md:text-lg lg:text-xl leading-relaxed text-gray-700">
            <p>
              Kigali Public Library (KPL) is a public-serving institution that
              oversees and supports more than 100 libraries across Rwanda,
              expanding access to books, digital resources, and learning
              opportunities beyond the city of Kigali.
            </p>

            <p>
              As a custodian of knowledge and culture, KPL convenes readers,
              students, professionals, creatives, and families within an
              inclusive environment designed for discovery, dialogue,
              and personal growth.
            </p>
          </div>

        </div>
      </section>



      {/* VISION & MISSION */}
      <section className="bg-gray-50 py-16 md:py-24 lg:py-32 px-6 border-y border-gray-200">
        <div className="max-w-6xl mx-auto">

          <div className="text-center mb-12 md:mb-20">
            <h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold tracking-tight">
              Vision & Mission
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-10 md:gap-20 text-base md:text-lg lg:text-xl leading-relaxed text-gray-700">

            <div>
              <h3 className="text-xl md:text-2xl font-semibold text-secondary mb-4 md:mb-8 tracking-wide uppercase">
                Vision
              </h3>
              <p>
                To create a world where all communities have access to
                information and learning opportunities that meet their
                creativity, curiosity, and intellectual aspirations.
              </p>
            </div>

            <div>
              <h3 className="text-xl md:text-2xl font-semibold text-secondary mb-4 md:mb-8 tracking-wide uppercase">
                Mission
              </h3>
              <p>
                To provide a dynamic and inclusive national platform
                that fosters lifelong learning, cultural enrichment,
                and community transformation.
              </p>
            </div>

          </div>
        </div>
      </section>



      {/* CORE VALUES */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-7xl mx-auto">

          <div className="text-center mb-16 md:mb-24">
            <h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold tracking-tight">
              Core Values
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-x-10 md:gap-x-16 gap-y-12 md:gap-y-20 text-base md:text-lg leading-relaxed">

            {[
              {
                title: "Inclusion",
                text: "We ensure equal access to knowledge, programs, and opportunities that promote human and social development."
              },
              {
                title: "Quality Services",
                text: "We deliver impactful educational, cultural, and community services that create measurable value."
              },
              {
                title: "Integrity",
                text: "We uphold transparency, accountability, and ethical conduct in all our engagements."
              },
              {
                title: "Adaptability",
                text: "We embrace innovation and technology to remain relevant in an evolving global landscape."
              },
              {
                title: "Collaboration",
                text: "We cultivate partnerships that amplify impact and accelerate transformative change."
              }
            ].map((value, index) => (
              <div key={index}>
                <div className="w-10 md:w-12 h-0.5 bg-secondary mb-4 md:mb-6" />
                <h4 className="text-lg md:text-xl lg:text-2xl font-semibold mb-3 md:mb-4 tracking-tight">
                  {value.title}
                </h4>
                <p className="text-gray-600">
                  {value.text}
                </p>
              </div>
            ))}

          </div>

        </div>
      </section>

    </div>
  );
}
