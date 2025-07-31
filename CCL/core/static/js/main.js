
document.addEventListener('DOMContentLoaded', function() {

    // --- LÓGICA PARA EL PRELOADER ---
    const preloader = document.getElementById('preloader');
    if (preloader) {
        setTimeout(() => {
            preloader.classList.add('preloader-hidden');
        }, 200);
        setTimeout(() => {
            if (preloader.parentNode) {
                preloader.parentNode.removeChild(preloader);
            }
        }, 1000);
    }

    // --- LÓGICA PARA EL NAVBAR DINÁMICO ---
    const navbar = document.getElementById('navbar-main');
    const heroSection = document.querySelector('.hero-full-screen');
    if (navbar && heroSection) {
        const handleScroll = () => {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-solid');
                navbar.classList.remove('navbar-transparent');
            } else {
                navbar.classList.remove('navbar-solid');
                navbar.classList.add('navbar-transparent');
            }
        };
        handleScroll();
        window.addEventListener('scroll', handleScroll);
    }

    // --- LÓGICA PARA ANIMACIONES AL HACER SCROLL ---
    const animatedElements = document.querySelectorAll('.anim-fade-in-up, .anim-fade-in-down, .anim-fade-in-left, .anim-fade-in-right');

    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1 // Animar cuando el 10% es visible
        });

        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }

    // --- LÓGICA PARA LA ANIMACIÓN DE MÁQUINA DE ESCRIBIR ---
    const typewriterElement = document.querySelector('.typewriter-text');
    
    // Solo ejecuta el script si el elemento existe en la página actual
    if (typewriterElement) {
        const textToAnimate = "¿Listo para Impulsar tu Negocio?";
        let i = 0;
        let isErasing = false;

        function typeLoop() {
            if (isErasing) {
                // Acción de borrar
                typewriterElement.textContent = textToAnimate.substring(0, i - 1);
                i--;
            } else {
                // Acción de escribir
                typewriterElement.textContent = textToAnimate.substring(0, i + 1);
                i++;
            }

            if (!isErasing && i === textToAnimate.length) {
                // Pausa al final de la escritura y empieza a borrar
                isErasing = true;
                setTimeout(typeLoop, 2000); // Pausa de 2 segundos
            } else if (isErasing && i === 0) {
                // Pausa al final del borrado y empieza a escribir de nuevo
                isErasing = false;
                setTimeout(typeLoop, 500); // Pausa de 0.5 segundos
            } else {
                // Continúa la animación
                const speed = isErasing ? 50 : 120; // Borra más rápido de lo que escribe
                setTimeout(typeLoop, speed);
            }
        }
        
        // Inicia la animación
        typeLoop();
    }
});