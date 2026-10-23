"use client";

import Image from "next/image";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselPrevious,
    CarouselNext,
} from "@/components/ui/carousel";
import AutoFitCarousel from "@/components/layout/auto-fit-carousel";

interface BookItem {
    src: any;
    alt: string;
}

interface NewArrivalsProps {
    adult?: BookItem[];
    teens?: BookItem[];
    kids?: BookItem[];
}

export default function NewArrivals({ adult = [], teens = [], kids = [] }: NewArrivalsProps) {
    // Build an array of tabs that actually have books
    const tabs = [
        { id: "adult", label: "Adult", data: adult },
        { id: "teens", label: "Teens", data: teens },
        { id: "kids", label: "Kids", data: kids },
    ].filter((t) => t.data.length > 0);

    // Don't render section if all are empty
    if (tabs.length === 0) return null;

    return (
        <section className="w-full flex justify-center items-center mx-auto py-10">
            <Tabs defaultValue={tabs[0].id} className="w-full">

                {/* Header */}
                <TabsList className="w-full flex justify-center gap-3 mb-8 bg-foreground rounded-none h-24">
                    <div className="w-full max-w-7xl flex flex-col md:flex-row justify-between items-start px-4 gap-2">

                        <h2 className="text-background font-bold text-3xl md:text-4xl lg:text-5xl uppercase">
                            New Arrivals
                        </h2>

                        <div className="flex justify-end items-center gap-7">
                            {tabs.map((tab) => (
                                <TabsTrigger
                                    key={tab.id}
                                    value={tab.id}
                                    className="flex-none data-[state=active]:bg-secondary data-[state=active]:text-background 
                  bg-white text-black border border-black rounded-xl py-2 px-5
                  hover:bg-accent hover:text-background transition uppercase w-fit"
                                >
                                    {tab.label}
                                </TabsTrigger>
                            ))}
                        </div>

                    </div>
                </TabsList>

                {/* Content */}
                <div className="flex justify-center items-center w-full max-w-7xl mx-auto">
                    {tabs.map((tab) => (
                        <TabsContent key={tab.id} value={tab.id} className="w-full flex justify-center">
                            <AutoFitCarousel items={tab.data} />
                        </TabsContent>
                    ))}
                </div>

            </Tabs>
        </section>
    );
}
