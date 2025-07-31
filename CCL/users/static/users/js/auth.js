document.addEventListener('DOMContentLoaded', () => {
    // --- LÓGICA PARA FORMULARIO ---
    const formInputs = document.querySelectorAll('.auth-form-side input');
    formInputs.forEach(input => {
        if (input.type !== 'checkbox' && input.type !== 'hidden') {
            input.classList.add('form-control');
            let placeholder = input.name.replace('_', ' ').replace('1', '').replace('2', '');
            placeholder = placeholder.charAt(0).toUpperCase() + placeholder.slice(1);
            if (input.name.includes('password')) placeholder = 'Contraseña';
            input.setAttribute('placeholder', placeholder);
        }
    });

    // --- LÓGICA PARA ANIMACIÓN PLEXUS ---
    const canvas = document.getElementById('plexus-background');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        let particles = [];
        let mouse = { x: null, y: null, radius: 150 };

        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            init();
        });

        window.addEventListener('mousemove', (event) => {
            mouse.x = event.x;
            mouse.y = event.y;
        });

        class Particle {
            constructor(x, y, dirX, dirY, size, color) {
                this.x = x; this.y = y; this.dirX = dirX; this.dirY = dirY;
                this.size = size; this.color = color;
            }
            draw() {
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2, false);
                ctx.fillStyle = 'rgba(255,255,255,0.8)';
                ctx.fill();
            }
            update() {
                if (this.x > canvas.width || this.x < 0) this.dirX = -this.dirX;
                if (this.y > canvas.height || this.y < 0) this.dirY = -this.dirY;
                this.x += this.dirX;
                this.y += this.dirY;
                this.draw();
            }
        }

        function init() {
            particles = [];
            let numParticles = (canvas.height * canvas.width) / 9000;
            for (let i = 0; i < numParticles; i++) {
                let size = (Math.random() * 2) + 1;
                let x = (Math.random() * ((innerWidth - size * 2) - (size * 2)) + size * 2);
                let y = (Math.random() * ((innerHeight - size * 2) - (size * 2)) + size * 2);
                let dirX = (Math.random() * 0.4) - 0.2;
                let dirY = (Math.random() * 0.4) - 0.2;
                particles.push(new Particle(x, y, dirX, dirY, size));
            }
        }

        function connect() {
            for (let a = 0; a < particles.length; a++) {
                for (let b = a; b < particles.length; b++) {
                    let distance = Math.sqrt(
                        (particles[a].x - particles[b].x) * (particles[a].x - particles[b].x) +
                        (particles[a].y - particles[b].y) * (particles[a].y - particles[b].y)
                    );
                    if (distance < (canvas.width / 7) * (canvas.height / 7) / 100) {
                        let opacity = 1 - (distance / 150);
                        ctx.strokeStyle = `rgba(255,193,7,${opacity})`; // Color dorado
                        ctx.lineWidth = 1;
                        ctx.beginPath();
                        ctx.moveTo(particles[a].x, particles[a].y);
                        ctx.lineTo(particles[b].x, particles[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            requestAnimationFrame(animate);
            ctx.clearRect(0, 0, innerWidth, innerHeight);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
            }
            connect();
        }

        init();
        animate();
    }
});
document.addEventListener('DOMContentLoaded', () => {
    
    // --- LÓGICA PARA ANIMACIÓN DE TRIÁNGULOS 3D ---
    const container = document.getElementById('three-background');

    if (container) {
        let scene, camera, renderer, triangles;

        function init() {
            // Escena
            scene = new THREE.Scene();

            // Cámara
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 50;

            // Renderer
            renderer = new THREE.WebGLRenderer({ alpha: true }); // alpha:true para fondo transparente
            renderer.setSize(window.innerWidth, window.innerHeight);
            container.appendChild(renderer.domElement);

            // Geometría de los triángulos
            const geometry = new THREE.BufferGeometry();
            const vertices = [];
            const numTriangles = 100;

            for (let i = 0; i < numTriangles; i++) {
                const x = (Math.random() - 0.5) * 200;
                const y = (Math.random() - 0.5) * 200;
                const z = (Math.random() - 0.5) * 100;
                vertices.push(x, y, z);
            }
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));

            // Material
            const material = new THREE.PointsMaterial({
                color: 0xffc107, // Color dorado
                size: 1.5,
                map: createTriangleTexture(),
                transparent: true,
                opacity: 0.7
            });

            triangles = new THREE.Points(geometry, material);
            scene.add(triangles);

            window.addEventListener('resize', onWindowResize, false);
        }

        function createTriangleTexture() {
            const canvas = document.createElement('canvas');
            canvas.width = 64;
            canvas.height = 64;
            const context = canvas.getContext('2d');
            context.beginPath();
            context.moveTo(32, 5);
            context.lineTo(59, 59);
            context.lineTo(5, 59);
            context.closePath();
            context.fillStyle = 'white';
            context.fill();
            return new THREE.CanvasTexture(canvas);
        }

        function onWindowResize() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }

        function animate() {
            requestAnimationFrame(animate);

            // Animación de rotación
            if (triangles) {
                triangles.rotation.x += 0.0005;
                triangles.rotation.y += 0.0005;
            }

            renderer.render(scene, camera);
        }

        init();
        animate();
    }
});