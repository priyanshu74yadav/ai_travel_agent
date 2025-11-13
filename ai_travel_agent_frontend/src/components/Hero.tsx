"use client";

import { useMemo } from "react";

import { SearchBox, type SearchFormValues } from "@/components/SearchBox";

const HERO_IMAGE =
  "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=2000&q=80";

interface HeroProps {
  onSearch: (values: SearchFormValues) => Promise<void> | void;
  loading: boolean;
  error?: string | null;
}

export function Hero({ onSearch, loading, error }: HeroProps) {
  const gradientOverlay = useMemo(
    () =>
      "linear-gradient(180deg, rgba(17, 24, 39, 0.8) 0%, rgba(17, 24, 39, 0.55) 40%, rgba(17, 24, 39, 0.2) 100%)",
    []
  );

  return (
    <section
      id="home"
      className="relative flex min-h-screen items-center justify-center overflow-hidden"
    >
      <div
        className="absolute inset-0 bg-cover bg-center"
        style={{ backgroundImage: `url(${HERO_IMAGE})` }}
      />
      <div
        className="absolute inset-0"
        style={{ background: gradientOverlay }}
        aria-hidden="true"
      />

      <div className="relative z-10 mx-auto flex w-full max-w-4xl flex-col items-center gap-10 px-6 text-center text-white animate-in fade-in slide-in-from-bottom-6 duration-700">
        <div className="space-y-4">
          <span className="inline-flex items-center rounded-full bg-white/10 px-4 py-2 text-sm font-semibold uppercase tracking-wide backdrop-blur">
            Plan smart. Travel better.
          </span>
          <h1 className="text-4xl font-semibold leading-tight md:text-6xl">
            Discover. Explore. Go!
          </h1>
          <p className="text-lg text-white/80 md:text-xl">
            Explore stunning destinations, unique experiences, and plan your
            perfect trip today!
          </p>
        </div>
        <SearchBox onSearch={onSearch} loading={loading} error={error} />
      </div>
    </section>
  );
}

