const CACHE_NAME = "app-entrenamiento-v1";
const STATIC_ASSETS = [
    "/static/frontend/style.css",
    "/static/frontend/icon-192.png",
    "/static/frontend/icon-512.png",
];

self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
    );
});

self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((names) =>
            Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
        )
    );
});

self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);

    // Estáticos: cache primero, red como respaldo
    if (url.pathname.startsWith("/static/")) {
        event.respondWith(
            caches.match(event.request).then((cached) => cached || fetch(event.request))
        );
        return;
    }

    // Páginas dinámicas: red primero, cache como respaldo si no hay conexión
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});