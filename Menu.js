var contenedor = document.getElementById('contenedor');

function reproducirContenido(tipo, url) {
	// Vaciamos el contenido del contenedor
	contenedor.innerHTML = '';

	// Creamos el elemento correspondiente según el tipo de contenido
	if (tipo === 'iframe') {
		var iframe = document.createElement('iframe');
		iframe.setAttribute('src', url);
		iframe.setAttribute('frameborder', '0');
		iframe.setAttribute('allowfullscreen', 'true');
		iframe.setAttribute('width', '100%');
		iframe.setAttribute('height', '200em');
		contenedor.appendChild(iframe);
	} else if (tipo === 'm3u8') {
		var video = document.createElement('video');
		video.setAttribute('controls', '');
		
		var source = document.createElement('source');
		source.setAttribute('src', url);
		source.setAttribute('type', 'application/x-mpegURL');
		

		
		video.setAttribute('width', '100%');
  video.setAttribute('height', '100%');
  
		video.appendChild(source);
		contenedor.appendChild(video);
	}
}




function buscar() {
  // Obtener el texto ingresado por el usuario
  var input = document.getElementById("buscador").value.toLowerCase();
  // Obtener todos los botones
  var botones = document.getElementsByTagName("button");
  // Iterar por todos los botones y ocultar aquellos que no coincidan con la búsqueda
  for (var i = 0; i < botones.length; i++) {
    if (botones[i].innerHTML.toLowerCase().indexOf(input) > -1) {
      botones[i].style.display = "";
    } else {
      botones[i].style.display = "none";
      
    }
  }
}




  




const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click", () => {
    nav.classList.add("visible");
})

cerrar.addEventListener("click", () => {
    nav.classList.remove("visible");
})
