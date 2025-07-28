document.addEventListener('DOMContentLoaded', () => {
    // Asegúrate de que la función tsParticles esté disponible
    if (typeof tsParticles === 'undefined') {
        console.error('Error: tsParticles library not loaded.');
        return;
    }

    tsParticles.load({
        id: "tsparticles", // El ID del div que creamos en el HTML
        options: {
            // --- Apariencia General ---
            background: {
                color: {
                    value: 'transparent' // El fondo es transparente para que se vea el de la web
                }
            },
            particles: {
                // --- Partículas (Puntos Dorados) ---
                number: {
                    value: 80, // Cantidad de partículas. No demasiadas para no sobrecargar.
                    density: {
                        enable: true,
                    }
                },
                color: {
                    value: "#B48314" // Nuestro color dorado
                },
                shape: {
                    type: "circle"
                },
                opacity: {
                    value: { min: 0.3, max: 0.8 } // Opacidad variable para un look más orgánico
                },
                size: {
                    value: { min: 1, max: 3 } // Tamaño variable y pequeño
                },
                // --- Líneas que conectan las partículas ---
                links: {
                    color: "#B48314",
                    distance: 150,
                    enable: true,
                    opacity: 0.2, // Muy sutiles para no distraer
                    width: 1
                },
                // --- Movimiento de las partículas ---
                move: {
                    enable: true,
                    speed: 1, // Movimiento lento y elegante
                    direction: "none",
                    outModes: {
                        default: "out"
                    }
                }
            },
            // --- Interactividad con el Cursor ---
            interactivity: {
                events: {
                    onHover: {
                        enable: true,
                        mode: "repulse" // El cursor "empuja" las partículas, creando una reacción elegante
                    },
                    onClick: {
                        enable: true,
                        mode: "push" // Al hacer clic, se añaden nuevas partículas
                    }
                },
                modes: {
                    repulse: {
                        distance: 100 // Distancia de la reacción al cursor
                    },
                    push: {
                        quantity: 4 // Cuántas partículas añadir al hacer clic
                    }
                }
            },
            detectRetina: true
        }
    });
});