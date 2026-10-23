import QuickActionItem from "./quick-action";
import { StaticImageData } from "next/image";

interface QuickLink {
  href: string;
  icon: StaticImageData | string;
  title: string;
}

interface QuickActionsSectionProps {
  links: QuickLink[];
}

export default function QuickActionsSection({ links }: QuickActionsSectionProps) {
  return (
    <section className="w-full flex justify-center items-center mx-auto py-6 md:py-10 px-4 border-b">
      <div className="w-full max-w-7xl md:flex justify-between items-center grid grid-cols-2 grid-rows-2 gap-7">
        {links.map((item, idx) => (
          <QuickActionItem
            key={idx}
            href={item.href}
            icon={item.icon}
            title={item.title}
          />
        ))}
      </div>
    </section>
  );
}
