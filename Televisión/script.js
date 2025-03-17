document.addEventListener('DOMContentLoaded', function() {
    const cuadro = document.querySelector('.cuadro');
    const numero = cuadro.querySelector('.numero');
    const img = cuadro.querySelector('img');
    const h2 = cuadro.querySelector('h2');
    const video = cuadro.querySelector('video');

    let touchStart = null;

    cuadro.addEventListener('touchstart', function(event) {
        touchStart = new Date().getTime();
        event.preventDefault(); // Evitar comportamientos predeterminados

        // Ocultar elementos visuales
        numero.style.display = 'none';
        img.style.display = 'none';
        h2.style.display = 'none';

        // Mostrar video
        video.style.display = 'block';
        video.play();
    });

    cuadro.addEventListener('touchend', function(event) {
        const touchEnd = new Date().getTime();
        const duration = touchEnd - touchStart;

        // Ocultar video y pausar
        video.style.display = 'none';
        video.pause();

        // Mostrar elementos visuales
        numero.style.display = 'block';
        img.style.display = 'block';
        h2.style.display = 'block';
    });

    cuadro.addEventListener('touchmove', function(event) {
        event.preventDefault(); // Evitar comportamientos predeterminados
    });

    // Evento para dispositivos de escritorio (opcional)
    cuadro.addEventListener('mousedown', function(event) {
        const startTime = new Date().getTime();

        // Ocultar elementos visuales
        numero.style.display = 'none';
        img.style.display = 'none';
        h2.style.display = 'none';

        // Mostrar video
        video.style.display = 'block';
        video.play();

        document.addEventListener('mouseup', function() {
            // Ocultar video y pausar
            video.style.display = 'none';
            video.pause();

            // Mostrar elementos visuales
            numero.style.display = 'block';
            img.style.display = 'block';
            h2.style.display = 'block';
        }, { once: true });
    });
});
