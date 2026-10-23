import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Get a Library Card",
  description:
    "Apply for a Kigali Public Library membership and enjoy access to books, digital resources, internet services, and learning opportunities.",
};

export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}