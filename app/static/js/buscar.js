// search.js - Funcionalidad del buscador

// Esperar a que cargue el DOM
document.addEventListener('DOMContentLoaded', function() {
    const searchToggle = document.getElementById('search-toggle');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    // Cargar la lista de novelas desde el servidor
    let novelasList = [];
    
    // Obtener las novelas mediante fetch
    fetch('/api/novelas')
        .then(response => response.json())
        .then(data => {
            novelasList = data;
        })
        .catch(error => console.error('Error cargando novelas:', error));
    
    // Toggle del buscador
    if (searchToggle) {
        searchToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            searchForm.classList.toggle('active');
            if (searchForm.classList.contains('active')) {
                searchInput.focus();
            }
        });
    }
    
    // Función para cerrar el buscador
    function closeSearch() {
        searchForm.classList.remove('active');
        searchInput.value = '';
        searchResults.innerHTML = '';
    }
    
    // Cerrar buscador al hacer click fuera
    document.addEventListener('click', function(e) {
        const searchContainer = document.querySelector('.search-container');
        if (searchContainer && !searchContainer.contains(e.target)) {
            closeSearch();
        }
    });
    
    // Función para buscar novelas
    function searchNovelas(query) {
        if (!query.trim()) {
            searchResults.innerHTML = '';
            return;
        }
        
        const resultados = novelasList.filter(novela => 
            novela.toLowerCase().includes(query.toLowerCase())
        );
        
        if (resultados.length > 0) {
            searchResults.innerHTML = resultados.map(novela => `
                <div class="search-result-item">
                    <a href="/novela/${encodeURIComponent(novela)}">${escapeHtml(novela)}</a>
                </div>
            `).join('');
        } else {
            searchResults.innerHTML = '<div class="no-results">No se encontraron novelas</div>';
        }
    }
    
    // Función para escapar HTML (seguridad)
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Evento de búsqueda
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            searchNovelas(e.target.value);
        });
    }
    
    // Cerrar buscador al hacer clic en un resultado
    if (searchResults) {
        searchResults.addEventListener('click', function(e) {
            closeSearch();
        });
    }
    
    // Cerrar con tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && searchForm.classList.contains('active')) {
            closeSearch();
        }
    });
});