/*
 * Archivo: proyecto.js
 * Descripción: Funcionalidad JavaScript customizada para el Proyecto Cartelera de Cine.
 * Autor: Javier Cachón Garrido (Refactorizado con Gemini)
 */

document.addEventListener('DOMContentLoaded', function () {
    // === Lógica para el Modal de Confirmación de Eliminación (index.html) ===
    const deleteConfirmModal = document.getElementById('deleteConfirmModal');

    if (deleteConfirmModal) {
        const deleteForm = document.getElementById('deleteForm');
        const modalPeliculaTitulo = document.getElementById('modalPeliculaTitulo');
        const modalPeliculaId = document.getElementById('modalPeliculaId');

        deleteConfirmModal.addEventListener('show.bs.modal', function (event) {
            // Botón que disparó el modal
            const button = event.relatedTarget; 
            
            // Extraer datos del botón (data-* attributes)
            const peliculaId = button.getAttribute('data-pelicula-id');
            const peliculaTitulo = button.getAttribute('data-pelicula-titulo');

            // 1. Actualizar los detalles en el cuerpo del modal
            if (modalPeliculaTitulo) modalPeliculaTitulo.textContent = peliculaTitulo;
            if (modalPeliculaId) modalPeliculaId.textContent = peliculaId;

            // 2. Actualizar la acción del formulario
            if (deleteForm && peliculaId) {
                deleteForm.action = `/peliculas/eliminar/${peliculaId}`;
            }
        });
    }

    // === Lógica de Inicialización Global (si se necesita más adelante) ===
    // Por ejemplo: 
    // const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    // const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));

});