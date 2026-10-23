import EventsCarousel from "./events-carousel";
import EventsList from "./events-list";

export interface CarouselImage {
  src: string | any;
  alt: string;
}

export interface EventItem {
  title: string;
  date: string;
  location: string;
  href?: string;
}

interface LibraryEventsSectionProps {
  carouselImages: CarouselImage[];
  events: EventItem[];
}

export default function LibraryEvents({
  carouselImages,
  events,
}: LibraryEventsSectionProps) {
  return (
    <section className="w-full flex justify-center mx-auto py-12 md:py-16 lg:py-20 px-6">
      <div className="w-full max-w-6xl flex flex-col lg:flex-row justify-between items-start gap-8 md:gap-10 lg:gap-12">

        {/* Left: Carousel */}
        <div className="flex flex-col gap-6 md:gap-8">
          <h2 className="text-2xl md:text-3xl font-semibold tracking-tight text-gray-900">
            What’s Happening at the Library
          </h2>

          <EventsCarousel images={carouselImages} />
        </div>

        {/* Right: Events */}
        <div className="flex flex-col gap-6 md:gap-8">
          <h2 className="text-2xl md:text-3xl font-semibold tracking-tight text-gray-900">
            Upcoming Events
          </h2>

          <EventsList events={events} />
        </div>

      </div>
    </section>
  );
}
