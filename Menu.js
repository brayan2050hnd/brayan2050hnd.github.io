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







function searchImagesAndButtons() {
  const term = document.getElementById('search').value.toLowerCase();
  
  // Ocultar todos los elementos h4
  const h4 = document.getElementsByTagName('h4');
  for (let i = 0; i < h4.length; i++) {
    h4[i].style.display = 'none';
  }
  
  
  
  
    const h1 = document.getElementsByTagName('h1');
  for (let i = 0; i < h1.length; i++) {
    h1[i].style.display = 'none';
  }
  
  
  
  const images = document.getElementsByTagName('img');
  
  const buttons = document.getElementsByTagName('button');
  
  for (let i = 0; i < images.length; i++) {
    const alt = images[i].alt.toLowerCase();
    if (alt.includes(term)) {
      images[i].style.display = 'block';
    } else {
      images[i].style.display = 'none';
    }
  }
  
  for (let i = 0; i < buttons.length; i++) {
    const text = buttons[i].textContent.toLowerCase();
    if (text.includes(term)) {
      buttons[i].style.display = 'block';
    } else {
      buttons[i].style.display = 'none';
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