    

  

    const loader = document.querySelector('.loader');

setTimeout(() => {
  loader.style.display = 'none';
}, 5000);

    
    
    
      const images1 = [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Canal_5_Honduras.webp/1200px-Canal_5_Honduras.webp.png",
        "https://i.ytimg.com/vi/2q1ltRgrtLk/hqdefault.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/Canal_5_HN_logo.png",
        "https://upload.wikimedia.org/wikipedia/commons/a/ad/Canal_5_HN_logo_2019.png",
      ];

      const images2 = [
        "https://upload.wikimedia.org/wikipedia/commons/f/ff/TSi_logo.png",
        "https://programacion.televicentro.com/images/tsi.png",
        "https://s3.amazonaws.com/prod-wp-tvc/wp-content/uploads/2020/05/Generica-TSi.png",
        "https://cdn.mitvstatic.com/programs/hn_noticiero-infantil-tsi_p_m.jpg"
      ];

      const images3 = [
        "https://upload.wikimedia.org/wikipedia/commons/4/40/Telecadena7y42018.png",
        "https://i.pinimg.com/originals/38/89/11/3889115d234269ff87bdcc812f815a6c.jpg",
        "https://s3.amazonaws.com/prod-wp-tvc/wp-content/uploads/2020/05/Generica-Canal-7.png",
        "https://programacion.televicentro.com/images/telecadena.png"
      ];
      
      
      
      
      const images4 = [
        "https://hch.tv/wp-content/uploads/2021/09/logos-hch-bueno-1.png",
        "https://www.televisiongratis.tv/components/com_televisiongratis/images/hch-en-vivo-889.jpg",
        "https://pbs.twimg.com/media/EPjyAw4XsAADHJc.jpg",
        "https://hch.tv/wp-content/uploads/2021/06/WhatsApp-Image-2021-06-13-at-5.54.02-PM.jpeg",
      ];

      const images5 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/52439c85-e2bd-4b9d-a51c-96a4fa0e51d1",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRco0VV0bCbEa5pp7yJdwNhYOL-Wv0003SrpQ&usqp=CAU",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/MetroTV_2000.svg/2560px-MetroTV_2000.svg.png",
        "https://w7.pngwing.com/pngs/859/451/png-transparent-metrotv-indonesia-television-channel-news-metro-city-television-text-trademark.png"
      ];

      const images6 = [
        "https://i0.wp.com/directostv.teleame.com/wp-content/uploads/2017/10/Canal-11-Aysen-en-vivo-Online.png?fit=1920%2C1080&ssl=1",
        "https://upload.wikimedia.org/wikipedia/commons/3/32/Canal_11_HN_logo_2010.png",
        "https://www.oncenoticias.hn/wp-content/uploads/2022/11/C11-1-990x557.jpg",
        "https://www.oncenoticias.hn/wp-content/uploads/2018/11/CANAL-11.jpg"
      ];
      
      
      const images7 = [
        "https://pbs.twimg.com/media/DM71p8GX0AENVWT.jpg:large",
        "https://apprecs.org/gp/images/app-icons/300/0c/com.yourappland.tdtv.jpg",
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/898a3be8-230b-4b73-96db-a6163101384f",
        "https://lh3.googleusercontent.com/apXbKaSmEba3reAuL6Lcu3jXrh_BdfDxNU0fYUDRXHc1Q9OyQP8NH0-oER6VeURPjA=w1024"
      ];
      
      
      
      
      const images8 = [
        "https://i.ytimg.com/vi/dmOxCxMyJVs/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLB3UEy-P_awVYXL9z4lKDdg-N1Qwg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQT_MfT5NRJ3kkOBG5MJmVr7v2LYKtFIYHyug&usqp=CAU",
        "https://2.bp.blogspot.com/--HxQ_rnA4hU/Wdv5wSG_xuI/AAAAAAAAAko/5vqniQKxFiYszx7QjEUjX4Sb3qQN-r7TQCLcBGAs//TEN-TV-Honduras.png",
        "https://www.tencanal10.tv/wp-content/uploads/2017/07/mintenani.jpg",
      ];

      const images9 = [
        "https://3dwarehouse.sketchup.com/warehouse/v1.0/content/public/67780b66-feb8-4d2d-909c-5661e68d4ec8",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7EY4BFHsFaYKh0O6ZXXUeK1AeoJW3F8-W_A&usqp=CAU",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRit-FZiN03VG1tIcchJof7p_SG6n42scxQXw&usqp=CAU",
        "https://yt3.googleusercontent.com/ytc/AL5GRJWlh6psUNchVdXl4Q9fCU3_v6HG7gppeHD8kHkJ=s900-c-k-c0x00ffffff-no-rj"
      ];

      
      
      
      
      
      
      
      

      const imgElements = document.querySelectorAll(".card-img");

      let index1 = 0;
      let index2 = 0;
      let index3 = 0;
      let index4 = 0;
      let index5 = 0;
      let index6 = 0;
      let index7 = 0;
      let index8 = 0;
      let index9 = 0;

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
    
    
    setInterval(() => {
        index7 = (index7 + 1) % images1.length;
        imgElements[6].src = images7[index7];
      }, 7000);
    
    setInterval(() => {
        index8 = (index8 + 1) % images2.length;
        imgElements[7].src = images8[index8];
      }, 7500);
    
    setInterval(() => {
        index9 = (index9 + 1) % images3.length;
        imgElements[8].src = images9[index9];
      }, 8000);
    
    
    
    
    
    
    
    
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








function searchImagesAndButtons() {
  const term = document.getElementById('search').value.toLowerCase();
  
  // Ocultar todos los elementos h4
  const h2 = document.getElementsByTagName('h2');
  for (let i = 0; i < h2.length; i++) {
    h2[i].style.display = 'none';
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







  const searchButton = document.getElementById('search-button');
  const searchInput = document.getElementById('search-bar');
  const cards = document.querySelectorAll('.card');

  searchButton.addEventListener('click', () => {
    const searchText = searchInput.value.toLowerCase();
    cards.forEach(card => {
      const imageSrc = card.querySelector('.card-img').getAttribute('src').toLowerCase();
      if (imageSrc.includes(searchText)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });


