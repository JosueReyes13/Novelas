// filtro_abecedario.js
// Filtro alfabético para la biblioteca de novelas ligeras

document.addEventListener('DOMContentLoaded', () => {

  const LETRAS = ['#', 'A','B','C','D','E','F','G','H','I','J','K','L','M',
                  'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'];

  // ── 1. Construir la barra de filtros ──────────────────────────────────────
  const grid = document.querySelector('.novel-grid');
  if (!grid) return; // Si no existe el grid, no hacemos nada

  const barraWrapper = document.createElement('div');
  barraWrapper.id = 'filtro-abecedario';

  // Botón "TODAS"
  const btnTodas = document.createElement('button');
  btnTodas.textContent = 'Todas';
  btnTodas.classList.add('filtro-btn', 'activo');
  btnTodas.dataset.letra = 'todas';
  barraWrapper.appendChild(btnTodas);

  // Botones por letra
  LETRAS.forEach(letra => {
    const btn = document.createElement('button');
    btn.textContent = letra;
    btn.classList.add('filtro-btn');
    btn.dataset.letra = letra;
    barraWrapper.appendChild(btn);
  });

  // Insertar la barra ANTES del grid
  grid.parentNode.insertBefore(barraWrapper, grid);

  // ── 2. Mensaje de "sin resultados" ────────────────────────────────────────
  const sinResultados = document.createElement('p');
  sinResultados.id = 'sin-resultados';
  sinResultados.textContent = 'No hay novelas con esta letra.';
  sinResultados.style.display = 'none';
  grid.parentNode.insertBefore(sinResultados, grid.nextSibling);

  // ── 3. Obtener tarjetas ───────────────────────────────────────────────────
  const tarjetas = Array.from(grid.querySelectorAll('.novel-card'));

  // ── 4. Lógica de filtrado ─────────────────────────────────────────────────
  function filtrar(letra) {
    let visibles = 0;

    tarjetas.forEach(card => {
      const titulo = card.querySelector('h4')?.textContent.trim() || '';
      let mostrar = false;

      if (letra === 'todas') {
        mostrar = true;
      } else if (letra === '#') {
        // Caracteres que no son letras del abecedario (números, símbolos…)
        mostrar = /^[^A-Za-záéíóúÁÉÍÓÚüÜñÑ]/.test(titulo);
      } else {
        // Comparación ignorando tildes
        const primeraLetra = titulo.charAt(0)
          .normalize('NFD')
          .replace(/[\u0300-\u036f]/g, '')
          .toUpperCase();
        mostrar = primeraLetra === letra;
      }

      card.style.display = mostrar ? '' : 'none';
      if (mostrar) visibles++;
    });

    // Mostrar/ocultar mensaje
    sinResultados.style.display = visibles === 0 ? 'block' : 'none';
  }

  // ── 5. Eventos de clic ────────────────────────────────────────────────────
  barraWrapper.addEventListener('click', e => {
    const btn = e.target.closest('.filtro-btn');
    if (!btn) return;

    // Marcar activo
    barraWrapper.querySelectorAll('.filtro-btn').forEach(b => b.classList.remove('activo'));
    btn.classList.add('activo');

    filtrar(btn.dataset.letra);
  });

  // ── 6. Deshabilitar botones sin novelas (opcional, mejora UX) ─────────────
  function deshabilitarVacias() {
    barraWrapper.querySelectorAll('.filtro-btn[data-letra]').forEach(btn => {
      const letra = btn.dataset.letra;
      if (letra === 'todas') return;

      const hayNovelas = tarjetas.some(card => {
        const titulo = card.querySelector('h4')?.textContent.trim() || '';
        if (letra === '#') return /^[^A-Za-záéíóúÁÉÍÓÚüÜñÑ]/.test(titulo);
        const primera = titulo.charAt(0)
          .normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase();
        return primera === letra;
      });

      btn.classList.toggle('sin-novelas', !hayNovelas);
    });
  }

  deshabilitarVacias();
});