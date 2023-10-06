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


// Variables
var images = document.querySelectorAll("img");
var transmisiones = [
  {
    id: 1,
    url: "https://cdn.jwplayer.com/players/OIytnimW-9lfZClGD.html",
    type: "iframe",
  },
  {
    id: 2,
    url: "https://mdstrm.com/live-stream/6287fda8ea3b8b397d1ca2ed",
    type: "m3u8",
  },
  {
    id: 3,
    url: "https://cdn.jwplayer.com/players/OIytnimW-9lfZClGD.html",
    type: "iframe",
  },
  {
    id: 4,
    url: "https://mdstrm.com/live-stream/6287fda8ea3b8b397d1ca2ed",
    type: "m3u8",
  },
];

// Función para ocultar las imágenes
function ocultarImagenes() {
  images.forEach(function(img) {
    img.style.display = "none";
  });
}

// Función para reproducir la transmisión
function reproducirTransmision(id) {
  // Ocultar las imágenes
  ocultarImagenes();

  // Obtener la transmisión
  var transmision = transmisiones[id - 1];

  // Reproducir la transmisión
  if (transmision.type === "iframe") {
    var iframe = document.createElement("iframe");
    iframe.src = transmision.url;
    iframe.controls = true;
    iframe.style.width = "100%";
    iframe.style.height = "100%";
    document.querySelector("body").appendChild(iframe);
    'iframe.play()';
  } else if (transmision.type === "m3u8") {
    var video = document.createElement("video");
    video.src = transmision.url;
    video.controls = true;
    video.style.width = "100%";
    video.style.height = "100%";
    document.querySelector("body").appendChild(video);
    video.play();
  }
}

// Eventos click
images.forEach(function(img, index) {
  img.addEventListener("click", function() {
    reproducirTransmision(index + 1);
  });
});




