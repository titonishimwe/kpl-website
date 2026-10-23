"use client";

import { useEffect, useState } from "react";

export default function CookieConsent() {
    const [visible, setVisible] = useState(false);

    useEffect(() => {
        const stored = localStorage.getItem("cookie-consent");

        if (!stored) {
            setVisible(true);
            document.body.style.overflow = "hidden";
        } else if (stored === "accepted" && window.gtag) {
            window.gtag("consent", "update", {
                analytics_storage: "granted",
            });
        } else if (stored === "declined" && window.gtag) {
            window.gtag("consent", "update", {
                analytics_storage: "denied",
            });
        }
    }, []);

    const handleChoice = (choice: "accepted" | "declined") => {
        localStorage.setItem("cookie-consent", choice);

        if (window.gtag) {
            window.gtag("consent", "update", {
                analytics_storage: choice === "accepted" ? "granted" : "denied",
            });
        }

        document.body.style.overflow = "";
        setVisible(false);
    };

    if (!visible) return null;

    return (
        <div className="fixed inset-0 z-[200] bg-black/60 flex items-center justify-center px-6">

            <div className="max-w-xl text-center space-y-6 bg-white p-8 rounded-lg shadow-lg">

                <h2 className="text-2xl md:text-3xl font-semibold tracking-tight text-gray-900">
                    Privacy & Cookies
                </h2>

                <p className="text-base md:text-lg text-gray-700 leading-relaxed">
                    We use Google Analytics to understand how visitors interact with our website and to improve our services. The information collected is anonymized and does not personally identify you. You may accept or decline analytics tracking. Your choice will not affect access to the website.

                </p>

                <div className="flex flex-col sm:flex-row justify-center gap-4 pt-4">

                    <button
                        onClick={() => handleChoice("declined")}
                        className="px-6 py-3 border border-gray-300 rounded-full text-base hover:bg-gray-100 transition"
                    >
                        Decline
                    </button>

                    <button
                        onClick={() => handleChoice("accepted")}
                        className="px-8 py-3 bg-accent text-white rounded-full text-base hover:opacity-90 transition"
                    >
                        Accept
                    </button>

                </div>

            </div>

        </div>
    );
}
