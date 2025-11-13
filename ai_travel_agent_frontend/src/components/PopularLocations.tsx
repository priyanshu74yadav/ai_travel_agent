const POPULAR_LOCATIONS = [
  {
    name: "Australia",
    image:
      "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Singapore",
    image:
      "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Thailand",
    image:
      "https://images.unsplash.com/photo-1529511582893-2d7e684dd128?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Bali",
    image:
      "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "Japan",
    image:
      "https://images.unsplash.com/photo-1518544889280-6f1d3b5e72c0?auto=format&fit=crop&w=1200&q=80",
  },
  {
    name: "New Zealand",
    image:
      "https://images.unsplash.com/photo-1503754769183-0a5fb55b9a8e?auto=format&fit=crop&w=1200&q=80",
  },
];

export function PopularLocations() {
  return (
    <section
      id="discover"
      className="relative mx-auto max-w-6xl space-y-10 px-6 py-20 animate-in fade-in slide-in-from-bottom-6 duration-700 w-full"
    >
      <div className="space-y-3 text-center">
        <h2 className="text-3xl font-semibold text-slate-900 md:text-4xl">
          Explore All Popular Locations
        </h2>
        <p className="text-slate-500">
          Curated hideaways and vibrant cities to inspire your next adventure.
        </p>
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {POPULAR_LOCATIONS.map((location) => (
          <div
            key={location.name}
            className="group relative h-72 overflow-hidden rounded-3xl shadow-lg transition-transform duration-500 hover:scale-105"
          >
            <div
              className="absolute inset-0 bg-cover bg-center"
              style={{ backgroundImage: `url(${location.image})` }}
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-900/80 via-slate-900/20 to-transparent" />
            <div className="absolute bottom-6 left-6 z-10">
              <span className="rounded-full bg-white/20 px-4 py-1 text-xs font-semibold uppercase tracking-wider text-white backdrop-blur">
                Popular
              </span>
              <h3 className="mt-3 text-2xl font-semibold text-white">
                {location.name}
              </h3>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

