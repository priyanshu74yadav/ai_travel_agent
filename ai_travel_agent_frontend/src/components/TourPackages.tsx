import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface TourPackage {
  id: number;
  title: string;
  image: string;
  duration: string;
  priceRange: string;
  description: string;
}

const TOUR_PACKAGES: TourPackage[] = [
  {
    id: 1,
    title: "Mediterranean Coastline",
    image:
      "https://images.unsplash.com/photo-1493558103817-58b2924bce98?auto=format&fit=crop&w=1200&q=80",
    duration: "7 days",
    priceRange: "$1,450 - $1,950",
    description: "Sail the azure waters and explore seaside villages.",
  },
  {
    id: 2,
    title: "Andean Peaks Expedition",
    image:
      "https://images.unsplash.com/photo-1508261306210-74f88e6e1c5c?auto=format&fit=crop&w=1200&q=80",
    duration: "7 days",
    priceRange: "$1,250 - $1,780",
    description: "Guided treks and cultural immersion in the Andes.",
  },
  {
    id: 3,
    title: "Nordic Lights Escape",
    image:
      "https://images.unsplash.com/photo-1431037242647-4c2c27cb5bb1?auto=format&fit=crop&w=1200&q=80",
    duration: "7 days",
    priceRange: "$1,980 - $2,450",
    description: "Chase the aurora borealis with local storytellers.",
  },
  {
    id: 4,
    title: "Southeast Asia Discovery",
    image:
      "https://images.unsplash.com/photo-1494475673543-6a6a27143fc8?auto=format&fit=crop&w=1200&q=80",
    duration: "7 days",
    priceRange: "$1,150 - $1,680",
    description: "Street food tours, temples, and island hopping bliss.",
  },
];

export function TourPackages() {
  return (
    <section
      id="resources"
      className="mx-auto max-w-6xl space-y-10 px-6 py-20 animate-in fade-in slide-in-from-bottom-6 duration-700"
    >
      <div className="space-y-3 text-center">
        <h2 className="text-3xl font-semibold text-slate-900 md:text-4xl">
          Our Tour Packages you’ll love
        </h2>
        <p className="text-slate-500">
          Seamless itineraries designed for indulgent explorers.
        </p>
      </div>

      <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4">
        {TOUR_PACKAGES.map((pkg) => (
          <Card
            key={pkg.id}
            className="group overflow-hidden rounded-3xl border-0 shadow-xl transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div className="relative h-48 overflow-hidden">
              <div
                className="absolute inset-0 bg-cover bg-center transition duration-500 group-hover:scale-105"
                style={{ backgroundImage: `url(${pkg.image})` }}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/75 via-slate-900/20 to-transparent" />
              <Badge className="absolute left-4 top-4 rounded-full bg-white/80 px-3 py-1 text-xs font-semibold text-slate-900">
                {pkg.duration}
              </Badge>
            </div>
            <CardHeader>
              <CardTitle className="text-xl">{pkg.title}</CardTitle>
              <CardDescription>{pkg.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-base font-semibold text-primary">
                {pkg.priceRange}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

