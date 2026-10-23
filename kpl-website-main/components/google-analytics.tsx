"use client";

import Script from "next/script";

export default function GoogleAnalytics() {
  return (
    <>
      {/* GA Script */}
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=G-RWQT3ZM61W`}
        strategy="afterInteractive"
      />

      {/* Consent Mode Default */}
      <Script id="ga-init" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          window.gtag = gtag;

          gtag('js', new Date());

          // Default: analytics denied
          gtag('consent', 'default', {
            analytics_storage: 'denied'
          });

          gtag('config', 'G-RWQT3ZM61W', {
            anonymize_ip: true
          });
        `}
      </Script>
    </>
  );
}
