interface EventCardProps {
  title: string;
  date: string;
  location: string;
  href?: string;
}

export default function EventCard({
  title,
  date,
  location,
  href,
}: EventCardProps) {
  return (
    <div className="flex flex-col space-y-2 md:space-y-3">

      {/* Title */}
      <a
        href={href ?? "#"}
        className="group transition-colors duration-300"
      >
        <h3 className="
          text-lg md:text-xl
          font-semibold
          tracking-tight
          text-gray-900
          group-hover:text-secondary
          transition-colors
        ">
          {title}
        </h3>
      </a>

      {/* Meta */}
      <div className="
        space-y-1
        text-sm md:text-base
        font-normal
        text-gray-700
        leading-relaxed
      ">

        <p>
          <span className="text-xs font-light uppercase tracking-widest text-gray-400 mr-3">
            Date
          </span>
          {date}
        </p>

        <p>
          <span className="text-xs font-light uppercase tracking-widest text-gray-400 mr-3">
            Location
          </span>
          {location}
        </p>

      </div>

    </div>
  );
}
