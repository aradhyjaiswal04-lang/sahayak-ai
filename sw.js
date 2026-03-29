const CACHE_NAME = 'sahayak-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/results.html',
  '/schemes.json',
  '/logo.png'
];

// Install the service worker and cache files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

// Serve files from cache when offline
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});