window.addEventListener("load", function() {
    document.body.classList.add("cargado");
  });

  
  const botonTelevision = document.getElementById("television");
  const modalPaises = document.getElementById("modal-paises");
  const botonCerrar = document.getElementById("boton-cerrar");
  
  function mostrarVentana() {
    // Muestra la ventana emergente
    modalPaises.classList.add("visible");
    botonCerrar.classList.add("visible"); // Muestra el botón de cerrar
  }
  
  // Cierra la ventana emergente al hacer clic en el botón
  botonCerrar.addEventListener("click", function() {
    ocultarVentana();
  });
  
  function ocultarVentana() {
    modalPaises.classList.remove("visible");
    botonCerrar.classList.remove("visible"); // Oculta el botón de cerrar
  }
  
  // Opcional: Añade funcionalidad a los botones de los países
  const botonesPaises = document.querySelectorAll(".pais");
  
  for (const boton of botonesPaises) {
    boton.addEventListener("click", function() {
      // Muestra información sobre el país (opcional)
      alert("Información del país: " + boton.textContent);
    });
  }

  





 
  const botonMusica = document.getElementById("musica");
  const modalMusica = document.getElementById("modal-musica");
  const botonCerrarMusica = document.getElementById("boton-cerrar-musica");
  
  botonMusica.addEventListener("click", function() {
    mostrarVentana1("modal-musica");
  });
  
  botonCerrarMusica.addEventListener("click", function() {
    ocultarVentana1("modal-musica");
  });
  
  function mostrarVentana1(idModal) {
    const modal = document.getElementById(idModal);
    modal.classList.add("visible");
  }
  
  function ocultarVentana1(idModal) {
    const modal = document.getElementById(idModal);
    modal.classList.remove("visible");
  }
  





  const botonPeliculas = document.getElementById("peliculas");
const modalPeliculas = document.getElementById("modal-peliculas");
const botonCerrarPeliculas = document.getElementById("boton-cerrar-peliculas");

botonPeliculas.addEventListener("click", function() {
  mostrarVentana2("modal-peliculas");
});

botonCerrarPeliculas.addEventListener("click", function() {
  ocultarVentana2("modal-peliculas");
});

function mostrarVentana2(idModal) {
  const modal = document.getElementById(idModal);
  modal.classList.add("visible");
}

function ocultarVentana2(idModal) {
  const modal = document.getElementById(idModal);
  modal.classList.remove("visible");
}
