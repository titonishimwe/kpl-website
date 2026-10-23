import Image, { StaticImageData } from "next/image";

interface QuickLinkItemProps {
  href: string;
  icon: StaticImageData | string;
  title: string;
}

export default function QuickActionItem({ href, icon, title }: QuickLinkItemProps) {
  return (
    <a
      href={href}
      className="flex flex-col gap-2.5 justify-between items-center"
    >
      <Image src={icon} alt={title} width={70} height={70} className="w-8 h-8 md:w-16 md:h-16"/>
      <h2 className="text-md md:text-lg lg:text-xl uppercase">{title}</h2>
    </a>
  );
}
