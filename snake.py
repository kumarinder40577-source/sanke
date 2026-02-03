import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎮 Cyber-Snake 3D: Sound & FX Edition")
st.write("Controls: **WASD** (Plane), **Q/E** (Vertical). *Click the game area to enable sound!*")

shell_script = """
<div id="game-container" style="width: 100%; height: 600px; background: #000; cursor: crosshair;"></div>
<div id="ui" style="position: absolute; top: 80px; left: 30px; color: #0ff; font-family: 'Orbitron', sans-serif;">
    <h2 id="score-display">SCORE: 000</h2>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>

<script>
    // 1. SOUND ENGINE (Procedural Audio)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    
    function playSound(freq, type, duration) {
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    }

    // 2. SCENE SETUP
    const container = document.getElementById('game-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / 600, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.offsetWidth, 600);
    container.appendChild(renderer.domElement);

    // 3. VISUAL EFFECTS (Bloom-ish Glow)
    const ambientLight = new THREE.AmbientLight(0x404040, 2); 
    scene.add(ambientLight);
    const pointLight = new THREE.PointLight(0x00ffff, 2, 50);
    scene.add(pointLight);

    // 4. GAME OBJECTS
    let snake = [{x: 0, y: 0, z: 0}, {x: -1, y: 0, z: 0}, {x: -2, y: 0, z: 0}];
    let snakeMeshes = [];
    let direction = {x: 1, y: 0, z: 0};
    let foodPos = {x: 5, y: 2, z: 5};
    let score = 0;
    const gridSize = 20;

    // Grid Floor
    const grid = new THREE.GridHelper(gridSize, 20, 0x00ffcc, 0x003333);
    scene.add(grid);

    // Materials
    const snakeMat = new THREE.MeshPhongMaterial({ color: 0x00ffcc, emissive: 0x004444, shininess: 100 });
    const foodMat = new THREE.MeshStandardMaterial({ color: 0xff00ff, emissive: 0x550055 });
    
    const foodMesh = new THREE.Mesh(new THREE.OctahedronGeometry(0.6), foodMat);
    scene.add(foodMesh);

    function createSnakeSegment(pos) {
        const mesh = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.85), snakeMat);
        mesh.position.set(pos.x, pos.y, pos.z);
        scene.add(mesh);
        return mesh;
    }

    function initSnake() {
        snakeMeshes.forEach(m => scene.remove(m));
        snakeMeshes = snake.map(createSnakeSegment);
    }

    function moveFood() {
        foodPos.x = Math.round((Math.random() - 0.5) * 15);
        foodPos.y = Math.round(Math.random() * 5);
        foodPos.z = Math.round((Math.random() - 0.5) * 15);
        foodMesh.position.set(foodPos.x, foodPos.y, foodPos.z);
        playSound(440, 'square', 0.1); // Spawn sound
    }

    // 5. INPUTS
    window.addEventListener('keydown', (e) => {
        const k = e.key.toLowerCase();
        if (k === 'w' && direction.z === 0) direction = {x:0, y:0, z:-1};
        if (k === 's' && direction.z === 0) direction = {x:0, y:0, z:1};
        if (k === 'a' && direction.x === 0) direction = {x:-1, y:0, z:0};
        if (k === 'd' && direction.x === 0) direction = {x:1, y:0, z:0};
        if (k === 'q' && direction.y === 0) direction = {x:0, y:1, z:0};
        if (k === 'e' && direction.y === 0) direction = {x:0, y:-1, z:0};
        playSound(150, 'sine', 0.05); // Move click
    });

    // 6. ANIMATION LOOP
    camera.position.set(15, 15, 15);
    camera.lookAt(0,0,0);
    initSnake();
    moveFood();

    let lastMove = 0;
    function animate(time) {
        requestAnimationFrame(animate);

        // Visual Polish
        foodMesh.rotation.y += 0.05;
        foodMesh.position.y += Math.sin(time * 0.005) * 0.01;
        pointLight.position.copy(snakeMeshes[0].position);

        if (time - lastMove > 180) {
            const head = {...snake[0]};
            head.x += direction.x;
            head.y += direction.y;
            head.z += direction.z;

            // Check Food
            if (head.x === foodPos.x && head.y === foodPos.y && head.z === foodPos.z) {
                score += 10;
                document.getElementById('score-display').innerText = "SCORE: " + score.toString().padStart(3, '0');
                playSound(880, 'triangle', 0.3); // Eat sound
                moveFood();
            } else {
                snake.pop();
            }

            snake.unshift(head);
            
            // Sync Meshes with GSAP for smooth sliding
            snake.forEach((pos, i) => {
                if (!snakeMeshes[i]) snakeMeshes[i] = createSnakeSegment(pos);
                gsap.to(snakeMeshes[i].position, {
                    x: pos.x, y: pos.y, z: pos.z,
                    duration: 0.15,
                    ease: "power2.out"
                });
            });

            lastMove = time;
        }

        // Smooth Camera Follow
        camera.position.lerp(new THREE.Vector3(snake[0].x + 10, snake[0].y + 10, snake[0].z + 10), 0.05);
        camera.lookAt(snake[0].x, snake[0].y, snake[0].z);

        renderer.render(scene, camera);
    }
    animate(0);
</script>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
"""

components.html(shell_script, height=650)
