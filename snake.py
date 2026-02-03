import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎮 Cyber-Snake 3D: Tactical Pause")
st.write("Controls: **WASDQE** | Toggle Pause: **Spacebar** or **Button**")

shell_script = """
<div id="game-container" style="width: 100%; height: 600px; background: #000; position: relative;">
    <div id="ui-overlay" style="position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center; background: rgba(0,0,0,0.5); z-index: 10; font-family: 'Orbitron', sans-serif;">
        <h1 id="status-text" style="color: #0ff; text-shadow: 0 0 10px #0ff;">PAUSED</h1>
        <button id="btn-toggle" style="padding: 15px 30px; font-family: 'Orbitron'; background: transparent; border: 2px solid #0ff; color: #0ff; cursor: pointer; font-size: 20px;">RESUME</button>
    </div>
    <div id="score-card" style="position: absolute; top: 20px; left: 20px; color: #0ff; font-family: 'Orbitron'; font-size: 24px; z-index: 5;">SCORE: 000</div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.9.1/gsap.min.js"></script>

<script>
    // 1. GAME STATE
    let isRunning = false;
    const uiOverlay = document.getElementById('ui-overlay');
    const btnToggle = document.getElementById('btn-toggle');
    const statusText = document.getElementById('status-text');

    function toggleGame() {
        isRunning = !isRunning;
        uiOverlay.style.display = isRunning ? 'none' : 'flex';
        btnToggle.innerText = isRunning ? 'PAUSE' : 'RESUME';
        statusText.innerText = 'PAUSED';
        playSound(isRunning ? 600 : 300, 'sine', 0.1);
    }

    btnToggle.onclick = toggleGame;

    // 2. SOUND ENGINE
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

    // 3. THREE.JS SETUP
    const container = document.getElementById('game-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, container.offsetWidth / 600, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.offsetWidth, 600);
    container.appendChild(renderer.domElement);

    const pointLight
