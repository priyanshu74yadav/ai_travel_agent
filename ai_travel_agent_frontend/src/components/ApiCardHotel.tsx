import { FaMapMarkerAlt, FaStar } from "react-icons/fa";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

export interface ApiHotel {
  name: string;
  rating?: number;
  price?: string;
  address?: string;
  image?: string;
  currency?: string;
}

interface ApiCardHotelProps {
  hotel: ApiHotel;
}

const FALLBACK_IMAGE =
  "https://images.unsplash.com/photo-1568495248636-6432b97bd949?auto=format&fit=crop&w=800&q=80";

export function ApiCardHotel({ hotel }: ApiCardHotelProps) {
  const { name, rating, price, address, image } = hotel;

  return (
    <Card className="overflow-hidden rounded-3xl border-0 shadow-lg transition hover:-translate-y-1 hover:shadow-2xl">
      <div className="relative h-40 bg-slate-200">
        <div
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: `url(${image ?? FALLBACK_IMAGE})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-slate-900/50 via-slate-900/10 to-transparent" />
        {typeof rating === "number" && (
          <div className="absolute right-4 top-4 flex items-center gap-1 rounded-full bg-white px-3 py-1 text-xs font-semibold text-slate-900 shadow">
            <FaStar className="h-3 w-3 text-amber-400" />
            {rating.toFixed(1)}
          </div>
        )}
      </div>
      <CardHeader className="space-y-2">
        <CardTitle className="text-xl">{name}</CardTitle>
        {price && (
          <p className="text-base font-semibold text-primary">
            {price}
          </p>
        )}
      </CardHeader>
      <CardContent>
        {address ? (
          <CardDescription className="flex items-start gap-2 text-sm text-slate-500">
            <FaMapMarkerAlt className="mt-1 h-3.5 w-3.5 text-primary" />
            <span>{address}</span>
          </CardDescription>
        ) : (
          <CardDescription className={cn("text-sm text-slate-500")}>
            A stylish stay curated just for your escape.
          </CardDescription>
        )}
      </CardContent>
    </Card>
  );
}

