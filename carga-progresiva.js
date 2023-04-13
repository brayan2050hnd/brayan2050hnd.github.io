const elementos = document.querySelectorAll('img, video, audio, iframe');
let contador = 0;

function cargarElementos() {
  if (contador < elementos.length) {
    const elementoActual = elementos[contador];
    if (elementoActual.getAttribute('src') === null) {
      elementoActual.src = elementoActual.getAttribute('data-src');
      elementoActual.onload = function() {
        elementoActual.removeAttribute('data-src');
        contador++;
        cargarElementos();
      }
    } else {
      contador++;
      cargarElementos();
    }
  }
}

window.onload = cargarElementos;
