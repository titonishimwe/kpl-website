/**
 * Kigali Public Library (KPL) - Main JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Scroll effect for header
  const header = document.querySelector(".kpl-header");
  const scrollSegmentBar = document.querySelector(".header-scroll-bar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 40) {
      if (header) header.classList.add("scrolled");
      if (scrollSegmentBar) scrollSegmentBar.classList.remove("d-none");
    } else {
      if (header) header.classList.remove("scrolled");
      if (scrollSegmentBar) scrollSegmentBar.classList.add("d-none");
    }
  });

  // 2. Catalog Search Handler
  const catalogForm = document.getElementById("catalogSearchForm");
  const catalogInput = document.getElementById("catalogSearchInput");
  const KOHA_SEARCH_URL = "https://library.kplonline.org/cgi-bin/koha/opac-search.pl";

  if (catalogForm && catalogInput) {
    catalogForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const rawQuery = catalogInput.value;
      const sanitized = rawQuery
        .trim()
        .replace(/\s+/g, " ")
        .replace(/[^\w\s\-']/g, "")
        .slice(0, 50);

      if (sanitized) {
        const url = `${KOHA_SEARCH_URL}?q=${encodeURIComponent(sanitized)}`;
        window.open(url, "_blank");
      }
    });
  }

  // 3. Cookie Consent Banner
  const cookieBanner = document.getElementById("cookieConsentBanner");
  const acceptBtn = document.getElementById("acceptCookiesBtn");
  const declineBtn = document.getElementById("declineCookiesBtn");

  if (cookieBanner) {
    const consent = localStorage.getItem("kpl-cookie-consent");
    if (!consent) {
      cookieBanner.style.display = "flex";
      document.body.style.overflow = "hidden";
    }

    if (acceptBtn) {
      acceptBtn.addEventListener("click", function () {
        localStorage.setItem("kpl-cookie-consent", "accepted");
        cookieBanner.style.display = "none";
        document.body.style.overflow = "";
      });
    }

    if (declineBtn) {
      declineBtn.addEventListener("click", function () {
        localStorage.setItem("kpl-cookie-consent", "declined");
        cookieBanner.style.display = "none";
        document.body.style.overflow = "";
      });
    }
  }

  // 4. Membership Form Age Detection (Parent / Guardian fields toggle)
  const dobInput = document.querySelector("input[name='dob']");
  const guardianSection = document.getElementById("guardianSection");

  if (dobInput && guardianSection) {
    function calculateAge(birthday) {
      const birthDate = new Date(birthday);
      const today = new Date();
      let age = today.getFullYear() - birthDate.getFullYear();
      const m = today.getMonth() - birthDate.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }
      return age;
    }

    function checkAge() {
      if (!dobInput.value) {
        guardianSection.style.display = "none";
        return;
      }
      const age = calculateAge(dobInput.value);
      if (age < 18) {
        guardianSection.style.display = "block";
      } else {
        guardianSection.style.display = "none";
      }
    }

    dobInput.addEventListener("change", checkAge);
    dobInput.addEventListener("input", checkAge);
    checkAge(); // Initial check on load
  }
});
