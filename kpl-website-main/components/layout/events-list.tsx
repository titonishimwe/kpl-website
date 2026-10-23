import { Button } from "@/components/ui/button";
import EventCard from "./event-card";
import { EventItem } from "./library-events";

interface EventsListProps {
  events: EventItem[];
}

export default function EventsList({ events }: EventsListProps) {
  return (
    <div className="flex flex-col gap-4 md:gap-6">

      {/* Events */}
      <div className="flex flex-col divide-y divide-gray-200">

        {events.map((event, index) => (
          <div key={index} className="py-3 md:py-4 first:pt-0 last:pb-0">
            <EventCard
              title={event.title}
              date={event.date}
              location={event.location}
              href={event.href}
            />
          </div>
        ))}

      </div>

      {/* CTA */}
      <div>
        <Button
          className="
            rounded-full
            px-6 md:px-7
            py-3 md:py-4
            text-sm md:text-base
            font-semibold tracking-wide
            transition-all duration-300
            hover:bg-accent
          "
        >
          View All Events
        </Button>
      </div>

    </div>
  );
}
