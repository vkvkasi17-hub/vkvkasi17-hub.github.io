// --- CUSTOM CURSOR ---
const cursor = document.getElementById('customCursor');
let mouseX = window.innerWidth/2; let mouseY = window.innerHeight/2;
document.addEventListener('mousemove', (e) => {
mouseX = e.clientX; mouseY = e.clientY;
cursor.style.left = mouseX + 'px'; cursor.style.top = mouseY + 'px';
});
document.querySelectorAll('a, button, input, textarea, .filter-btn').forEach(el => {
el.addEventListener('mouseenter', () => cursor.classList.add('hovering'));
el.addEventListener('mouseleave', () => cursor.classList.remove('hovering'));
});

// --- SKILL BUBBLE POP & RETURN INTERACTION ---
document.querySelectorAll('.skill-tag').forEach(tag => {
tag.addEventListener('click', function() {
if(this.classList.contains('popped')) return;
this.classList.add('popped');
setTimeout(() => { this.classList.remove('popped'); }, 1000);
});
});

// --- BOOK PAGE TURN OBSERVER ---
const pages = document.querySelectorAll('.book-page');
const observer = new IntersectionObserver((entries) => {
entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('page-open'); } });
}, { threshold: 0.1 });
pages.forEach(page => observer.observe(page));

// --- THEME TOGGLE ---
const themeToggleBtn = document.getElementById('themeToggle');
if (localStorage.getItem('portfolio-theme') === 'dark') {
document.body.classList.add('dark-mode'); themeToggleBtn.querySelector('i').classList.replace('fa-moon', 'fa-sun');
}
themeToggleBtn.addEventListener('click', () => {
document.body.classList.toggle('dark-mode'); const icon = themeToggleBtn.querySelector('i');
if (document.body.classList.contains('dark-mode')) { localStorage.setItem('portfolio-theme', 'dark'); icon.classList.replace('fa-moon', 'fa-sun'); }
else { localStorage.setItem('portfolio-theme', 'light'); icon.classList.replace('fa-sun', 'fa-moon'); }
});

// --- TYPEWRITER ---
const titles = ["Python Developer", "Generative AI Engineer", "Backend Specialist", "Data Engineer", "Python Developer | Generative AI | Backend Engineer"];
let countText = 0; let index = 0; let currentText = ''; let letter = ''; let isDeleting = false;
function type() {
if (countText === titles.length) countText = 0;
currentText = titles[countText];
if (isDeleting) letter = currentText.slice(0, --index); else letter = currentText.slice(0, ++index);
document.getElementById('typewriter').textContent = letter;
let typeSpeed = isDeleting ? 30 : 70;
if (!isDeleting && letter.length === currentText.length) { typeSpeed = 2000; isDeleting = true; }
else if (isDeleting && letter.length === 0) { isDeleting = false; countText++; typeSpeed = 500; }
setTimeout(type, typeSpeed);
}
document.addEventListener("DOMContentLoaded", type);

// --- DRAGGABLE RACE CAR SCROLLBAR ---
const raceCar = document.getElementById('raceCar');
const raceTrack = document.getElementById('raceTrack');
let isDraggingCar = false;

function handleCarDrag(yPos) {
const trackHeight = raceTrack.offsetHeight;
let y = Math.max(0, Math.min(yPos, trackHeight));
const scrollPercent = y / trackHeight;
const docHeight = document.documentElement.scrollHeight - window.innerHeight;
window.scrollTo({ top: scrollPercent * docHeight, behavior: 'instant' });
}
raceTrack.addEventListener('mousedown', (e) => {
isDraggingCar = true; document.body.classList.add('is-dragging-car');
document.body.style.userSelect = 'none'; handleCarDrag(e.clientY);
});
window.addEventListener('mouseup', () => { isDraggingCar = false; document.body.classList.remove('is-dragging-car'); document.body.style.userSelect = ''; });
window.addEventListener('mousemove', (e) => { if (isDraggingCar) handleCarDrag(e.clientY); });
raceTrack.addEventListener('touchstart', (e) => {
isDraggingCar = true; document.body.classList.add('is-dragging-car'); handleCarDrag(e.touches[0].clientY);
}, {passive: true});
window.addEventListener('touchend', () => { isDraggingCar = false; document.body.classList.remove('is-dragging-car'); });
window.addEventListener('touchmove', (e) => { if (isDraggingCar) handleCarDrag(e.touches[0].clientY); }, {passive: true});

