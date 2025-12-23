import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "@/lib/providers";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

export const metadata: Metadata = {
  title: {
    default: "NexusCore - Singapore SaaS Platform",
    template: "%s | NexusCore",
  },
  description: "Enterprise-grade SaaS platform built for Singapore businesses. GST compliant, PDPA ready.",
  keywords: ["SaaS", "Singapore", "GST", "PDPA", "Enterprise", "Business Software"],
  authors: [{ name: "NexusCore Team" }],
  openGraph: {
    title: "NexusCore - Singapore SaaS Platform",
    description: "Enterprise-grade SaaS platform built for Singapore businesses.",
    url: "https://nexuscore.sg",
    siteName: "NexusCore",
    locale: "en_SG",
    type: "website",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}


