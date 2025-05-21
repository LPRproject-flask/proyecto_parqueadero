// loader.js
function showLoader() {
  const loader = document.getElementById('loader');
  if (loader) {
    loader.classList.remove('hidden');
  }
}

function hideLoader() {
  const loader = document.getElementById('loader');
  if (loader) {
    loader.classList.add('hidden');
  }
}

// Esta función se ejecuta al hacer clic en los botones con el atributo `data-show-loader`
function attachLoaderToButtons() {
  const buttons = document.querySelectorAll('[data-show-loader]');
  buttons.forEach(button => {
    button.addEventListener('click', () => {
      showLoader();
      
      // Establecer un tiempo de espera para ocultar el loader (en este caso, 3 segundos)
      setTimeout(hideLoader, 4000); // Cambia el valor de 3000 para ajustar el tiempo (en milisegundos)
    });
  });
}

window.addEventListener('DOMContentLoaded', attachLoaderToButtons);

