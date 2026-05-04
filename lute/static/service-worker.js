const LUTE_PWA_CACHE = "lute-pwa-v1";
const LUTE_OFFLINE_URL = "/offline";

const LUTE_PRECACHED_URLS = [
  LUTE_OFFLINE_URL,
  "/static/css/styles.css",
  "/static/css/player-styles.css",
  "/static/favicon.ico",
  "/static/img/lute.png",
  "/static/img/apple-touch-icon-114x114.png",
  "/static/img/pwa-icon-192.png",
  "/static/img/pwa-icon-512.png"
];

self.addEventListener("install", function (event) {
  event.waitUntil(
    caches.open(LUTE_PWA_CACHE)
      .then(function (cache) {
        return cache.addAll(LUTE_PRECACHED_URLS);
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

self.addEventListener("activate", function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (cacheNames) {
        return Promise.all(
          cacheNames
            .filter(function (cacheName) {
              return cacheName !== LUTE_PWA_CACHE;
            })
            .map(function (cacheName) {
              return caches.delete(cacheName);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

function isCacheableStaticAsset(requestUrl) {
  if (requestUrl.origin !== self.location.origin) {
    return false;
  }

  if (!requestUrl.pathname.startsWith("/static/")) {
    return false;
  }

  return !requestUrl.pathname.startsWith("/static/js/never_cache/");
}

function networkFirstStatic(request) {
  return fetch(request)
    .then(function (response) {
      if (response && response.ok) {
        const responseToCache = response.clone();
        caches.open(LUTE_PWA_CACHE).then(function (cache) {
          cache.put(request, responseToCache);
        });
      }
      return response;
    })
    .catch(function () {
      return caches.match(request).then(function (cachedResponse) {
        return cachedResponse || Response.error();
      });
    });
}

function navigationFallback(request) {
  return fetch(request)
    .catch(function () {
      return caches.match(LUTE_OFFLINE_URL);
    });
}

self.addEventListener("fetch", function (event) {
  const request = event.request;

  if (request.method !== "GET") {
    return;
  }

  const requestUrl = new URL(request.url);

  if (requestUrl.origin !== self.location.origin) {
    return;
  }

  if (request.mode === "navigate") {
    event.respondWith(navigationFallback(request));
    return;
  }

  if (isCacheableStaticAsset(requestUrl)) {
    event.respondWith(networkFirstStatic(request));
  }
});
