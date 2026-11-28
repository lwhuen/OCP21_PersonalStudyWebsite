const CACHE = "ocp21-6fa264f553";
const ASSETS = ["./", "Week-01-glossary.html", "Week-01-notes.html", "Week-02-glossary.html", "Week-02-notes.html", "Week-03-glossary.html", "Week-03-notes.html", "Week-04-glossary.html", "Week-04-notes.html", "Week-05-glossary.html", "Week-05-notes.html", "Week-06-glossary.html", "Week-06-notes.html", "Week-07-glossary.html", "Week-07-notes.html", "Week-08-glossary.html", "Week-08-notes.html", "index.html", "review.html", "stats.html", "strategy.html", "study-plan.html", "style.css?v=1a1555c85c", "search.js?v=1a1555c85c", "favicon.svg", "icon-192.png", "icon-512.png", "manifest.webmanifest"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ASSETS)).then(() => self.skipWaiting()));
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
    const network = fetch(request).then(keep);
    network.catch(() => {});
    event.waitUntil(network.catch(() => {}));
    event.respondWith((async () => {
      const slow = new Promise((resolve) => setTimeout(resolve, 3000));
      try {
        const first = await Promise.race([network, slow]);
        if (first) return first;
      } catch (error) {}
      const hit = (await caches.match(request, { ignoreSearch: true })) || (await caches.match("index.html"));
      return hit || network;
    })());
    return;
  }
  event.respondWith(caches.match(request).then((hit) => hit || fetch(request).then(keep)));
});
