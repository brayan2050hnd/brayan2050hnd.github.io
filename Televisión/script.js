// script.js
const videoPlayer = document.getElementById("videoPlayer");
const customControls = document.getElementById("customControls");
const liveIndicator = document.getElementById("liveIndicator");
const muteButton = document.getElementById("muteButton");
const fullscreenButton = document.getElementById("fullscreenButton");
const popupButton = document.getElementById("popupButton");
let controlsTimeout;

// Desactivar los controles predeterminados
videoPlayer.removeAttribute("controls");

// Cargar un archivo m3u8
const mediaUrl = "URL_DEL_ARCHIVO_M3U8"; // Reemplázalo con la URL del video.
if (Hls.isSupported()) {
  const hls = new Hls();
  hls.loadSource(mediaUrl);
  hls.attachMedia(videoPlayer);
} else if (videoPlayer.canPlayType("application/vnd.apple.mpegurl")) {
  videoPlayer.src = mediaUrl;
}

// Mostrar y ocultar controles
videoPlayer.addEventListener("click", () => {
  // Hacer visibles los controles y el texto "En Vivo"
  customControls.classList.add("visible");
  liveIndicator.classList.add("visible");

  clearTimeout(controlsTimeout);
  
  // Ocultar los controles y el texto "En Vivo" después de 3 segundos
  controlsTimeout = setTimeout(() => {
    customControls.classList.remove("visible");
    liveIndicator.classList.remove("visible");
  }, 3000);
});

// Botón de silencio
muteButton.addEventListener("click", () => {
  videoPlayer.muted = !videoPlayer.muted;
  muteButton.innerHTML = videoPlayer.muted ? "<i class='fas fa-volume-up'></i>" : "<i class='fas fa-volume-mute'></i>";
});

// Botón de pantalla completa
fullscreenButton.addEventListener("click", () => {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    videoPlayer.requestFullscreen();
  }
});

// Detectar cuando se entra o se sale de pantalla completa
document.addEventListener("fullscreenchange", () => {
  if (document.fullscreenElement) {
    // Al entrar en pantalla completa, aseguramos que los controles personalizados se mantengan visibles
    customControls.classList.add("visible");
    // Evitar que los controles por defecto se activen en pantalla completa
    videoPlayer.controls = false;
  } else {
    // Cuando se sale de pantalla completa, ocultamos los controles
    customControls.classList.remove("visible");
    videoPlayer.controls = false;  // Desactivar controles por defecto al salir de pantalla completa
  }
});

// Botón de ventana emergente
popupButton.addEventListener("click", () => {
  window.open(mediaUrl, "_blank", "width=800,height=450");
});