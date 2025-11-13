import { ApiCardActivity, type ApiActivity } from "@/components/ApiCardActivity";
import { ApiCardHotel, type ApiHotel } from "@/components/ApiCardHotel";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export interface TravelPlan {
  hotels: ApiHotel[];
  activities: ApiActivity[];
  summary: string;
}

interface ResultsSectionProps {
  plan?: TravelPlan | null;
  loading: boolean;
}

export function ResultsSection({ plan, loading }: ResultsSectionProps) {
  if (!plan && !loading) {
    return null;
  }

  return (
    <section
      id="about"
      className="mx-auto max-w-6xl space-y-12 px-6 py-20 animate-in fade-in slide-in-from-bottom-6 duration-700"
    >
      <div className="space-y-3 text-center">
        <h2 className="text-3xl font-semibold text-slate-900 md:text-4xl">
          Your Travel Plan
        </h2>
        <p className="text-slate-500">
          Tailored recommendations for hotels, activities, and experiences.
        </p>
      </div>

      {loading ? (
        <Card className="rounded-3xl border-0 bg-white/80 p-10 text-center shadow-xl">
          <p className="animate-pulse text-lg text-slate-500">
            Crafting your travel plan...
          </p>
        </Card>
      ) : plan ? (
        <div className="space-y-16">
          <div>
            <div className="mb-6 flex items-center justify-between">
              <h3 className="text-2xl font-semibold text-slate-900">
                Stay recommendations
              </h3>
              <span className="text-sm text-slate-500">
                Handpicked hotels matched to your budget.
              </span>
            </div>
            <div className="grid gap-6 md:grid-cols-2">
              {plan.hotels.map((hotel) => (
                <ApiCardHotel key={hotel.name} hotel={hotel} />
              ))}
            </div>
          </div>

          <div>
            <div className="mb-6 flex items-center justify-between">
              <h3 className="text-2xl font-semibold text-slate-900">
                Experiences you’ll love
              </h3>
              <span className="text-sm text-slate-500">
                Adventures, food, and culture — all in one.
              </span>
            </div>
            <div className="grid gap-6 md:grid-cols-2">
              {plan.activities.map((activity) => (
                <ApiCardActivity key={activity.name} activity={activity} />
              ))}
            </div>
          </div>

          <Card className="rounded-3xl border-0 bg-gradient-to-r from-slate-900 via-slate-800 to-slate-700 text-white shadow-2xl">
            <CardHeader>
              <CardTitle className="text-2xl">AI-Powered Summary</CardTitle>
              <CardDescription className="text-slate-200">
                Based on your preferences and budget.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-lg leading-relaxed">{plan.summary}</p>
            </CardContent>
          </Card>
        </div>
      ) : null}
    </section>
  );
}

