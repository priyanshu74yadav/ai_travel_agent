"use client";

import { useState } from "react";
import { HiOutlineLocationMarker } from "react-icons/hi";
import { LuCalendar, LuUsers } from "react-icons/lu";
import { PiCurrencyDollarSimpleBold } from "react-icons/pi";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

export interface SearchFormValues {
  destination: string;
  budget: number;
  checkIn: string;
  checkOut: string;
  travelers: number;
  tab: string;
}

interface SearchBoxProps {
  onSearch: (payload: SearchFormValues) => Promise<void> | void;
  loading: boolean;
  error?: string | null;
}

const TABS = [
  { id: "stays", label: "Stays" },
  { id: "flight", label: "Flight" },
  { id: "hotel", label: "Hotel" },
  { id: "restaurant", label: "Restaurant" },
];

export function SearchBox({ onSearch, loading, error }: SearchBoxProps) {
  const [formValues, setFormValues] = useState<SearchFormValues>({
    destination: "",
    budget: 2500,
    checkIn: "",
    checkOut: "",
    travelers: 2,
    tab: "stays",
  });

  const handleChange = (field: keyof SearchFormValues, value: string) => {
    setFormValues((prev) => ({
      ...prev,
      [field]:
        field === "budget" || field === "travelers"
          ? Number(value)
          : value,
    }));
  };

  const handleSearch = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formValues.destination) {
      return;
    }
    await onSearch(formValues);
  };

  return (
    <Card className="w-full rounded-3xl border-0 bg-white/95 p-2 shadow-2xl backdrop-blur">
      <CardHeader className="pb-4 text-left">
        <CardTitle className="text-xl">Plan your dream escape</CardTitle>
        <CardDescription>
          Select your travel preference and let us craft the itinerary.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <Tabs
          defaultValue="stays"
          onValueChange={(value) =>
            setFormValues((prev) => ({ ...prev, tab: value }))
          }
        >
          <TabsList className="grid grid-cols-2 rounded-full bg-slate-100 p-1 md:grid-cols-4">
            {TABS.map((tab) => (
              <TabsTrigger
                key={tab.id}
                value={tab.id}
                className="rounded-full data-[state=active]:bg-white data-[state=active]:shadow-md"
              >
                {tab.label}
              </TabsTrigger>
            ))}
          </TabsList>
          {TABS.map((tab) => (
            <TabsContent key={tab.id} value={tab.id} className="mt-6">
              <form
                className="grid gap-4 md:grid-cols-2 lg:grid-cols-4"
                onSubmit={handleSearch}
              >
                <SearchInput
                  label="Destination"
                  icon={<HiOutlineLocationMarker className="h-5 w-5 text-primary" />}
                  placeholder="Where to?"
                  value={formValues.destination}
                  onChange={(value) => handleChange("destination", value)}
                />
                <SearchInput
                  label="Check-in"
                  icon={<LuCalendar className="h-5 w-5 text-primary" />}
                  type="date"
                  value={formValues.checkIn}
                  onChange={(value) => handleChange("checkIn", value)}
                />
                <SearchInput
                  label="Check-out"
                  icon={<LuCalendar className="h-5 w-5 text-primary" />}
                  type="date"
                  value={formValues.checkOut}
                  onChange={(value) => handleChange("checkOut", value)}
                />
                <SearchInput
                  label="Travelers"
                  icon={<LuUsers className="h-5 w-5 text-primary" />}
                  type="number"
                  min={1}
                  value={formValues.travelers.toString()}
                  onChange={(value) => handleChange("travelers", value)}
                />
                <SearchInput
                  label="Budget (USD)"
                  icon={<PiCurrencyDollarSimpleBold className="h-5 w-5 text-primary" />}
                  type="number"
                  min={0}
                  value={formValues.budget.toString()}
                  onChange={(value) => handleChange("budget", value)}
                />
                <div className="md:col-span-2 lg:col-span-4 flex flex-wrap items-center justify-between gap-4">
                  {error ? (
                    <p className="text-sm text-red-500">{error}</p>
                  ) : (
                    <p className="text-sm text-slate-500">
                      Tip: Booking early unlocks exclusive bundle discounts.
                    </p>
                  )}
                  <Button
                    type="submit"
                    className="rounded-full px-8 py-6 text-base font-semibold shadow-lg"
                    disabled={loading}
                  >
                    {loading ? "Searching..." : "Search"}
                  </Button>
                </div>
              </form>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}

interface SearchInputProps {
  label: string;
  icon: React.ReactNode;
  type?: string;
  placeholder?: string;
  value: string;
  min?: number;
  onChange: (value: string) => void;
}

function SearchInput({
  label,
  icon,
  type = "text",
  placeholder,
  value,
  min,
  onChange,
}: SearchInputProps) {
  return (
    <label className="group flex flex-col gap-2 text-left">
      <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {label}
      </span>
      <div className="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm transition hover:border-primary hover:shadow-md">
        <span className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
          {icon}
        </span>
        <Input
          type={type}
          min={min}
          value={value}
          placeholder={placeholder}
          className={cn(
            "border-0 bg-transparent px-0 text-base font-medium text-slate-800 placeholder:text-slate-400 focus-visible:ring-0 focus-visible:ring-offset-0",
            type === "date" && !value && "text-slate-400"
          )}
          onChange={(event) => onChange(event.target.value)}
        />
      </div>
    </label>
  );
}

