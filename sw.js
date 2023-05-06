self.addEventListener('sync', function(event) {
    if (event.tag === 'sync') {
        event.waitUntil(
            self.registration.showNotification('Solicitud de permiso', {
                body: 'Se requiere permiso de segundo plano para continuar',
                icon: 'icon.png'
            })
        );
    }
});
