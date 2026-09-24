const CACHE_NAME = 'neighbour-v1';

const STATIC_ASSETS = [
    '/static/manifest.json',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/app.js',
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async cache => {
            for (const asset of STATIC_ASSETS) {
                const response = await fetch(asset);

                if (response.ok) {
                    await cache.put(asset, response);
                }
            }
        })
    )

    self.skipWaiting();
});


self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', event => {
    console.log('Neighbour push event received');

    const data = event.data ? event.data.json() : {};

    console.log('Neighbour push data:', data);

    event.waitUntil(
        self.registration.showNotification('Neighbour', {
            body: data.body || 'Test notification received.',
            icon: '/static/images/neighbour_logo_badge.png',
            badge: '/static/images/neighbour_logo_badge.png'
        }).then(() => {
            console.log('Neighbour notification displayed');
        }).catch(error => {
            console.error('Neighbour notification failed:', error);
        })
    );
});

self.addEventListener('notificationclick', event => {
    event.notification.close();

    event.waitUntil(self.clients.matchAll({
        type: 'window',
        includeUncontrolled: true
    }).then(clientList => {
        for (const client of clientList) {
                if ('focus' in client) {
                    return client.focus();
                }
        }

        if (clients.openWindow) {
            return clients.openWindow('/');
        }
    }));
});