import Image from "next/image";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselPrevious,
    CarouselNext,
} from "@/components/ui/carousel";
import { CarouselImage } from "./library-events";

interface EventsCarouselProps {
    images: CarouselImage[];
}

export default function EventsCarousel({ images }: EventsCarouselProps) {
    return (
        <Carousel className="w-full" opts={{
            align: "center",
        }}>
            {/* Limit the content width so arrows don't shrink centering */}
            <CarouselContent className="relative max-w-[730px] max-h-[350px] md:h-[400px]">
                {images.map((img, index) => (
                    <CarouselItem key={index}>
                        <Image
                            src={img.src}
                            alt={img.alt}
                            width={730}
                            height={400}
                            className="w-full h-full object-contain rounded"
                        />
                    </CarouselItem>
                ))}
            </CarouselContent>

            {/* Arrows positioned OUTSIDE the content width */}
            <CarouselPrevious className="left-0 top-1/2 -translate-y-1/2 p-2 bg-accent text-white hover:text-white rounded-full" />
            <CarouselNext className="absolute right-0 top-1/2 -translate-y-1/2 p-2 bg-accent text-white rounded-full" />
        </Carousel>

    );
}
