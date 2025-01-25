
const video = document.getElementById('video');
const fullscreenButton = document.getElementById('fullscreen');
const muteUnmuteButton = document.getElementById('mute-unmute');
const pipButton = document.getElementById('pip');
const videoContainer = document.querySelector('.video-container');
const menuToggle = document.getElementById('menu-toggle');
const menu = document.getElementById('menu');
const videoSrc = "https://cdndirector.dailymotion.com/cdn/live/video/x81za5c.m3u8?sec=5p7gnyQ8VEMECSppNFfyTkAkHUc3Up0pdsd5O24ErUpj0tTwvq4A7Lugc5B7oQZVlOrBdWz3iBk_FecfBRb6B42JuK1-E0cnUEl9qkJCGY0&dmTs=170393&dmV1st=5e5398ff-7f9c-7726-6d5d-728d55816669";

if (Hls.isSupported()) {
    const hls = new Hls();
    hls.loadSource(videoSrc);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
        video.muted = true;
        video.play().catch(error => {
            console.error('Error al reproducir el video:', error);
        });
    });
} else if (video.canPlayType('application/vnd.apple.mpegurl')) {
    video.src = videoSrc;
    video.addEventListener('loadedmetadata', () => {
        video.muted = true;
        video.play().catch(error => {
            console.error('Error al reproducir el video:', error);
        });
    });
}

muteUnmuteButton.addEventListener('click', () => {
    if (video.muted) {
        video.muted = false;
        muteUnmuteButton.innerHTML = '<i class="fas fa-volume-up"></i>';
    } else {
        video.muted = true;
        muteUnmuteButton.innerHTML = '<i class="fas fa-volume-mute"></i>';
    }
});

fullscreenButton.addEventListener('click', () => {
    if (!document.fullscreenElement) {
        videoContainer.requestFullscreen().catch(err => {
            console.error('Error al entrar en pantalla completa:', err);
        });
    } else {
        document.exitFullscreen().catch(err => {
            console.error('Error al salir de pantalla completa:', err);
        });
    }
});

pipButton.addEventListener('click', async () => {
    try {
        if (document.pictureInPictureElement) {
            await document.exitPictureInPicture();
        } else {
            await video.requestPictureInPicture();
        }
    } catch (error) {
        console.error('Error al cambiar a Picture-in-Picture:', error);
    }
});

menuToggle.addEventListener('click', (event) => {
    event.stopPropagation();
    menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
});

document.addEventListener('click', (event) => {
    if (menu.style.display === 'block' && !menu.contains(event.target) && event.target !== menuToggle) {
        menu.style.display = 'none';
    }
});

function showControls() {
    videoContainer.classList.add('show-controls');
    clearTimeout(videoContainer.timeout);
    videoContainer.timeout = setTimeout(() => {
        videoContainer.classList.remove('show-controls');
    }, 2000);
}

video.addEventListener('click', showControls);
