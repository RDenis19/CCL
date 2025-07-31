const canvas = document.createElement('canvas');
canvas.id = 'background-canvas';
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');
let w, h;
let particles = [];

function resizeCanvas() {
    w = canvas.width = window.innerWidth;
    h = canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

for (let i = 0; i < 60; i++) {
    particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.5,
        vy: (Math.random() - 0.5) * 0.5
    });
}

function draw() {
    ctx.clearRect(0, 0, w, h);
    for (let i = 0; i < particles.length; i++) {
        let p = particles[i];
        ctx.beginPath();
        ctx.arc(p.x, p.y, 2, 0, Math.PI * 2);
        ctx.fillStyle = '#c9a337';
        ctx.fill();
        p.x += p.vx;
        p.y += p.vy;

        // Rebote
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;

        // Líneas
        for (let j = i + 1; j < particles.length; j++) {
            let p2 = particles[j];
            let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < 120) {
                ctx.beginPath();
                ctx.strokeStyle = 'rgba(201, 163, 55, 0.2)';
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }
    }
    requestAnimationFrame(draw);
}

draw();