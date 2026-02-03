import streamlit as st
import streamlit.components.v1 as components

st.title("3D Snake Game")
st.write("Use **WASD** to move on the plane and **Q/E** to move through depth!")

# We wrap your existing shell_script logic into Streamlit's component system
shell_script = """
<div id="game-container" style="width: 100%; height: 500px; background: #000;"></div>
<div id="score-display" style="color: white; font-family: sans-serif; font-size: 20px; margin-top: 10px;">Score: 0</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
    const container = document.getElementById('game-container');
    const scoreElement = document.getElementById('score-display');
    
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 800 / 500, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(800, 500);
    container.appendChild(renderer.domElement);

    const light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(5, 5, 5).normalize();
    scene.add(light);
    scene.add(new THREE.AmbientLight(0x404040));

    let snake = [{x: 0, y: 0, z: 0}];
    let snakeMeshes = [];
    let direction = {x: 1, y: 0, z: 0};
    let food = {x: 5, y: 5, z: 0};
    let score = 0;
    const gridSize = 20;

    const gridHelper = new THREE.GridHelper(gridSize, gridSize);
    scene.add(gridHelper);

    const boxGeo = new THREE.BoxGeometry(0.9, 0.9, 0.9);
    const snakeMat = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
    const foodMat = new THREE.MeshPhongMaterial({ color: 0xff0000 });
    
    let foodMesh = new THREE.Mesh(boxGeo, foodMat);
    scene.add(foodMesh);

    function updateSnakeMeshes() {
        snakeMeshes.forEach(m => scene.remove(m));
        snakeMeshes = [];
        snake.forEach(seg => {
            const mesh = new THREE.Mesh(boxGeo, snakeMat);
            mesh.position.set(seg.x, seg.y, seg.z);
            scene.add(mesh);
            snakeMeshes.push(mesh);
        });
    }

    function moveFood() {
        food.x = Math.floor((Math.random() - 0.5) * gridSize);
        food.y = Math.floor((Math.random() - 0.5) * gridSize);
        foodMesh.position.set(food.x, food.y, food.z);
    }

    window.addEventListener('keydown', (e) => {
        switch(e.key.toLowerCase()) {
            case 'w': direction = {x: 0, y: 1, z: 0}; break;
            case 's': direction = {x: 0, y: -1, z: 0}; break;
            case 'a': direction = {x: -1, y: 0, z: 0}; break;
            case 'd': direction = {x: 1, y: 0, z: 0}; break;
            case 'q': direction = {x: 0, y: 0, z: 1}; break;
            case 'e': direction = {x: 0, y: 0, z: -1}; break;
        }
    });

    camera.position.z = 15;
    camera.position.y = 10;
    camera.lookAt(0,0,0);

    let lastTime = 0;
    function animate(time) {
        requestAnimationFrame(animate);
        if (time - lastTime > 200) {
            const newHead = {
                x: snake[0].x + direction.x,
                y: snake[0].y + direction.y,
                z: snake[0].z + direction.z
            };

            if (newHead.x === food.x && newHead.y === food.y && newHead.z === food.z) {
                score += 10;
                scoreElement.innerText = "Score: " + score;
                moveFood();
            } else {
                snake.pop();
            }

            snake.unshift(newHead);
            updateSnakeMeshes();
            lastTime = time;
        }
        renderer.render(scene, camera);
    }
    moveFood();
    animate(0);
</script>
"""

# This renders the code in your Streamlit app
components.html(shell_script, height=600)
