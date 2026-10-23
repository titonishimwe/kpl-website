export default function PrivacyPage() {
  return (
    <div className="bg-white text-gray-900 font-light">

      <section className="py-36 px-6 border-b border-gray-200">
        <div className="max-w-6xl mx-auto text-center">

          <h1 className="text-6xl md:text-7xl tracking-tight font-semibold mb-10">
            Privacy Policy
          </h1>

          <div className="w-32 h-0.5 bg-secondary mx-auto mb-10" />

          <p className="text-2xl md:text-3xl leading-relaxed max-w-4xl mx-auto text-gray-700">
            Kigali Public Library is committed to protecting your privacy and ensuring transparency in how we collect and use information.
          </p>

          <p className="mt-10 text-lg text-gray-500 tracking-wide">
            Last updated: February 3, 2026
          </p>

        </div>
      </section>

      <section className="py-36 px-6">
        <div className="max-w-6xl mx-auto space-y-32">

          {/* Section */}
          <div className="grid md:grid-cols-12 gap-16">
            <div className="md:col-span-4">
              <h2 className="text-4xl font-semibold tracking-tight">
                Information We Collect
              </h2>
            </div>

            <div className="md:col-span-8 space-y-8 text-xl leading-relaxed text-gray-700">
              <p>
                While using our Service, we may ask you to provide certain
                personally identifiable information, including but not limited to:
              </p>

              <ul className="list-disc pl-6 space-y-4">
                <li>Email address</li>
                <li>First and last name</li>
                <li>Phone number</li>
                <li>Address information</li>
                <li>Usage Data</li>
              </ul>

              <p>
                Usage Data may include IP address, browser type, device
                information, pages visited, time spent on pages, and other
                diagnostic data.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-12 gap-16">
            <div className="md:col-span-4">
              <h2 className="text-4xl font-semibold tracking-tight">
                Cookies & Tracking
              </h2>
            </div>

            <div className="md:col-span-8 space-y-8 text-xl leading-relaxed text-gray-700">
              <p>
                We use cookies and similar technologies to enhance functionality
                and analyze website usage.
              </p>

              <ul className="list-disc pl-6 space-y-4">
                <li><strong>Essential Cookies</strong> — required for basic functionality.</li>
                <li><strong>Analytics Cookies</strong> — used in anonymized form to understand website performance.</li>
                <li><strong>Functionality Cookies</strong> — remember your preferences.</li>
              </ul>

              <p>
                You may accept or decline analytics tracking through our consent system.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-12 gap-16">
            <div className="md:col-span-4">
              <h2 className="text-4xl font-semibold tracking-tight">
                Use of Data
              </h2>
            </div>

            <div className="md:col-span-8 space-y-8 text-xl leading-relaxed text-gray-700">
              <p>
                Personal Data may be used to:
              </p>

              <ul className="list-disc pl-6 space-y-4">
                <li>Provide and maintain our Service</li>
                <li>Manage user accounts</li>
                <li>Respond to inquiries</li>
                <li>Improve functionality and security</li>
                <li>Comply with legal obligations</li>
              </ul>
            </div>
          </div>


          <div className="grid md:grid-cols-12 gap-16">
            <div className="md:col-span-4">
              <h2 className="text-4xl font-semibold tracking-tight">
                Data Security & Retention
              </h2>
            </div>

            <div className="md:col-span-8 space-y-8 text-xl leading-relaxed text-gray-700">
              <p>
                We retain Personal Data only as long as necessary and implement
                reasonable measures to protect your information. However, no
                transmission method is completely secure.
              </p>
            </div>
          </div>

          <div className="grid md:grid-cols-12 gap-16 border-t border-gray-200 pt-24">
            <div className="md:col-span-4">
              <h2 className="text-4xl font-semibold tracking-tight">
                Contact Us
              </h2>
            </div>

            <div className="md:col-span-8 space-y-8 text-xl leading-relaxed text-gray-700">
              <p>
                If you have questions regarding this Privacy Policy, please contact:
              </p>

              <p className="text-gray-900">
                Kigali Public Library<br />
                info@kplonline.org<br />
                +250 788 500 777
              </p>
            </div>
          </div>

        </div>
      </section>

    </div>
  );
}
