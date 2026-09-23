self.addEventListener('install', event => {
    event.skipWaiting(self.skipWaiting());
});

self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('push', event => {
    const data = event.data ? event.data.json() : {};

    event.waitUntil(
        self.registration.showNotification(data.title || 'Neighbour', {
            body: data.body || 'You have a new notification.',
            icon: '/static/images/neighbour_logo.png',
            badge: '/static/images/neighbour_logo.png',
            data: {
                url: data.url || '/'
            }
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