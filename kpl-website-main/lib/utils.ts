import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

import { CLOSED_DATES, LIBRARY_SCHEDULE } from "@/app/constants";


export const getLibraryStatusRW = () => {
  const now = new Date();

  const formatter = new Intl.DateTimeFormat("en-RW", {
    timeZone: "Africa/Kigali",
    hour: "numeric",
    hour12: false,
    weekday: "long",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });

  const parts = formatter.formatToParts(now);

  const hour = Number(parts.find(p => p.type === "hour")?.value);
  const weekday = parts.find(p => p.type === "weekday")?.value;

  const dateString = `${parts.find(p => p.type === "year")?.value}-${
    parts.find(p => p.type === "month")?.value
  }-${parts.find(p => p.type === "day")?.value}`;

  // Check closed dates
  if (CLOSED_DATES.includes(dateString)) {
    return {
      isOpen: false,
      status: "Closed today",
      hours: "Closed",
    };
  }

  const isWeekend = weekday === "Saturday" || weekday === "Sunday";
  const schedule = isWeekend
    ? LIBRARY_SCHEDULE.weekend
    : LIBRARY_SCHEDULE.weekday;

  const isOpen = hour >= schedule.open && hour < schedule.close;

  return {
    isOpen,
    status: isOpen ? "We are currently open." : "We are currently closed.",
    hours: schedule.label,
  };
};
