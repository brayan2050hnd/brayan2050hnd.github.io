
const video = document.getElementById('video');
const fullscreenButton = document.getElementById('fullscreen');
const muteUnmuteButton = document.getElementById('mute-unmute');
const pipButton = document.getElementById('pip');
const videoContainer = document.querySelector('.video-container');
const menuToggle = document.getElementById('menu-toggle');
const menu = document.getElementById('menu');
const videoSrc = "https://cdndirector.dailymotion.com/cdn/live/video/x81za5c.m3u8?sec=uPyN8lANTPhmRv8FNSStuFR1c3WmZ1P_D1Gb7gFdMAkYIf3wROj2gpEnJLI4UVx7ItAo8WWlAIKbEgsKhGfJV1jz3ZO2eotKvNzTJI0MKS4&dmTs=723597&dmV1st=2b195602-e2f5-46c0-b7a3-1bab442cf4ea";

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
        videoContainer.requestFullscreen().then(() => {
            if (screen.orientation && screen.orientation.lock) {
                screen.orientation.lock('landscape').catch(err => {
                    console.error('Error al bloquear la orientación:', err);
                });
            }
        }).catch(err => {
            alert(`Error al entrar en pantalla completa: ${err.message}`);
        });
    } else {
        document.exitFullscreen().then(() => {
            if (screen.orientation && screen.orientation.unlock) {
                screen.orientation.unlock().catch(err => {
                    console.error('Error al desbloquear la orientación:', err);
                });
            }
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
