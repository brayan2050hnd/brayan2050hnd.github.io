    
      const images1 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Canal_5_Honduras.webp/1200px-Canal_5_Honduras.webp.png",
        "https://i.ytimg.com/vi/2q1ltRgrtLk/hqdefault.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Canal_5_HN_logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/a/ad/Canal_5_HN_logo_2019.png",
      ];

      const images2 = [
        "https://picsum.photos/100/60?random=5",
        "https://picsum.photos/100/60?random=6",
        "https://picsum.photos/100/60?random=7",
        "https://picsum.photos/100/60?random=8"
      ];

      const images3 = [
        "https://picsum.photos/100/60?random=9",
        "https://picsum.photos/100/60?random=10",
        "https://picsum.photos/100/60?random=11",
        "https://picsum.photos/100/60?random=12"
      ];
      
      
      
      
      const images4 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Canal_5_Honduras.webp/1200px-Canal_5_Honduras.webp.png",
        "https://i.ytimg.com/vi/2q1ltRgrtLk/hqdefault.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Canal_5_HN_logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/a/ad/Canal_5_HN_logo_2019.png",
      ];

      const images5 = [
        "https://picsum.photos/100/60?random=5",
        "https://picsum.photos/100/60?random=6",
        "https://picsum.photos/100/60?random=7",
        "https://picsum.photos/100/60?random=8"
      ];

      const images6 = [
        "https://picsum.photos/100/60?random=9",
        "https://picsum.photos/100/60?random=10",
        "https://picsum.photos/100/60?random=11",
        "https://picsum.photos/100/60?random=12"
      ];

      const imgElements = document.querySelectorAll(".card-img");

      let index1 = 0;
      let index2 = 0;
      let index3 = 0;
      let index4 = 0;
      let index5 = 0;
      let index6 = 0;

      setInterval(() => {
        index1 = (index1 + 1) % images1.length;
        imgElements[0].src = images1[index1];
      }, 4000);

      setInterval(() => {
        index2 = (index2 + 1) % images2.length;
        imgElements[1].src = images2[index2];
      }, 4500);

      setInterval(() => {
        index3 = (index3 + 1) % images3.length;
        imgElements[2].src = images3[index3];
      }, 5000);
    
    
    setInterval(() => {
        index4 = (index4 + 1) % images1.length;
        imgElements[3].src = images4[index4];
      }, 5500);

      setInterval(() => {
        index5 = (index5 + 1) % images2.length;
        imgElements[4].src = images5[index5];
      }, 6000);

      setInterval(() => {
        index6 = (index6 + 1) % images3.length;
        imgElements[5].src = images6[index6];
      }, 6500);
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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











const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click", () => {
    nav.classList.add("visible");
})

cerrar.addEventListener("click", () => {
    nav.classList.remove("visible");
})






document.getElementById("myBtn").addEventListener("click", function(){
   location.reload();
});








const searchBtn = document.getElementById('search-btn');
const searchInput = document.getElementById('search-input');
const cards = document.querySelectorAll('.card');

searchBtn.addEventListener('click', () => {
  const searchTerm = searchInput.value.toLowerCase();
  
  cards.forEach(card => {
    const title = card.querySelector('.card-title').textContent.toLowerCase();
    
    if (title.includes(searchTerm)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
});
