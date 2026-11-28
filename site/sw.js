const CACHE = "ocp21-45f81f7060";
const ASSETS = ["./", "Week-01-glossary.html", "Week-01-notes.html", "Week-02-glossary.html", "Week-02-notes.html", "Week-03-glossary.html", "Week-03-notes.html", "Week-04-glossary.html", "Week-04-notes.html", "Week-05-glossary.html", "Week-05-notes.html", "Week-06-glossary.html", "Week-06-notes.html", "Week-07-glossary.html", "Week-07-notes.html", "Week-08-glossary.html", "Week-08-notes.html", "index.html", "review.html", "stats.html", "strategy.html", "study-plan.html", "style.css?v=4b46093375", "search.js?v=4b46093375", "favicon.svg", "icon-192.png", "icon-512.png", "manifest.webmanifest"];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(ASSETS.map((url) => new Request(url, { cache: "reload" }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET" || new URL(request.url).origin !== location.origin) return;
  const keep = (response) => {
    if (response.ok) {
      const copy = response.clone();
      caches.open(CACHE).then((cache) => cache.put(request, copy));
    }
    return response;
  };
  if (request.mode === "navigate") {
    event.respondWith(
      caches.match(request, { ignoreSearch: true }).then((hit) =>
        hit || fetch(request).then(keep).catch(() => caches.match("index.html"))
      )
    );
    return;
  }
  event.respondWith(caches.match(request).then((hit) => hit || fetch(request).then(keep)));
});
