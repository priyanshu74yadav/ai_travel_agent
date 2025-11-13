import { FaStar } from "react-icons/fa";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Deal {
  id: number;
  name: string;
  image: string;
  rating: number;
  price: string;
  location: string;
}

const DEALS: Deal[] = [
  {
    id: 1,
    name: "Aurora Sky Lodge",
    image:
      "https://images.unsplash.com/photo-1516478177764-9fe5bdc9b9b6?auto=format&fit=crop&w=1200&q=80",
    rating: 4.9,
    price: "$360/night",
    location: "Reykjavík, Iceland",
  },
  {
    id: 2,
    name: "Desert Mirage Resort",
    image:
      "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1200&q=80",
    rating: 4.7,
    price: "$280/night",
    location: "Abu Dhabi, UAE",
  },
  {
    id: 3,
    name: "Rainforest Escape Villa",
    image:
      "https://images.unsplash.com/photo-1528909514045-2fa4ac7a08ba?auto=format&fit=crop&w=1200&q=80",
    rating: 4.8,
    price: "$210/night",
    location: "Ubud, Bali",
  },
  {
    id: 4,
    name: "Cliffside Panorama Suites",
    image:
      "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=1200&q=80",
    rating: 4.6,
    price: "$420/night",
    location: "Santorini, Greece",
  },
];

export function DealsSection() {
  return (
    <section
      id="tips"
      className="mx-auto max-w-6xl space-y-10 px-6 py-20 animate-in fade-in slide-in-from-bottom-6 duration-700"
    >
      <div className="space-y-3 text-center">
        <h2 className="text-3xl font-semibold text-slate-900 md:text-4xl">
          Last minute deals in unique places
        </h2>
        <p className="text-slate-500">
          Exclusive offers handpicked for spontaneous explorers.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {DEALS.map((deal) => (
          <Card
            key={deal.id}
            className="group overflow-hidden rounded-3xl border-0 shadow-xl transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="relative h-48 overflow-hidden">
              <div
                className="absolute inset-0 bg-cover bg-center transition duration-500 group-hover:scale-105"
                style={{ backgroundImage: `url(${deal.image})` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/70 via-slate-900/10 to-transparent" />
              <Badge className="absolute left-4 top-4 rounded-full bg-amber-400 px-4 py-1 text-xs font-semibold text-slate-900 shadow-lg">
                20% off
              </Badge>
            </div>
            <CardHeader>
              <CardTitle className="text-xl">{deal.name}</CardTitle>
              <CardDescription>{deal.location}</CardDescription>
            </CardHeader>
            <CardContent className="flex items-center justify-between">
              <div className="flex items-center gap-1 text-amber-500">
                <FaStar className="h-4 w-4" />
                <span className="text-sm font-semibold text-slate-700">
                  {deal.rating.toFixed(1)}
                </span>
              </div>
              <span className="text-base font-semibold text-primary">
                {deal.price}
              </span>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