let lastScrollY = window.scrollY;
let hasCelebrated = false;
let closeTimeout;

// Global tracking for 3D Camera scroll interaction
let currentScrollY = 0;

function closeModal() {
document.getElementById('celebrationModal').classList.remove('show');
document.getElementById('modalProgressBar').classList.remove('animate');
clearTimeout(closeTimeout);
}

// --- MASTER SCROLL CONTROLLER ---
window.addEventListener('scroll', () => {
currentScrollY = window.scrollY; // Saves scroll for the 3D loop

const docHeight = document.documentElement.scrollHeight - window.innerHeight;
const heroHeight = window.innerHeight;

if (currentScrollY <= 5) { document.body.classList.add('at-top'); } else { document.body.classList.remove('at-top'); }
if (currentScrollY > heroHeight * 0.2) { document.body.classList.add('past-hero'); document.body.classList.remove('in-hero'); }
else { document.body.classList.add('in-hero'); document.body.classList.remove('past-hero'); }
if (currentScrollY > lastScrollY) { raceCar.style.transform = 'translateX(-50%) rotate(-90deg)'; }
else if (currentScrollY < lastScrollY) { raceCar.style.transform = 'translateX(-50%) rotate(90deg)'; }
lastScrollY = currentScrollY;

if (!isDraggingCar) { raceCar.style.top = `${(currentScrollY / docHeight) * 95}%`; }
const navbar = document.getElementById('navbar');
if (currentScrollY > 20) { navbar.classList.add('scrolled'); } else { navbar.classList.remove('scrolled'); }

if (!hasCelebrated && currentScrollY >= docHeight - 50 && docHeight > 100 && currentScrollY > 500) {
hasCelebrated = true;
var duration = 3000; var end = Date.now() + duration;
(function frame() {
confetti({ particleCount: 7, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#4299e1', '#48bb78', '#df9e38'] });
confetti({ particleCount: 7, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#4299e1', '#48bb78', '#df9e38'] });
if (Date.now() < end) { requestAnimationFrame(frame); }
}());
setTimeout(() => {
document.getElementById('celebrationModal').classList.add('show');
document.getElementById('modalProgressBar').classList.add('animate');
closeTimeout = setTimeout(() => { closeModal(); }, 5000);
}, 500);
}
});
window.dispatchEvent(new Event('scroll'));

// --- PREDICTIVE RPS LOGIC ---
const userScoreEl = document.getElementById('userScore'); const aiScoreEl = document.getElementById('aiScore'); const gameLog = document.getElementById('gameLog');
let uScore = 0; let aScore = 0; let lastUserMove = null;
const history = { 'rock': { 'rock': 0, 'paper': 0, 'scissors': 0 }, 'paper': { 'rock': 0, 'paper': 0, 'scissors': 0 }, 'scissors': { 'rock': 0, 'paper': 0, 'scissors': 0 } };
const moves = ['rock', 'paper', 'scissors']; const beats = { 'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper' }; const losesTo = { 'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock' }; const emojis = { 'rock': '✊', 'paper': '✋', 'scissors': '✌️' };
function playRPS(userMove) {
let aiMove = moves[Math.floor(Math.random() * 3)];
if (lastUserMove) {
let maxCount = -1; let predictedMove = 'rock';
for (const m of moves) { if (history[lastUserMove][m] > maxCount) { maxCount = history[lastUserMove][m]; predictedMove = m; } }
if (maxCount > 0) aiMove = losesTo[predictedMove];
}
if (lastUserMove) history[lastUserMove][userMove]++;
lastUserMove = userMove;
let resultText = ''; let resultColor = '';
if (userMove === aiMove) { resultText = "It's a Tie!"; resultColor = "var(--text-muted)"; }
else if (beats[userMove] === aiMove) { resultText = "You Win! 🎉"; resultColor = "var(--accent)"; uScore++; }
else { resultText = "AI Wins! 🤖"; resultColor = "#fc8181"; aScore++; }
userScoreEl.innerText = uScore; aiScoreEl.innerText = aScore;
gameLog.innerHTML = `<div style="font-size: 1.1rem; color: var(--text-main); margin-bottom: 15px;">You <span style="font-size: 2.5rem; margin: 0 15px;">${emojis[userMove]}</span> <span style="color: var(--text-muted);">vs</span> <span style="font-size: 2.5rem; margin: 0 15px;">${emojis[aiMove]}</span> AI</div><div style="font-weight: bold; font-size: 1.3rem; color: ${resultColor};">${resultText}</div>`;
}
function filterProjects(category) {
document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active')); event.target.classList.add('active');
document.querySelectorAll('.new-project-card').forEach(project => { if (category === 'all' || project.dataset.category === category) project.classList.remove('project-hidden'); else project.classList.add('project-hidden'); });
}

// ==========================================
// --- MODALS & HOVER PREVIEWS ---
// ==========================================

document.addEventListener("DOMContentLoaded", () => {
const certItems = document.querySelectorAll('.cert-item');
const previewImg = document.getElementById('hover-preview-img');

if (previewImg) {
certItems.forEach(item => {
item.addEventListener('mouseenter', (e) => {
const imgSrc = item.getAttribute('data-img');
if (imgSrc) {
previewImg.src = imgSrc;
previewImg.style.display = 'block';
}
});

item.addEventListener('mousemove', (e) => {
previewImg.style.left = (e.pageX + 15) + 'px';
previewImg.style.top = (e.pageY + 15) + 'px';
});

item.addEventListener('mouseleave', () => {
previewImg.style.display = 'none';
previewImg.src = '';
});
});
}

const modal = document.getElementById("project-modal");
if (modal) {
const closeBtn = modal.querySelector(".project-close-btn");
const projectCards = document.querySelectorAll(".modal-trigger");

projectCards.forEach(card => {
card.addEventListener("click", () => {
const title = card.getAttribute("data-title");
const tech = card.getAttribute("data-tech");
const overview = card.getAttribute("data-overview");
const github = card.getAttribute("data-github");
const website = card.getAttribute("data-website");

if (overview || github || website) {
document.getElementById("modal-title").innerText = title || "Project Details";
document.getElementById("modal-tech").innerText = tech || "";
document.getElementById("modal-overview").innerHTML = overview || "No expanded overview available.";

const githubBtn = document.getElementById("modal-github");
if (github) {
githubBtn.href = github;
githubBtn.style.display = "inline-block";
} else {
githubBtn.style.display = "none";
}

const websiteBtn = document.getElementById("modal-website");
if (website) {
websiteBtn.href = website;
websiteBtn.style.display = "inline-block";
} else {
websiteBtn.style.display = "none";
}

modal.style.display = "block";
document.body.style.overflow = "hidden";
}
});
});

const closeModal = () => {
modal.style.display = "none";
document.body.style.overflow = "";
};

if (closeBtn) closeBtn.addEventListener("click", closeModal);
window.addEventListener("click", (event) => {
if (event.target === modal) {
closeModal();
}
});
}
});

// ==========================================
// --- IMMERSIVE NEURAL LANDSCAPE ENGINE ---
// ==========================================
window.addEventListener('DOMContentLoaded', () => {
if (typeof THREE === 'undefined' || !document.getElementById('llm-3d-bg')) return;

const bgContainer = document.getElementById('llm-3d-bg');
const scene = new THREE.Scene();

// Setup dynamic fog to hide the edges of the terrain and create depth
const colorLight = new THREE.Color(0xf8fafc);
const colorDark = new THREE.Color(0x0b0f19);
const initialFogColor = document.body.classList.contains('dark-mode') ? colorDark : colorLight;
scene.fog = new THREE.FogExp2(initialFogColor, 0.0015);

// Setup the camera deeply inside the terrain for an immersive feel
const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 4000);
const baseCameraZ = 800;
const baseCameraY = 120;
camera.position.set(0, baseCameraY, baseCameraZ);

const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio);
bgContainer.appendChild(renderer.domElement);

// Create a MASSIVE terrain plane (4000x4000) to fill the entire screen space
const geometry = new THREE.PlaneGeometry(4000, 4000, 160, 160);
geometry.rotateX(-Math.PI / 2); // Lay it flat like a floor

const positions = geometry.attributes.position.array;
const colors = new Float32Array(positions.length);
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

// Theme Colors
const color1 = new THREE.Color('#306998'); // Python Blue
const color2 = new THREE.Color('#00E5FF'); // AI Cyan
const color3 = new THREE.Color('#48BB78'); // Data Green
const color4 = new THREE.Color('#FFE873'); // Python Yellow

// Pre-calculate heights and colors
for (let i = 0; i < positions.length; i += 3) {
const x = positions[i];
const z = positions[i + 2];
// Complex mathematical noise to create realistic terrain mountains/valleys
const y = Math.sin(x * 0.0015) * Math.cos(z * 0.0015) * 200 +
Math.sin(x * 0.005) * Math.cos(z * 0.005) * 50;
positions[i + 1] = y;

// Map colors based on the elevation (y-axis)
let mixRatio = (y + 250) / 500;
mixRatio = Math.max(0, Math.min(1, mixRatio));

let finalColor = new THREE.Color();
if (mixRatio < 0.33) {
finalColor.lerpColors(color1, color2, mixRatio / 0.33);
} else if (mixRatio < 0.66) {
finalColor.lerpColors(color2, color3, (mixRatio - 0.33) / 0.33);
} else {
finalColor.lerpColors(color3, color4, (mixRatio - 0.66) / 0.34);
}

colors[i] = finalColor.r;
colors[i + 1] = finalColor.g;
colors[i + 2] = finalColor.b;
}

// Material 1: The glowing particles
const canvas = document.createElement('canvas');
canvas.width = 32; canvas.height = 32;
const context = canvas.getContext('2d');
context.beginPath();
context.arc(16, 16, 14, 0, Math.PI * 2);
context.fillStyle = '#ffffff';
context.fill();
const texture = new THREE.CanvasTexture(canvas);

const pointMaterial = new THREE.PointsMaterial({
size: 5,
map: texture,
vertexColors: true,
transparent: true,
opacity: 0.9,
alphaTest: 0.1
});
const points = new THREE.Points(geometry, pointMaterial);
scene.add(points);

// Material 2: The high-tech cyber wireframe
const wireframeMaterial = new THREE.LineBasicMaterial({
vertexColors: true,
transparent: true,
opacity: 0.15
});
const wireframe = new THREE.LineSegments(new THREE.WireframeGeometry(geometry), wireframeMaterial);
scene.add(wireframe);

// Mouse tracking for slight panning
let targetXMouse = 0;
let targetYMouse = 0;
let windowHalfX = window.innerWidth / 2;
let windowHalfY = window.innerHeight / 2;

document.addEventListener('mousemove', (event) => {
targetXMouse = event.clientX - windowHalfX;
targetYMouse = event.clientY - windowHalfY;
});

window.addEventListener('resize', () => {
windowHalfX = window.innerWidth / 2;
windowHalfY = window.innerHeight / 2;
camera.aspect = window.innerWidth / window.innerHeight;
camera.updateProjectionMatrix();
renderer.setSize(window.innerWidth, window.innerHeight);
});

// Smooth scroll tracker
let smoothedScrollY = 0;
let clock = 0;

function animate() {
requestAnimationFrame(animate);
clock += 0.01; // Internal time for continuous flowing animation

// Smoothly interpolate the global window scroll
smoothedScrollY += (currentScrollY - smoothedScrollY) * 0.1;
const maxScroll = (document.documentElement.scrollHeight - window.innerHeight) || 1;
const scrollPercent = smoothedScrollY / maxScroll;

// 3D CINEMATIC MOVEMENT
// The camera physically flies forward up to 2500 pixels deep into the landscape
const targetCamZ = baseCameraZ - (scrollPercent * 2500);
// The camera dips slightly as it flies forward to stay close to the data surface
const targetCamY = baseCameraY - (scrollPercent * 80);

// Blend Mouse interaction with Scroll interaction
camera.position.x += (targetXMouse * 0.5 - camera.position.x) * 0.05;
camera.position.y += (-(targetYMouse * 0.2) + targetCamY - camera.position.y) * 0.05;
camera.position.z += (targetCamZ - camera.position.z) * 0.05;
// Always look straight ahead to see the fog/horizon
camera.lookAt(camera.position.x, camera.position.y - 50, camera.position.z - 500);

// Continuously undulate the terrain to make it feel alive
const pos = geometry.attributes.position.array;
for (let i = 0; i < pos.length; i += 3) {
const x = pos[i];
const z = pos[i + 2];
pos[i + 1] = Math.sin(x * 0.0015 + clock * 0.5) * Math.cos(z * 0.0015 + clock * 0.5) * 200 +
Math.sin(x * 0.005 - clock * 0.3) * Math.cos(z * 0.005 - clock * 0.3) * 50;
}
geometry.attributes.position.needsUpdate = true;

// Smoothly adapt the 3D fog color when the user changes Light/Dark modes!
const targetFogColor = document.body.classList.contains('dark-mode') ? colorDark : colorLight;
scene.fog.color.lerp(targetFogColor, 0.05);

renderer.render(scene, camera);
}

animate();
});