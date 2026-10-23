"use client";

import SegmentBar from "@/components/segmentbar";
import XIcon from "@/components/icons/x-icon";
import YoutubeIcon from "@/components/icons/youtube-icon";
import InstagramIcon from "@/components/icons/instagram-icon";
import FacebookIcon from "@/components/icons/facebook-icon";

export default function Footer() {
  return (
    <footer className="w-full mt-7 md:mt-10">
      <SegmentBar />

      {/* Main Footer Content */}
      <div className="w-full max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start py-10 px-6 gap-10 md:gap-6 text-primary">

        {/* Contact Section */}
        <div className="flex flex-col gap-4 md:gap-5">
          <h2 className="text-sm font-medium tracking-widest uppercase">
            Contact
          </h2>

          <div className="flex flex-col gap-3 text-base md:text-base font-normal leading-relaxed text-gray-800">
            <p className="text-lg md:text-xl tracking-tight text-gray-700">
              Kigali Public Library
            </p>

            <a
              href="https://maps.app.goo.gl/ZjdB5MHwKms4dHMC9"
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-block hover:text-black transition-colors"
            >
              KN 8 Avenue, Gasabo<br />
              Kigali, Rwanda

              <span className="block text-sm font-light text-primary mt-1">
                View on Map →
              </span>
            </a>

            <p>
              <span className="font-light uppercase text-gray-400 mr-2">T</span>
              <a href="tel:+250788500777" className="hover:text-black transition-colors">
                +250 788 500 777
              </a>
            </p>

            <p>
              <span className="font-light uppercase text-gray-400 mr-2">E</span>
              <a href="mailto:info@kplonline.org" className="hover:text-black transition-colors">
                info@kplonline.org
              </a>
            </p>
          </div>
        </div>

        {/* Hours Section */}
        <div className="flex flex-col gap-4 md:gap-5">
          <h2 className="text-sm font-medium tracking-widest uppercase">
            Library Hours
          </h2>

          <div className="flex flex-col text-base md:text-base font-normal leading-relaxed gap-3 text-gray-800">
            <p>
              <span className="text-gray-700">
                Monday – Friday
              </span><br />
              8:00 AM – 8:00 PM
            </p>

            <p>
              <span className="text-gray-700">
                Saturday – Sunday
              </span><br />
              8:00 AM – 5:00 PM
            </p>
          </div>
        </div>

        {/* Links Section */}
        <div className="flex flex-col gap-4 md:gap-5">
          <h2 className="text-sm font-medium tracking-widest uppercase">
            Resources
          </h2>

          <div className="flex flex-col text-base md:text-base font-normal gap-3 text-gray-800">
            <a href="https://kplonline.overdrive.com/" className="hover:text-black transition">
              Digital Library
            </a>
            <a href="https://library.kplonline.org/" className="hover:text-black transition">
              Online Catalog
            </a>
            <a href="https://read.nabu.org/" className="hover:text-black transition">
              NABU
            </a>
            <a href="https://www.ekitabu.com/" className="hover:text-black transition">
              Ekitabu
            </a>
          </div>
        </div>

        {/* Social Section */}
        <div className="flex flex-col gap-4 md:gap-5">
          <h2 className="text-sm font-medium tracking-widest uppercase">
            Connect
          </h2>

          <div className="flex justify-start items-center gap-6">
            <XIcon className="fill-black w-5 h-5 lg:w-6 lg:h-6 transition-all duration-300 ease-in-out hover:scale-110 cursor-pointer" />
            <InstagramIcon className="fill-[#FF0069] w-6 h-6 transition-all duration-300 ease-in-out hover:scale-110 cursor-pointer" />
            <FacebookIcon className="fill-[#0866FF] w-6 h-7 transition-all duration-300 ease-in-out hover:scale-110 cursor-pointer" />
            <YoutubeIcon className="fill-red-600 w-6 h-5 transition-all duration-300 ease-in-out hover:scale-110 cursor-pointer" />
          </div>

          <p className="text-base md:text-base font-normal text-gray-600 leading-relaxed max-w-xs">
            Follow Kigali Public Library for updates on programs,
            initiatives, and library services.
          </p>
        </div>

      </div>

      {/* Bottom Bar */}
      <div className="w-full max-w-7xl mx-auto border-t border-gray-200 py-5 px-6 flex justify-start items-center">
        <p className="text-sm md:text-base font-normal text-gray-600 tracking-wide">
          © {new Date().getFullYear()} Kigali Public Library. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
