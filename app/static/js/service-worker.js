self.addEventListener('install', event => {
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
            icon: '/static/images/neighbour_logo.png',
            badge: '/static/images/neighbour_logo.png'
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