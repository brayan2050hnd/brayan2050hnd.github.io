const boton1 = document.getElementById("boton1");
const contenido1 = document.getElementById("contenido1");
const boton2 = document.getElementById("boton2");
const contenido2 = document.getElementById("contenido2");
const titulo = document.getElementById("titulo");

boton1.addEventListener("click", function() {
  contenido1.style.display = "block";
  contenido2.style.display = "none";
  boton1.style.display = "none";
  boton2.style.display = "none";
	titulo.style.display = "none";
});

boton2.addEventListener("click", function() {
  contenido2.style.display = "block";
  contenido1.style.display = "none";
  boton1.style.display = "none";
  boton2.style.display = "none";
	titulo.style.display = "none";
});

const botonRetroceso1 = document.getElementById("boton-retroceso1");
botonRetroceso1.addEventListener("click", function() {
  contenido1.style.display = "none";
  boton1.style.display = "block";
  boton2.style.display = "block";
	titulo.style.display = "block";
});

const botonRetroceso2 = document.getElementById("boton-retroceso2");
botonRetroceso2.addEventListener("click", function() {
  contenido2.style.display = "none";
  boton1.style.display = "block";
  boton2.style.display = "block";
	titulo.style.display = "block";
});



const botonCancelar = document.createElement("button");
botonCancelar.textContent = "Cancelar";
botonCancelar.addEventListener("click", function() {
  if (contenido1.style.display === "block") {
    contenido1.querySelector(".opciones").style.display = "none";
  }
});

opciones.appendChild(botonCancelar);



function mostraropciones() {
  const opciones = document.querySelector("#opciones");
  opciones.style.display = "block";
  boton1.style.display = "none";
  boton2.style.display = "none";
}




opciones.appendChild(botonCancelar);


function playStream(streamId) {
  var streamUrl = "https://cdn.jwplayer.com/players/OIytnimW-9lfZClGD.html";
  switch (streamId) {
    case 1:
      streamUrl = "https://cdn.jwplayer.com/players/OIytnimW-9lfZClGD.html";
      break;
    case 2:
      streamUrl = "https://mdstrm.com/live-stream/6287fda8ea3b8b397d1ca2ed";
      break;
    case 3:
      streamUrl = "https://mdstrm.com/live-stream/6287fda8ea3b8b397d1ca2ed";
      break;
  }

  // Ocultar imágenes
  document.querySelectorAll("img").forEach(function(img) {
    img.style.display = "none";
  });

  // Verificar tipo de transmisión
  var isIframe = streamUrl.match(/iframe/i);

  // Agregar transmisión al DOM
  if (isIframe) {
    // Crear iframe
    var iframe = document.createElement("iframe");
    iframe.src = streamUrl;
    iframe.controls = true;
    iframe.style.width = "100%";
    iframe.style.height = "100%";

    // Esperar a que se cargue el iframe
    iframe.addEventListener("load", function() {
      // Agregar iframe al DOM
      document.querySelector("body").appendChild(iframe);
      iframe.play();
    });
  } else {
    var video = document.createElement("video");
    video.src = streamUrl;
    video.controls = true;
    video.style.width = "100%";
    video.style.height = "100%";
    document.querySelector("body").appendChild(video);

    animarDesplazamiento(video);
  }

  // Agregar evento de deslizamiento
  var startX;
  var startY;

  video.addEventListener("touchstart", function(event) {
    // Guardar la posición inicial del dedo
    startX = event.touches[0].clientX;
    startY = event.touches[0].clientY;
  });

  video.addEventListener("touchmove", function(event) {
    // Obtener la posición actual del dedo
    var endX = event.touches[0].clientX;
    var endY = event.touches[0].clientY;

    // Calcular la distancia recorrida
    var deltaX = endX - startX;
    var deltaY = endY - startY;

    // Si la distancia recorrida es mayor a un umbral, quitar la transmisión
    if (Math.abs(deltaY) > 100) {
      quitar();
    }

    // Desplazar la transmisión
    video.style.transform = "translateX(" + deltaX + "px)";
  });
}


function quitar() {
  // Eliminar transmisiones
  var videos = document.querySelectorAll("video, iframe");
  videos.forEach(function(video) {
    video.pause();
    video.remove();
  });

  // Mostrar imágenes
  document.querySelectorAll("img").forEach(function(img) {
    img.style.display = "block";
  });
}




function animarDesplazamiento(video) {
  // Guardar la posición inicial del dedo
  startX = video.getBoundingClientRect().left;

  // Agregar evento de seguimiento del dedo
  video.addEventListener("touchmove", function(event) {
    // Obtener la posición actual del dedo
    var endX = event.touches[0].clientX;

    // Calcular la distancia recorrida
    var deltaX = endX - startX;

    // Animar desplazamiento
    video.style.transform = "translateX(" + deltaX + "px) translateZ(-10px)";
  });
}








