"use client";

import { useState } from "react";
import axios from "axios";

import { ApiActivity } from "@/components/ApiCardActivity";
import { ApiHotel } from "@/components/ApiCardHotel";
import { DealsSection } from "@/components/DealsSection";
import { Hero } from "@/components/Hero";
import { MapPlaceholder } from "@/components/MapPlaceholder";
import { Navbar } from "@/components/Navbar";
import { PopularLocations } from "@/components/PopularLocations";
import { ResultsSection, type TravelPlan } from "@/components/ResultsSection";
import { SearchFormValues } from "@/components/SearchBox";
import { TourPackages } from "@/components/TourPackages";
import { WinterTrips } from "@/components/WinterTrips";

interface PlanApiResponse {
  hotels: ApiHotel[];
  activities: ApiActivity[];
  summary: string;
}

export default function HomePage() {
  const [plan, setPlan] = useState<TravelPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (values: SearchFormValues) => {
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    if (!backendUrl) {
      setError("Travel service not configured. Please set NEXT_PUBLIC_BACKEND_URL.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post<PlanApiResponse>(
        `${backendUrl}/plan_trip`,
        {
          destination: values.destination,
          budget: values.budget,
        }
      );

      const data = response.data;

      if (!data?.hotels || !data?.activities || !data?.summary) {
        throw new Error("Incomplete response from travel service.");
      }

      setPlan({
        hotels: data.hotels,
        activities: data.activities,
        summary: data.summary,
      });

      window.scrollTo({
        top: window.innerHeight,
        behavior: "smooth",
      });
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Unable to fetch travel plan.";
      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen bg-white text-slate-900">
      <Navbar />
      <main className="flex flex-col">
        <Hero onSearch={handleSearch} loading={loading} error={error} />
        <PopularLocations />
        <DealsSection />
        <WinterTrips />
        <TourPackages />
        <ResultsSection plan={plan} loading={loading} />
        <MapPlaceholder />
      </main>
    </div>
  );
}
