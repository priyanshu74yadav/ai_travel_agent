const WINTER_DESTINATIONS = [
  {
    name: "Nepal",
    image:
      "https://images.unsplash.com/photo-1549887534-1541e9326642?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Switzerland",
    image:
      "https://images.unsplash.com/photo-1521295121783-8a321d551ad2?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Tibet",
    image:
      "https://images.unsplash.com/photo-1509644851220-51ebdcca886c?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "South Korea",
    image:
      "https://images.unsplash.com/photo-1517154421773-0529f29ea451?auto=format&fit=crop&w=1200&q=80",
  },
];

export function WinterTrips() {
  return (
    <section
      id="reviews"
      className="mx-auto max-w-6xl space-y-10 px-6 py-20 animate-in fade-in slide-in-from-bottom-6 duration-700 w-full"
    >
      <div className="space-y-3 text-center">
        <h2 className="text-3xl font-semibold text-slate-900 md:text-4xl">
          Winter Special Trips
        </h2>
        <p className="text-slate-500">
          Cozy alpine escapes and snow-dusted adventures await.
        </p>
      </div>

      <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-4 ">
        {WINTER_DESTINATIONS.map((destination) => (
          <div
            key={destination.name}
            className="group relative h-72 overflow-hidden rounded-3xl shadow-lg transition hover:-translate-y-1 hover:shadow-2xl"
          >
            <div
              className="absolute inset-0 bg-cover bg-center duration-500 group-hover:scale-105"
              style={{ backgroundImage: `url(${destination.image})` }}
            />
            <div className="absolute inset-0 bg-gradient-to-tr from-slate-900/80 via-slate-900/20 to-transparent" />
            <div className="absolute bottom-6 left-6 z-10">
              <span className="text-sm font-semibold uppercase tracking-wider text-white/80">
                Winter escape
              </span>
              <h3 className="mt-2 text-2xl font-semibold text-white">
                {destination.name}
              </h3>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

