// services/static/services/js/servicios.js

document.addEventListener('DOMContentLoaded', () => {

    // Función para animar elementos al ser visibles
    const animateOnScroll = () => {
        const elementsToAnimate = document.querySelectorAll('.fade-in-up');

        if (!elementsToAnimate.length) {
            return;
        }

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                // Si el elemento es visible
                if (entry.isIntersecting) {
                    entry.target.classList.add('is-visible');
                    // Opcional: deja de observar el elemento una vez que ha sido animado
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1 // La animación se dispara cuando el 10% del elemento es visible
        });

        elementsToAnimate.forEach(element => {
            observer.observe(element);
        });
    };

    // Inicializar la función
    animateOnScroll();

});