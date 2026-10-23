"use client";

import { useMemo, useState } from "react";
import type { Metadata } from "next";
import * as Dialog from "@radix-ui/react-dialog";
import { X, BookOpen, Wifi, Monitor, Database } from "lucide-react";

// Remove if your route is client-only metadata incompatible
// export const metadata: Metadata = {
//   title: "Get a Library Card",
//   description:
//     "Apply for a Kigali Public Library membership and enjoy access to books, digital resources, internet services, and learning opportunities.",
// };

type MembershipOption = {
  value: string;
  label: string;
  fee: string;
};

const membershipOptions: MembershipOption[] = [
  {
    value: "children_annual",
    label: "Children Annual",
    fee: "7,500 RWF",
  },
  {
    value: "student_monthly",
    label: "Student Monthly",
    fee: "1,500 RWF",
  },
  {
    value: "student_annual",
    label: "Student Annual",
    fee: "12,000 RWF",
  },
  {
    value: "adult_monthly",
    label: "Adult Monthly",
    fee: "2,500 RWF",
  },
  {
    value: "adult_annual",
    label: "Adult Annual",
    fee: "20,000 RWF",
  },
  {
    value: "internet_monthly",
    label: "Internet Café Monthly",
    fee: "10,000 RWF",
  },
];

const benefits = [
  {
    title: "Borrow Books",
    description:
      "Borrow up to 3 books with annual memberships and up to 2 books with monthly memberships.",
    icon: BookOpen,
  },
  {
    title: "Digital Library",
    description:
      "Access educational, research, and digital learning resources.",
    icon: Database,
  },
  {
    title: "Unlimited Wi-Fi",
    description:
      "Stay connected while studying, reading, or collaborating.",
    icon: Wifi,
  },
  {
    title: "Internet Cafe",
    description:
      "Access internet services and online learning opportunities.",
    icon: Monitor,
  },
];

