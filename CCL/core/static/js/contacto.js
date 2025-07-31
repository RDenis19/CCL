document.addEventListener('DOMContentLoaded', () => {
    const particlesContainer = document.getElementById('particles-hero');

    if (particlesContainer) {
        tsParticles.load(particlesContainer, {
            fpsLimit: 60,
            interactivity: {
                events: {
                    onClick: { enable: false, mode: "push" },
                    onHover: { enable: true, mode: "repulse" },
                    resize: true,
                },
                modes: {
                    push: { quantity: 4 },
                    repulse: { distance: 100, duration: 0.4 },
                },
            },
            particles: {
                color: { value: "#ffffff" },
                move: {
                    direction: "none",
                    enable: true,
                    outModes: { default: "bounce" },
                    random: true,
                    speed: 0.5,
                    straight: false,
                },
                number: { density: { enabled: true, area: 800 }, value: 80 },
                opacity: { value: 0.5 },
                shape: { type: "circle" },
                size: { value: { min: 1, max: 3 } },
            },
            detectRetina: true,
        });
    }
});