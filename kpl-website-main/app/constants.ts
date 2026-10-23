export const NAV_ITEMS = [
  { label: "HOME", href: "/" },
  { label: "ABOUT", href: "/about" },

  {
    label: "SERVICES",
    children: [
      {
        title: "Reserve spaces",
        items: [
          { label: "Meeting & Events Spaces", href: "/spaces" },
        ]
      },
      {
        title: "Use library resources",
        items: [
          { label: "Get a library card", href: "/membership" },
          { label: "Digital library", href: "https://kplonline.overdrive.com/" }
        ]
      },
      {
        title: "Popular events",
        items: [
          { label: "Event Space", href: "/event-space" }
        ]
      }
    ]
  },

  { label: "WRITING COMPETITION", href: "https://wc.kplonline.org" },
  { label: "CAREERS", href: "/careers" }
];

export const LIBRARY_SCHEDULE = {
  weekday: {
    open: 8,
    close: 20,
    label: "8:00 AM – 8:00 PM",
  },
  weekend: {
    open: 8,
    close: 17,
    label: "8:00 AM – 5:00 PM",
  },
};

/**
 * Closed days (YYYY-MM-DD) — easy to update
 * Examples: public holidays, maintenance days, events
 */
export const CLOSED_DATES = ["2025-01-01", "2025-07-04"];
