import streamlit as st
import streamlit.components.v1 as components

st.title("🐍 Animated 3D Snake")
st.write("Controls: **WASD** (Plane), **Q/E** (Depth). Watch for the pulse and particle effects!")

shell_script = """
<div id="game-container" style="width: 100%; height: 500px; background: #111; border-radius: 10px; overflow: hidden;"></div>
<div id="score-display" style="color: #00ff00; font-family: 'Courier New', monospace; font-size: 24px; font-weight: bold; margin-top: 10px;">Score: 0</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>

<script>
    const container = document.getElementById('game-container');
    const scoreElement = document.getElementById('score-display');
    
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x050505);
    
    const camera = new THREE.PerspectiveCamera(75, 800 / 500, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(800, 500);
    container.appendChild(renderer.domElement);

    // Neon Lighting
    const light = new THREE.PointLight(0x00ff00, 1, 100);
    light.position.set(5, 5, 5);
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x222222));

    let snake = [{x: 0, y: 0, z: 0}];
    let snakeMeshes = [];
    let direction = {x: 1, y: 0, z: 0};
    let food = {x: 5, y: 5, z: 0};
    let score = 0;
    const gridSize = 20;

    // Stylish Grid
    const gridHelper = new THREE.GridHelper(gridSize, gridSize, 0x444444, 0x222222);
    scene.add(gridHelper);

    // Geometries
    const boxGeo = new THREE.BoxGeometry(0.8, 0.8, 0.8);
    const snakeMat = new THREE.MeshPhongMaterial({ color: 0x00ff88, emissive: 0x003311 });
    const foodMat = new THREE.MeshPhongMaterial({ color: 0xff0055, emissive: 0x440011 });
    
    let foodMesh = new THREE.Mesh(new THREE.SphereGeometry(0.5, 16, 16), foodMat);
    scene.add(foodMesh);

    function updateSnakeMeshes() {
        snakeMeshes.forEach(m => scene.remove(m));
        snakeMeshes = [];
        snake.forEach((seg, index) => {
            const mesh = new THREE.Mesh(boxGeo, snakeMat);
            mesh.position.set(seg.x, seg.y, seg.z);
            // Scale head slightly larger
            if(index === 0) mesh.scale.set(1.2, 1.2, 1.2);
            scene.add(mesh);
            snakeMeshes.push(mesh);
        });
    }

    function createExplosion(x, y, z) {
        for(let i=0; i<10; i++) {
            const pGeo = new THREE.SphereGeometry(0.1, 4, 4);
            const pMat = new THREE.MeshBasicMaterial({ color: 0xff0055 });
            const p = new THREE.Mesh(pGeo, pMat);
            p.position.set(x, y, z);
            scene.add(p);
            
            gsap.to(p.position, {
                x: x + (Math.random()-0.5)*3,
                y: y + (Math.random()-0.5)*3,
                z: z + (Math.random()-0.5)*3,
                duration: 0.5,
                onComplete: () => scene.remove(p)
            });
        }
    }

    function moveFood() {
        food.x = Math.floor((Math.random() - 0.5) * gridSize);
        food.y = Math.floor((Math.random() - 0.5) * 5); // Keep it relatively low
        food.z = Math.floor((Math.random() - 0.5) * gridSize);
        foodMesh.position.set(food.x, food.y, food.z);
        
        // Pulse animation for new food
        gsap.from(foodMesh.scale, { x: 0, y: 0, z: 0, duration: 0.5, ease: "back.out(1.7)" });
    }

    window.addEventListener('keydown', (e) => {
        const key = e.key.toLowerCase();
        if (key === 'w' && direction.y === 0) direction = {x: 0, y: 1, z: 0};
        if (key === 's' && direction.y === 0) direction = {x: 0, y: -1, z: 0};
        if (key === 'a' && direction.x === 0) direction = {x: -1, y: 0, z: 0};
        if (key === 'd' && direction.x === 0) direction = {x: 1, y: 0, z: 0};
        if (key === 'q' && direction.z === 0) direction = {x: 0, y: 0, z: 1};
        if (key === 'e' && direction.z === 0) direction = {x: 0, y: 0, z: -1};
    });

    camera.position.set(12, 12, 12);
    camera.lookAt(0,0,0);

    let lastTime = 0;
    function animate(time) {
        requestAnimationFrame(animate);
        
        // Subtle food rotation & hover
        foodMesh.rotation.y += 0.05;
        foodMesh.position.y += Math.sin(time * 0.005) * 0.01;

        if (time - lastTime > 150) {
            const newHead = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y,
                z: snake[0].z + direction.z
            };

            if (newHead.x === food.x && newHead.y === food.y && newHead.z === food.z) {
                score += 10;
                scoreElement.innerText = "Score: " + score;
                createExplosion(food.x, food.y, food.z);
                moveFood();
            } else {
                snake.pop();
            }

            snake.unshift(newHead);
            updateSnakeMeshes();
            lastTime = time;
            
            // Camera follow (Smooth lag)
            gsap.to(camera.position, {
                x: newHead.x + 10,
                y: newHead.y + 10,
                z: newHead.z + 10,
                duration: 1
            });
            camera.lookAt(newHead.x, newHead.y, newHead.z);
        }
        renderer.render(scene, camera);
    }
    moveFood();
    animate(0);
</script>
"""

components.html(shell_script, height=600)
