document.addEventListener('DOMContentLoaded', () => {

    const animatedElements = document.querySelectorAll('.animar-entrada');

    if (!animatedElements.length) return;

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Obtener el retraso del atributo data-delay
                const delay = parseInt(entry.target.dataset.delay, 10) || 0;

                setTimeout(() => {
                    entry.target.classList.add('is-visible');
                }, delay);

                // Dejar de observar el elemento una vez animado
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    animatedElements.forEach(element => {
        observer.observe(element);
    });
});