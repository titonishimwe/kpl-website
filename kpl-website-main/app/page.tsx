import cardIcon from "@/public/images/icons/card.svg"
import digitalIcon from "@/public/images/icons/digital.svg"
import eventIcon from "@/public/images/icons/events.svg"
import roomIcon from "@/public/images/icons/room.svg"
import testImage from "@/public/images/bg/firstlady.jpg"
import richdadPic from "@/public/images/covers/richdad.jpg"
import dreamcountPic from "@/public/images/covers/dreamcount.webp"
import jacarandaPic from "@/public/images/covers/jacaranda.jpg"
import richestmanPic from "@/public/images/covers/richestman.jpeg"
import athousand from "@/public/images/covers/athousand.jpg"
import jacaranda from "@/public/images/events/jacaranda.png"
import NewArrivals from "@/components/layout/new-arrivals";
import LibraryEvents from "@/components/layout/library-events";
import QuickActionsSection from "@/components/layout/quick-actions-section";
import HeroSection from "@/components/layout/hero-section";
import { Metadata } from "next"

export const metadata: Metadata = {
  title: "Welcome to Kigali Public Library",
  description: "Kigali Public Library is an open and public platform that inspires communities to read, learn and discover. We provide access to educational, cultural, and inspirational materials in digital and physical formats. We host and create programs, workshops, and events that foster literacy, creativity, and innovation. ",
};

export default function Home() {
  return (
      <main className="flex flex-col">
        <HeroSection />
        <QuickActionsSection
          links={[
            {
              href: "/membership",
              icon: cardIcon,
              title: "Get a library card",
            },
            {
              href: "https://kplonline.overdrive.com/",
              icon: digitalIcon,
              title: "Digital Library",
            },
            {
              href: "/reserve-room",
              icon: roomIcon,
              title: "Reserve a Room",
            },
            {
              href: "/events",
              icon: eventIcon,
              title: "Events",
            },
          ]}
        />

        <LibraryEvents
          carouselImages={[
            { src: jacaranda, alt: "Jacaranda Event" },
            { src: testImage, alt: "First Lady Event" },
          ]}
          events={[
            {
              title: "Storytime",
              date: "November 14, 9:30–9:50 a.m.",
              location: "Kid's Zone",
              href: "#",
            },
            {
              title: "Read a loud session",
              date: "November 14, 10:00–10:30 a.m.",
              location: "Conference Room",
              href: "#",
            },
            {
              title: "Book Club Meeting",
              date: "November 15, 2:00–3:00 p.m.",
              location: "Meeting Room 1",
              href: "#",
            },
            {
              title: "Author Talk: Jane Doe",
              date: "November 16, 6:00–7:30 p.m.",
              location: "Auditorium",
              href: "#",
            },
          ]}
        />
        <NewArrivals adult={[{ src: athousand, alt: "Book" }, { src: jacarandaPic, alt: "Jacaranda" }, { src: dreamcountPic, alt: "Dream Count" }, { src: richestmanPic, alt: "Richest man in babylon" }, { src: richdadPic, alt: "Rich dad" }]}
          teens={[{ src: athousand, alt: "Book" }, { src: jacarandaPic, alt: "Jacaranda" }, { src: dreamcountPic, alt: "Dream Count" }, { src: richestmanPic, alt: "Richest man in babylon" }, { src: richdadPic, alt: "Rich dad" }]}
          kids={[{ src: athousand, alt: "Book" }, { src: jacarandaPic, alt: "Jacaranda" }, { src: dreamcountPic, alt: "Dream Count" }, { src: richestmanPic, alt: "Richest man in babylon" }, { src: richdadPic, alt: "Rich dad" }]}
        />
      </main>
  );
}