export default function GetLibraryCardPage() {
  const [open, setOpen] = useState(false);

  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const [document, setDocument] = useState<File | null>(null);

  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    dob: "",
    gender: "",

    idPassport: "",

    phone: "",
    altPhone: "",

    email: "",
    altEmail: "",

    village: "",
    sector: "",
    district: "",
    province: "",

    guardianName: "",
    guardianRelationship: "",
    guardianId: "",
    guardianPhone: "",

    membershipType: "",

    paymentMethod: "",

    // Honeypot
    website: "",
  });

  const age = useMemo(() => {
    if (!formData.dob) return null;

    const birthDate = new Date(formData.dob);
    const today = new Date();

    let age = today.getFullYear() - birthDate.getFullYear();

    const monthDifference =
      today.getMonth() - birthDate.getMonth();

    if (
      monthDifference < 0 ||
      (monthDifference === 0 &&
        today.getDate() < birthDate.getDate())
    ) {
      age--;
    }

    return age;
  }, [formData.dob]);

  const isMinor = age !== null && age < 18;

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement |
      HTMLTextAreaElement |
      HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const resetForm = () => {
    setFormData({
      firstName: "",
      lastName: "",
      dob: "",
      gender: "",

      idPassport: "",

      phone: "",
      altPhone: "",

      email: "",
      altEmail: "",

      village: "",
      sector: "",
      district: "",
      province: "",

      guardianName: "",
      guardianRelationship: "",
      guardianId: "",
      guardianPhone: "",

      membershipType: "",

      paymentMethod: "",

      website: "",
    });

    setDocument(null);
  };

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    // Honeypot
    if (formData.website) {
      return;
    }

    try {
      setLoading(true);

      const payload = new FormData();

      Object.entries(formData).forEach(([key, value]) => {
        payload.append(key, value);
      });

      if (document) {
        payload.append("document", document);
      }

      // TODO:
      // await fetch("/api/membership", {
      //   method: "POST",
      //   body: payload,
      // });

      await new Promise((resolve) =>
        setTimeout(resolve, 1500)
      );

      setSubmitted(true);
      resetForm();
    } catch (error) {
      console.error(error);
      alert(
        "An error occurred while submitting your application."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="bg-white text-primary font-light">
      {/* PART 2 STARTS BELOW */}      {/* HERO */}
      <section className="py-16 md:py-24 lg:py-32 px-6 border-b border-custom-gray">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-5xl lg:text-6xl tracking-tight font-semibold mb-8">
            Get a Library Card
          </h1>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-2xl leading-relaxed max-w-4xl mx-auto text-gray-700">
            Become a member of Kigali Public Library and enjoy access to books,
            digital resources, internet services, and learning opportunities.
          </p>
        </div>
      </section>

      {/* MEMBERSHIP CATEGORIES */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-12 gap-10 md:gap-16">
            <div className="md:col-span-4">
              <p className="text-accent uppercase tracking-[0.2em] text-xs mb-4">
                MEMBERSHIP
              </p>

              <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
                Membership Categories
              </h2>
            </div>

            <div className="md:col-span-8 overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-custom-gray">
                    <th className="text-left py-4 font-medium">Category</th>
                    <th className="text-left py-4 font-medium">Monthly</th>
                    <th className="text-left py-4 font-medium">Annual</th>
                  </tr>
                </thead>

                <tbody className="text-gray-700">
                  <tr className="border-b border-custom-gray">
                    <td className="py-5">Children (Under 12 Years)</td>
                    <td>—</td>
                    <td>7,500 RWF</td>
                  </tr>

                  <tr className="border-b border-custom-gray">
                    <td className="py-5">
                      Secondary & Undergraduate Students
                    </td>
                    <td>1,500 RWF</td>
                    <td>12,000 RWF</td>
                  </tr>

                  <tr className="border-b border-custom-gray">
                    <td className="py-5">
                      Adults & Postgraduate Students
                    </td>
                    <td>2,500 RWF</td>
                    <td>20,000 RWF</td>
                  </tr>

                  <tr>
                    <td className="py-5">Internet Café Only (13+)</td>
                    <td>10,000 RWF</td>
                    <td>—</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* BENEFITS */}
      <section className="bg-primary text-white py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-secondary uppercase tracking-[0.2em] text-xs mb-4">
              BENEFITS
            </p>

            <h2 className="text-3xl md:text-5xl font-semibold tracking-tight">
              Membership Benefits
            </h2>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12">
            {benefits.map((benefit) => {
              const Icon = benefit.icon;

              return (
                <div key={benefit.title}>
                  <Icon className="h-10 w-10 text-secondary mb-6" />

                  <h3 className="text-xl font-semibold mb-4">
                    {benefit.title}
                  </h3>

                  <p className="text-white/80 leading-relaxed">
                    {benefit.description}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* MEMBERSHIP RULES */}
      <section className="border-y border-custom-gray py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-6xl mx-auto grid md:grid-cols-12 gap-10 md:gap-16">
          <div className="md:col-span-4">
            <p className="text-accent uppercase tracking-[0.2em] text-xs mb-4">
              BORROWING
            </p>

            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">
              Membership Rules
            </h2>
          </div>

          <div className="md:col-span-8 text-lg text-gray-700 leading-relaxed space-y-6">
            <p>
              Annual members may borrow up to 3 books at a time.
            </p>

            <p>
              Monthly members may borrow up to 2 books at a time.
            </p>

            <p>
              Books are due within 21 days and may be renewed once for an
              additional 7 days.
            </p>

            <p>
              Late returns incur a fee of 300 RWF per book, per day.
            </p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 md:py-24 lg:py-32 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-semibold tracking-tight mb-8">
            Ready to Become a Member?
          </h2>

          <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

          <p className="text-lg md:text-xl text-gray-700 leading-relaxed mb-10">
            Complete a membership application and start enjoying the
            benefits of Kigali Public Library.
          </p>

          <Dialog.Root open={open} onOpenChange={setOpen}>
            <Dialog.Trigger asChild>
              <button
                className="
                  inline-flex
                  items-center
                  bg-primary
                  text-white
                  px-8
                  py-4
                  uppercase
                  tracking-[0.15em]
                  text-sm
                  transition-colors
                  duration-300
                  hover:bg-accent
                "
              >
                Get a Library Card
              </button>
            </Dialog.Trigger>

            <Dialog.Portal>
              <Dialog.Overlay
                className="
                  fixed
                  inset-0
                  bg-black/50
                  z-50
                "
              />

              <Dialog.Content
                className="
                  fixed
                  inset-x-4
                  top-[2%]
                  bottom-[2%]
                  z-50
                  bg-white
                  overflow-y-auto
                  max-w-5xl
                  mx-auto
                  p-8
                  md:p-12
                "
              >
                <div className="flex items-start justify-between mb-12">
                  <div>
                    <Dialog.Title className="text-3xl font-semibold tracking-tight mb-3">
                      Membership Application
                    </Dialog.Title>

                    <p className="text-gray-600">
                      Complete the form below to apply for membership.
                    </p>
                  </div>

                  <Dialog.Close asChild>
                    <button
                      className="
                        p-2
                        hover:bg-gray-100
                        transition-colors
                      "
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </Dialog.Close>
                </div>

                {submitted ? (
                  <div className="text-center py-20">
                    <h3 className="text-3xl font-semibold mb-6">
                      Application Submitted
                    </h3>

                    <div className="w-24 h-0.5 bg-secondary mx-auto mb-8" />

                    <p className="text-gray-600 max-w-xl mx-auto leading-relaxed">
                      Thank you for applying for a Kigali Public Library
                      membership. Our team will review your application
                      and contact you regarding the next steps.
                    </p>
                  </div>
                ) : (
                  <>
                    {/* PART 3 GOES HERE */}                    <form
                      onSubmit={handleSubmit}
                      className="space-y-16"
                    >
                      {/* Honeypot */}
                      <input
                        type="text"
                        name="website"
                        value={formData.website}
                        onChange={handleChange}
                        className="hidden"
                        tabIndex={-1}
                        autoComplete="off"
                      />

                      {/* PERSONAL INFORMATION */}
                      <div>
                        <h3 className="text-xl font-semibold mb-8">
                          Personal Information
                        </h3>

                        <div className="grid md:grid-cols-2 gap-8">
                          <input
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            required
                            placeholder="First Name *"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            required
                            placeholder="Last Name *"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <div>
                            <label className="block text-sm text-gray-500 mb-2">
                              Date of Birth *
                            </label>

                            <input
                              type="date"
                              name="dob"
                              value={formData.dob}
                              onChange={handleChange}
                              required
                              className="w-full border-b border-custom-gray py-4 outline-none bg-transparent"
                            />
                          </div>

                          <select
                            name="gender"
                            value={formData.gender}
                            onChange={handleChange}
                            required
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          >
                            <option value="">
                              Select Gender
                            </option>

                            <option value="male">
                              Male
                            </option>

                            <option value="female">
                              Female
                            </option>
                          </select>

                          <input
                            name="idPassport"
                            value={formData.idPassport}
                            onChange={handleChange}
                            required
                            placeholder="National ID / Passport *"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            required
                            placeholder="Phone Number *"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                            placeholder="Email Address *"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="altPhone"
                            value={formData.altPhone}
                            onChange={handleChange}
                            placeholder="Alternative Phone Number"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="altEmail"
                            value={formData.altEmail}
                            onChange={handleChange}
                            placeholder="Alternative Email Address"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="village"
                            value={formData.village}
                            onChange={handleChange}
                            placeholder="Village"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="sector"
                            value={formData.sector}
                            onChange={handleChange}
                            placeholder="Sector"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="district"
                            value={formData.district}
                            onChange={handleChange}
                            placeholder="District"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />

                          <input
                            name="province"
                            value={formData.province}
                            onChange={handleChange}
                            placeholder="Province"
                            className="border-b border-custom-gray py-4 outline-none bg-transparent"
                          />
                        </div>
                      </div>

                      {/* GUARDIAN INFORMATION */}
                      {isMinor && (
                        <div>
                          <h3 className="text-xl font-semibold mb-8">
                            Parent / Guardian Information
                          </h3>

                          <div className="grid md:grid-cols-2 gap-8">
                            <input
                              name="guardianName"
                              value={formData.guardianName}
                              onChange={handleChange}
                              required
                              placeholder="Parent / Guardian Name *"
                              className="border-b border-custom-gray py-4 outline-none bg-transparent"
                            />

                            <input
                              name="guardianRelationship"
                              value={formData.guardianRelationship}
                              onChange={handleChange}
                              required
                              placeholder="Relationship *"
                              className="border-b border-custom-gray py-4 outline-none bg-transparent"
                            />

                            <input
                              name="guardianId"
                              value={formData.guardianId}
                              onChange={handleChange}
                              required
                              placeholder="Parent / Guardian ID *"
                              className="border-b border-custom-gray py-4 outline-none bg-transparent"
                            />

                            <input
                              name="guardianPhone"
                              value={formData.guardianPhone}
                              onChange={handleChange}
                              required
                              placeholder="Parent / Guardian Phone Number *"
                              className="border-b border-custom-gray py-4 outline-none bg-transparent"
                            />
                          </div>
                        </div>
                      )}

                      {/* MEMBERSHIP */}
                      <div>
                        <h3 className="text-xl font-semibold mb-8">
                          Membership Selection
                        </h3>

                        <select
                          required
                          name="membershipType"
                          value={formData.membershipType}
                          onChange={handleChange}
                          className="w-full border-b border-custom-gray py-4 outline-none bg-transparent"
                        >
                          <option value="">
                            Select Membership Type
                          </option>

                          {membershipOptions.map((option) => (
                            <option
                              key={option.value}
                              value={option.value}
                            >
                              {option.label} — {option.fee}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* PAYMENT */}
                      <div>
                        <h3 className="text-xl font-semibold mb-8">
                          Payment Method
                        </h3>

                        <div className="space-y-4">
                          <label className="flex items-center gap-3">
                            <input
                              type="radio"
                              name="paymentMethod"
                              value="momo"
                              checked={
                                formData.paymentMethod ===
                                "momo"
                              }
                              onChange={handleChange}
                              required
                            />

                            <span>MoMo Pay</span>
                          </label>

                          <label className="flex items-center gap-3">
                            <input
                              type="radio"
                              name="paymentMethod"
                              value="card"
                              checked={
                                formData.paymentMethod ===
                                "card"
                              }
                              onChange={handleChange}
                            />

                            <span>Bank Card</span>
                          </label>
                        </div>

                        <div className="mt-8 border-l-2 border-secondary pl-6">
                          <p className="font-medium">
                            MoMo Pay
                          </p>

                          <p className="text-gray-600 mt-2">
                            *182*8*1*021216#
                          </p>
                        </div>
                      </div>

                      {/* DOCUMENT */}
                      <div>
                        <h3 className="text-xl font-semibold mb-8">
                          Supporting Document
                        </h3>

                        <label
                          htmlFor="document"
                          className="
                            block
                            border
                            border-custom-gray
                            p-8
                            cursor-pointer
                            hover:border-secondary
                            transition-colors
                          "
                        >
                          <span className="block text-gray-700">
                            Upload National ID, Passport, or
                            Student ID
                          </span>

                          <span className="block text-sm text-gray-500 mt-2">
                            PDF, JPG, JPEG or PNG
                          </span>

                          {document && (
                            <span className="block mt-4 text-secondary">
                              {document.name}
                            </span>
                          )}
                        </label>

                        <input
                          id="document"
                          type="file"
                          accept=".pdf,.jpg,.jpeg,.png"
                          className="hidden"
                          onChange={(e) =>
                            setDocument(
                              e.target.files?.[0] || null
                            )
                          }
                        />
                      </div>

                      {/* CONSENT */}
                      <div>
                        <label className="flex items-start gap-4">
                          <input
                            type="checkbox"
                            required
                            className="mt-1"
                          />

                          <span className="text-gray-700 leading-relaxed">
                            I confirm that the information
                            provided is accurate and I agree
                            to abide by Kigali Public Library
                            membership policies and borrowing
                            regulations.
                          </span>
                        </label>
                      </div>

                      <button
                        type="submit"
                        disabled={loading}
                        className="
                          inline-flex
                          items-center
                          bg-primary
                          text-white
                          px-8
                          py-4
                          uppercase
                          tracking-[0.15em]
                          text-sm
                          transition-colors
                          duration-300
                          hover:bg-accent
                          disabled:opacity-50
                        "
                      >
                        {loading
                          ? "Submitting..."
                          : "Submit Application"}
                      </button>
                    </form>

                  </>
                )}
                              </Dialog.Content>
            </Dialog.Portal>
          </Dialog.Root>
        </div>
      </section>
    </main>
  );
}