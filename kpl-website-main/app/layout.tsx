import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { Header } from "@/components/layout/header";
import Footer from "@/components/layout/footer";
import GoogleAnalytics from "@/components/google-analytics";
import CookieBanner from "@/components/cookie-banner";


const dinPro = localFont({
  src: [
    {
      path: "../public/fonts/dinpro/dinpro_light.otf",
      weight: "300",
      style: "normal",
    },
    {
      path: "../public/fonts/dinpro/dinpro_lightitalic.ttf",
      weight: "300",
      style: "italic",
    },
    {
      path: "../public/fonts/dinpro/dinpro.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "../public/fonts/dinpro/dinpro_medium.otf",
      weight: "500",
      style: "normal"
    },

    {
      path: "../public/fonts/dinpro/dinpro_mediumitalic.otf",
      weight: "500",
      style: "italic"
    },

    {
      path: "../public/fonts/dinpro/dinpro_italic.otf",
      weight: "400",
      style: "italic",
    },
    {
      path: "../public/fonts/dinpro/dinpro_bold.otf",
      weight: "700",
      style: "normal",
    },
    {
      path: "../public/fonts/dinpro/dinpro_bolditalic.otf",
      weight: "700",
      style: "italic",
    },
    {
      path: "../public/fonts/dinpro/dinpro_condensedregular.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "../public/fonts/dinpro/dinpro_condenseditalic.otf",
      weight: "400",
      style: "italic",
    },
    {
      path: "../public/fonts/dinpro/dinpro_condensedbold.otf",
      weight: "700",
      style: "normal",
    },
    {
      path: "../public/fonts/dinpro/dinpro_condensedbolditalic.otf",
      weight: "700",
      style: "italic",
    },
  ],
  variable: "--font-dinpro",
});


export const metadata: Metadata = {
  title: {
    default: "Kigali Public Library",
    template: "%s | Kigali Public Library",
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${dinPro.variable} antialiased min-h-screen flex flex-col`}
      >
        <Header />
        <main className="flex-1 font-sans pt-27.5">{children}</main>
        <Footer />
        <GoogleAnalytics />
        <CookieBanner />
      </body>

    </html>
  );
}
