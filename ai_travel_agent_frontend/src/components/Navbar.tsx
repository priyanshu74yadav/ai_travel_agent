"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  { href: "#discover", label: "Discover" },
  { href: "#tips", label: "Tips" },
  { href: "#reviews", label: "Reviews" },
  { href: "#resources", label: "Resources" },
  { href: "#about", label: "About" },
];

export function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setIsScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all",
        isScrolled
          ? "bg-white/95 shadow-md backdrop-blur text-slate-900"
          : "bg-transparent text-white"
      )}
    >
      <nav className="mx-auto flex h-20 max-w-6xl items-center justify-between px-6 lg:px-10">
        <Link
          href="#home"
          className="text-2xl font-semibold uppercase tracking-wide"
        >
          go<span className="text-primary">explore</span>
        </Link>
        <div className="hidden items-center gap-10 text-sm font-medium md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="transition-colors hover:text-primary"
            >
              {link.label}
            </Link>
          ))}
        </div>
        <Button
          variant="default"
          className={cn(
            "px-6 font-semibold transition",
            isScrolled
              ? "bg-primary text-white hover:bg-primary/90"
              : "border border-white/40 bg-white/20 text-white hover:bg-white/30"
          )}
        >
          Login
        </Button>
      </nav>
    </header>
  );
}

