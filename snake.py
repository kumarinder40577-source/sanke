import streamlit as st
import streamlit.components.v1 as components

# 1. Setup Streamlit Page
st.set_page_config(layout="wide", page_title="3D Cyber Snake")
st.title("🎮 Cyber-Snake 3D")
st.write("Controls: **WASDQE** | **Spacebar** to Play/Pause")

# 2. The Game Script (HTML/JavaScript)
# I have fixed the triple-quote syntax error here
shell_script = """
<div id="game-container" style="width: 100%; height: 600px; background: #000; position: relative; border-radius: 15px; border: 2px solid #0ff;">
    <div id="ui-overlay" style="position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.7); z-index: 10; font-family: 'Orbitron', sans-serif;">
        <h1 id="status-text" style="color: #0ff; text-shadow: 0 0 10px #0ff; margin-bottom: 20px;">READY?</h1>
        <button id="btn-toggle" style="padding: 15px 40px; font-family: 'Orbitron'; background: transparent; border: 2px solid #0ff; color: #0ff; cursor: pointer; font-size: 20px; transition: 0.3s;">START GAME</button>
    </div>
    <div id="score-card" style="position: absolute; top: 20px; left: 20px; color: #0ff; font-family: 'Orbitron'; font-size: 24px; z-index: 5; text-shadow: 0 0 5px #0ff;">SCORE: 000</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>

<script>
    let isRunning = false;
    let isGameOver = false;
    const uiOverlay = document.getElementById('ui-overlay');
    const btnToggle = document.getElementById('btn-toggle');
    const statusText = document.getElementById('status-text');
    const scoreCard = document.getElementById('score-card');

    // --- AUDIO SYSTEM ---
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

    // --- THREE.JS SETUP ---
    const container = document.getElementById('game-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / 600, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.offsetWidth, 600);
    container.appendChild(renderer.domElement);

    const pointLight = new THREE.PointLight(0x00ffff, 2, 50);
    scene.add(pointLight);
    scene.add(new THREE.AmbientLight(0x404040, 2));

    // --- GAME LOGIC ---
    let snake = [{x: 0, y: 0, z: 0}, {x: -1, y: 0, z: 0}];
    let snakeMeshes = [];
    let direction = {x: 1, y: 0, z: 0};
    let foodPos = {x: 5, y: 0, z: 5};
    let score = 0;
    const gridSize = 20;

    const grid = new THREE.GridHelper(gridSize, 20, 0x00ffcc, 0x003333);
    scene.add(grid);

    const snakeMat = new THREE.MeshPhongMaterial({ color: 0x00ffcc, emissive: 0x002222 });
    const foodMesh = new THREE.Mesh(new THREE.OctahedronGeometry(0.6), new THREE.MeshStandardMaterial({ color: 0xff00ff, emissive: 0x550055 }));
    scene.add(foodMesh);

    function syncMeshes() {
        snakeMeshes.forEach(m => scene.remove(m));
        snakeMeshes = snake.map(pos => {
            const m = new THREE.Mesh(new THREE.BoxGeometry(0.85, 0.85, 0.85), snakeMat);
            m.position.set(pos.x, pos.y, pos.z);
            scene.add(m);
            return m;
        });
    }

    function resetGame() {
        snake = [{x: 0, y: 0, z: 0}, {x: -1, y: 0, z: 0}];
        direction = {x: 1, y: 0, z: 0};
        score = 0;
        scoreCard.innerText = "SCORE: 000";
        isGameOver = false;
        statusText.innerText = "PAUSED";
        btnToggle.innerText = "RESUME";
        syncMeshes();
    }

    function toggleGame() {
        if(isGameOver) {
            resetGame();
            return;
        }
        isRunning = !isRunning;
        uiOverlay.style.display = isRunning ? 'none' : 'flex';
        btnToggle.innerText = isRunning ? 'PAUSE' : 'RESUME';
        statusText.innerText = 'PAUSED';
        playSound(isRunning ? 600 : 300, 'sine', 0.1);
    }

    btnToggle.onclick = toggleGame;

    window.addEventListener('keydown', (e) => {
        if (e.code === 'Space') { toggleGame(); return; }
        if (!isRunning) return;

        const k = e.key.toLowerCase();
        if (k === 'w' && direction.z === 0) direction = {x:0, y:0, z:-1};
        if (k === 's' && direction.z === 0) direction = {x:0, y:0, z:1};
        if (k === 'a' && direction.x === 0) direction = {x:-1, y:0, z:0};
        if (k === 'd' && direction.x === 0) direction = {x:1, y:0, z:0};
        if (k === 'q' && direction.y === 0) direction = {x:0, y:1, z:0};
        if (k === 'e' && direction.y === 0) direction = {x:0, y:-1, z:0};
    });

    camera.position.set(12, 12, 12);
    syncMeshes();
    
    let lastMove = 0;
    function animate(time) {
        requestAnimationFrame(animate);

        if (isRunning && !isGameOver) {
            foodMesh.rotation.y += 0.05;
            
            if (time - lastMove > 180) {
                const head = {...snake[0]};
                head.x += direction.x; head.y += direction.y; head.z += direction.z;

                // Boundary/Self Collision Check
                const hitSelf = snake.some(s => s.x === head.x && s.y === head.y && s.z === head.z);
                const outBounds = Math.abs(head.x) > 10 || Math.abs(head.z) > 10 || head.y < 0 || head.y > 10;

                if (hitSelf || outBounds) {
                    isGameOver = true;
                    isRunning = false;
                    uiOverlay.style.display = 'flex';
                    statusText.innerText = "GAME OVER";
                    btnToggle.innerText = "RESTART";
                    playSound(150, 'sawtooth', 0.5);
                    return;
                }

                if (head.x === foodPos.x && head.y === foodPos.y && head.z === foodPos.z) {
                    score += 10;
                    scoreCard.innerText = "SCORE: " + score.toString().padStart(3, '0');
                    playSound(880, 'triangle', 0.2);
                    foodPos = {x: Math.round((Math.random()-0.5)*18), y: Math.round(Math.random()*5), z: Math.round((Math.random()-0.5)*18)};
                    foodMesh.position.set(foodPos.x, foodPos.y, foodPos.z);
                } else {
                    snake.pop();
                }

                snake.unshift(head);
                syncMeshes();
                lastMove = time;
            }
            camera.position.lerp(new THREE.Vector3(snake[0].x+12, snake[0].y+12, snake[0].z+12), 0.05);
            camera.lookAt(snake[0].x, snake[0].y, snake[0].z);
            pointLight.position.copy(snakeMeshes[0].position);
        }
        renderer.render(scene, camera);
    }
    animate(0);
</script>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap" rel="stylesheet">
"""

# 3. Render the Component
components.html(shell_script, height=650)
