import { FaStar } from "react-icons/fa";
import { LuTicket } from "react-icons/lu";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export interface ApiActivity {
  name: string;
  rating?: number;
  price?: string;
  category?: string;
  image?: string;
}

interface ApiCardActivityProps {
  activity: ApiActivity;
}

const FALLBACK_IMAGE =
  "https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?auto=format&fit=crop&w=800&q=80";

export function ApiCardActivity({ activity }: ApiCardActivityProps) {
  const { name, rating, price, category, image } = activity;

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
      <CardHeader className="space-y-1">
        <CardTitle className="text-xl">{name}</CardTitle>
        {category && <CardDescription>{category}</CardDescription>}
      </CardHeader>
      <CardContent>
        <p className="flex items-center gap-2 text-sm font-semibold text-primary">
          <LuTicket className="h-4 w-4" />
          {price ?? "Included in your plan"}
        </p>
      </CardContent>
    </Card>
  );
}

