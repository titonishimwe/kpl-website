"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import logo from "@/public/images/logos/logo.png";
import { NAV_ITEMS } from "@/app/constants";
import { getLibraryStatusRW } from "@/lib/utils";
import SegmentBar from "../segmentbar";

export const Header = () => {
  const [open, setOpen] = useState(false);
  const [openSubmenu, setOpenSubmenu] = useState<string | null>(null);
  const [scrolled, setScrolled] = useState(false);

  const { isOpen, status, hours } = getLibraryStatusRW();

  /* Scroll detection */
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 60);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  /* Lock body scroll when drawer open */
  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  return (
    <>
      {/* ================= HEADER ================= */}
      <header className="fixed top-0 left-0 w-full z-50">
        {/* Cinematic Background */}
        <div
          className={`
            absolute inset-0 transition-all duration-500 backdrop-blur-md
            ${
              scrolled
                ? "bg-white/90 shadow-[0_4px_20px_rgba(0,0,0,0.05)]"
                : "bg-white"
            }
          `}
        />

        <div className="relative">
          {/* ================= TOP BAR ================= */}
          <div
            className={`
              max-w-7xl mx-auto flex justify-between items-center px-6
              transition-all duration-500
              ${scrolled ? "py-2" : "py-4"}
            `}
          >
            {/* Logo */}
            <div className="flex flex-col items-center gap-1">
              <Image
                src={logo}
                alt="KPL Logo"
                priority
                className={`transition-all duration-500 ${
                  scrolled ? "w-20" : "w-24"
                }`}
              />

              <p className="font-light tracking-widest text-[11px] text-gray-600">
                READ – LEARN – DISCOVER
              </p>
            </div>

            {/* Desktop Status */}
            <div className="hidden md:flex flex-col items-end text-right">
              <p
                className={`text-sm font-medium tracking-wide ${
                  isOpen ? "text-[#1f7a3e]" : "text-[#8b1e1e]"
                }`}
              >
                {status}
              </p>

              <p className="text-sm text-gray-700">
                <span className="font-medium">Today’s hours:</span> {hours}
              </p>
            </div>

            {/* Hamburger */}
            <button
              onClick={() => setOpen(true)}
              className="md:hidden flex flex-col gap-1"
              aria-label="Open menu"
            >
              <span className="w-6 h-[1.5px] bg-black"></span>
              <span className="w-6 h-[1.5px] bg-black"></span>
              <span className="w-6 h-[1.5px] bg-black"></span>
            </button>
          </div>

          {/* ================= DESKTOP NAV ================= */}
          <nav className="hidden md:block">
            <ul
              className={`
                max-w-7xl mx-auto flex justify-end gap-8 px-6
                font-semibold tracking-wide transition-all duration-500
                ${scrolled ? "text-base py-3" : "text-lg py-4"}
              `}
            >
              {NAV_ITEMS.map((item) => (
                <li key={item.label} className="relative group">
                  {/* Normal Links */}
                  {!item.children && (
                    <a
                      href={item.href}
                      className="transition-colors duration-300 hover:text-[#a15965]"
                    >
                      {item.label}
                    </a>
                  )}

                  {/* Mega Menu Trigger */}
                  {item.children && (
                    <>
                      <span className="cursor-pointer flex items-center gap-1 hover:text-[#a15965]">
                        {item.label} ▾
                      </span>

                      {/* MEGA MENU */}
                      <div className="absolute top-full left-1/2 -translate-x-1/2 w-3xl bg-white/95 shadow-xl hidden group-hover:block">
                        <div className="max-w-7xl mx-auto px-10 py-10 grid grid-cols-3 gap-12 text-black">
                          {item.children.map((section) => (
                            <div key={section.title}>
                              <h3 className="text-xs font-bold tracking-widest text-gray-500 uppercase mb-4">
                                {section.title}
                              </h3>

                              <ul className="space-y-3">
                                {section.items.map((service) => (
                                  <li key={service.label}>
                                    <a
                                      href={service.href}
                                      className="text-lg hover:text-[#a15965] transition-colors"
                                    >
                                      {service.label}
                                    </a>
                                  </li>
                                ))}
                              </ul>
                            </div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}
                </li>
              ))}
            </ul>
          </nav>
        </div>

        {scrolled && <SegmentBar height="h-[2px]" />}
      </header>

      {/* ================= MOBILE DRAWER ================= */}
      <div
        className={`
          fixed inset-0 z-[60] md:hidden
          ${open ? "pointer-events-auto" : "pointer-events-none"}
        `}
      >
        {/* Backdrop */}
        <div
          onClick={() => setOpen(false)}
          className={`
            absolute inset-0 bg-black/30 backdrop-blur-sm
            transition-opacity duration-500
            ${open ? "opacity-100" : "opacity-0"}
          `}
        />

        {/* Drawer */}
        <aside
          className={`
            absolute right-0 top-0 h-full w-3/4 max-w-sm bg-white
            shadow-[0_20px_60px_rgba(0,0,0,0.15)]
            transform transition-transform duration-500
            ease-[cubic-bezier(0.22,1,0.36,1)]
            ${open ? "translate-x-0" : "translate-x-full"}
          `}
        >
          <div className="p-8 flex flex-col gap-10">
            <button
              onClick={() => setOpen(false)}
              className="self-end text-xl font-light"
            >
              ✕
            </button>

            {/* Mobile Status */}
            <div className="border-b border-gray-200 pb-6">
              <p
                className={`text-sm font-medium tracking-wide ${
                  isOpen ? "text-[#1f7a3e]" : "text-[#8b1e1e]"
                }`}
              >
                {status}
              </p>

              <p className="text-sm text-gray-700 mt-1">
                <span className="font-medium">Today’s hours:</span> {hours}
              </p>
            </div>

            {/* Mobile Nav */}
            <ul className="flex flex-col gap-6 text-xl font-semibold tracking-wide">
              {NAV_ITEMS.map((item) => (
                <li key={item.label}>
                  {/* Normal link */}
                  {!item.children && (
                    <a
                      href={item.href}
                      onClick={() => setOpen(false)}
                      className="hover:text-[#a15965]"
                    >
                      {item.label}
                    </a>
                  )}

                  {/* Expandable submenu */}
                  {item.children && (
                    <div className="flex flex-col gap-3">
                      <button
                        onClick={() =>
                          setOpenSubmenu(
                            openSubmenu === item.label ? null : item.label
                          )
                        }
                        className="flex justify-between items-center w-full hover:text-[#a15965]"
                      >
                        {item.label}
                        <span>
                          {openSubmenu === item.label ? "▴" : "▾"}
                        </span>
                      </button>

                      <div
                        className={`flex flex-col gap-3 pl-4 text-lg transition-all duration-300 ${
                          openSubmenu === item.label
                            ? "max-h-96 opacity-100"
                            : "max-h-0 opacity-0 overflow-hidden"
                        }`}
                      >
                        {item.children.map((section) =>
                          section.items.map((service) => (
                            <a
                              key={service.label}
                              href={service.href}
                              onClick={() => setOpen(false)}
                              className="text-gray-700 hover:text-[#a15965]"
                            >
                              {service.label}
                            </a>
                          ))
                        )}
                      </div>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </div>
        </aside>
      </div>
    </>
  );
};