
        function openModal(modalId, link) {
            if (link) {
                window.open(link, '_blank');
            } else {
                document.getElementById(modalId).style.display = "block";
            }
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = "none";
        }

        function searchModal(modalId) {
            const input = document.querySelector(`#${modalId} .modal-search-container input`).value.toLowerCase();
            const cards = document.querySelectorAll(`#${modalId} .modal-image-card`);

            cards.forEach(card => {
                const title = card.querySelector('.modal-image-title').textContent.toLowerCase();
                if (title.includes(input)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
    
