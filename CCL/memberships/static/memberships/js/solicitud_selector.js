// Solo opcional, podrías agregar partículas u otras animaciones en el fondo.
// Aquí mantenemos un fondo animado sencillo:
document.addEventListener("DOMContentLoaded", function () {
    const bg = document.createElement("div");
    bg.style.position = "fixed";
    bg.style.top = 0;
    bg.style.left = 0;
    bg.style.width = "100%";
    bg.style.height = "100%";
    bg.style.zIndex = -1;
    bg.style.background = "radial-gradient(circle at center, rgba(255, 245, 200, 0.05), transparent 60%)";
    bg.style.animation = "pulse 6s ease-in-out infinite";
    document.body.appendChild(bg);
});
