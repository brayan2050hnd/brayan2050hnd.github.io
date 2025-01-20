
function showContent(countryId) {
    document.getElementById("country-list").style.display = "none";
    document.getElementById("title").style.display = "none";
    document.getElementById("content").classList.remove("hidden");

    const countries = document.querySelectorAll(".country-content");
    countries.forEach(country => {
        country.style.display = "none";
    });

    document.getElementById(countryId).style.display = "block";
}

function goBack() {
    // Mostrar la lista de países y el título
    document.getElementById("country-list").style.display = "block";
    document.getElementById("title").style.display = "block";
    document.getElementById("content").classList.add("hidden");

    // Detener cualquier video que esté reproduciéndose
    const players = document.querySelectorAll("iframe");
    players.forEach(player => {
        player.src = ""; // Limpiar el src para detener la reproducción
    });
}

function playVideo(playerId, videoSrc) {
    document.getElementById(playerId).src = videoSrc;
}

function filterCards(countryId, searchTerm) {
    const cards = document.querySelectorAll(`#${countryId} .card`);
    searchTerm = searchTerm.toLowerCase().trim(); // Convertimos a minúsculas y eliminamos espacios

    cards.forEach(card => {
        const title = card.querySelector('h3').innerText.toLowerCase();
        // Si el término de búsqueda está vacío, mostramos todas las tarjetas
        if (searchTerm === '' || title.includes(searchTerm)) {
            card.style.display = ''; // Mostrar tarjeta
        } else {
            card.style.display = 'none'; // Ocultar tarjeta
        }
    });
}
