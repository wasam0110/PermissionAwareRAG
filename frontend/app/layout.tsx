import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Permission-Aware RAG",
  description: "Secure multi-tenant retrieval-augmented generation",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
