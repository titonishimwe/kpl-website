"use client";

import Image from "next/image";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";

interface Item {
  src: any;
  alt: string;
}

interface AutoFitCarouselProps {
  items: Item[];
  imageWidth?: number;
  imageHeight?: number;
  gap?: number;
}

export default function AutoFitCarousel({
  items,
  imageWidth = 127,
  imageHeight = 185,
  gap = 4, 
}: AutoFitCarouselProps) {
  return (
    <div className="w-full max-w-5xl px-4 relative">
      <Carousel className="w-full" opts={{ align: "center" }}>
        <CarouselContent className={`flex gap-${gap}`}>
          {items.map((it, idx) => (
            <CarouselItem
              key={idx}
              className="
                grow-0 shrink-0 px-2
                basis-1/2 sm:basis-1/3 md:basis-1/4
              "
            >
              <div className="flex justify-center">
                <Image
                  src={it.src}
                  alt={it.alt}
                  width={imageWidth}
                  height={imageHeight}
                  className="rounded-md object-contain"
                />
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>

        {/* INSIDE CENTERED ARROWS */}
        <CarouselPrevious
          className="
            absolute left-0 top-1/2 -translate-y-1/2
            hover:text-white p-2  z-10
          transition
          "
          aria-label="Previous"
        />
        <CarouselNext
          className="
            absolute right-0 top-1/2 -translate-y-1/2
          hover:text-white p-2 z-10
         transition
          "
          aria-label="Next"
        />
      </Carousel>
    </div>
  );
}
