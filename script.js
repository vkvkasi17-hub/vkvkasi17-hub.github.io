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
let count = 0; let index = 0; let currentText = ''; let letter = ''; let isDeleting = false;
function type() {
    if (count === titles.length) count = 0;
    currentText = titles[count];
    if (isDeleting) letter = currentText.slice(0, --index); else letter = currentText.slice(0, ++index);
    document.getElementById('typewriter').textContent = letter;
    let typeSpeed = isDeleting ? 30 : 70;
    if (!isDeleting && letter.length === currentText.length) { typeSpeed = 2000; isDeleting = true; } 
    else if (isDeleting && letter.length === 0) { isDeleting = false; count++; typeSpeed = 500; }
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

// --- HERO NEURAL NETWORK LOGIC ---
const netCanvas = document.getElementById('networkCanvas');
const netCtx = netCanvas.getContext('2d');
let netW = netCanvas.width = window.innerWidth;
let netH = netCanvas.height = window.innerHeight;
const netParticles = [];
for(let i=0; i<80; i++) {
    netParticles.push({
        x: Math.random() * netW, y: Math.random() * netH,
        vx: (Math.random()-0.5)*0.5, vy: (Math.random()-0.5)*0.5, radius: Math.random()*2+1
    });
}
function animateNet() {
    if(document.body.classList.contains('in-hero')) {
        netCtx.clearRect(0,0,netW,netH);
        const isDark = document.body.classList.contains('dark-mode');
        const dotColor = isDark ? 'rgba(99,179,237,0.6)' : 'rgba(43,108,176,0.3)';
        const lineRGB = isDark ? '99,179,237' : '43,108,176';
        
        for(let i=0; i<netParticles.length; i++) {
            let p = netParticles[i];
            p.x += p.vx; p.y += p.vy;
            if(p.x<0) p.x=netW; if(p.x>netW) p.x=0;
            if(p.y<0) p.y=netH; if(p.y>netH) p.y=0;
            
            netCtx.beginPath(); netCtx.arc(p.x, p.y, p.radius, 0, Math.PI*2);
            netCtx.fillStyle = dotColor; netCtx.fill();
            
            for(let j=i+1; j<netParticles.length; j++) {
                let p2 = netParticles[j];
                let dx = p.x-p2.x, dy = p.y-p2.y;
                let dist = Math.sqrt(dx*dx+dy*dy);
                if(dist < 120) {
                    netCtx.beginPath(); netCtx.strokeStyle = `rgba(${lineRGB},${0.2*(1-dist/120)})`;
                    netCtx.lineWidth=0.8; netCtx.moveTo(p.x,p.y); netCtx.lineTo(p2.x,p2.y); netCtx.stroke();
                }
            }
            let dxM = p.x - mouseX, dyM = p.y - mouseY;
            let distM = Math.sqrt(dxM*dxM + dyM*dyM);
            if(distM < 150) {
                netCtx.beginPath(); netCtx.strokeStyle = `rgba(${lineRGB},${0.4*(1-distM/150)})`;
                netCtx.lineWidth=1; netCtx.moveTo(p.x,p.y); netCtx.lineTo(mouseX,mouseY); netCtx.stroke();
            }
        }
    }
    requestAnimationFrame(animateNet);
}
animateNet();

// --- WEATHER ENGINE (RAIN & SPLASH) LOGIC ---
const rainCanvas = document.getElementById('rainCanvas');
const ctx = rainCanvas.getContext('2d');
let width = rainCanvas.width = window.innerWidth;
let height = rainCanvas.height = window.innerHeight;
window.addEventListener('resize', () => { 
    width = rainCanvas.width = window.innerWidth; height = rainCanvas.height = window.innerHeight; 
    netW = netCanvas.width = window.innerWidth; netH = netCanvas.height = window.innerHeight;
});

const drops = []; const splashes = []; 
for(let i=0; i<350; i++) {
    drops.push({
        x: Math.random() * width, y: Math.random() * height,
        speed: Math.random() * 5 + 3, length: Math.random() * 20 + 10, 
        thickness: Math.random() * 1.5 + 0.8, opacity: Math.random() * 0.5 + 0.2
    });
}

let lastScrollY = window.scrollY;
let weatherTimeout;
let hasCelebrated = false;
let closeTimeout;

function closeModal() { 
    document.getElementById('celebrationModal').classList.remove('show'); 
    document.getElementById('modalProgressBar').classList.remove('animate');
    clearTimeout(closeTimeout); 
}

// --- MASTER SCROLL CONTROLLER ---
window.addEventListener('scroll', () => {
    const currentScrollY = window.scrollY;
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

    if (!hasCelebrated && currentScrollY >= docHeight - 50 && docHeight > 100) {
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

    document.body.classList.add('is-scrolling'); document.body.classList.remove('is-idle');
    clearTimeout(weatherTimeout);
    weatherTimeout = setTimeout(() => {
        document.body.classList.remove('is-scrolling'); document.body.classList.add('is-idle');
    }, 300); 
});
window.dispatchEvent(new Event('scroll'));

function animateRain() {
    if(document.body.classList.contains('past-hero')) {
        ctx.clearRect(0, 0, width, height);
        const isDark = document.body.classList.contains('dark-mode');
        const colorRGB = isDark ? '200, 230, 255' : '100, 150, 200'; 

        if (document.body.classList.contains('is-idle')) {
            for(let drop of drops) {
                drop.y += drop.speed; drop.x += 0.5; 
                if(drop.y > height - 10) { 
                    splashes.push({ x: drop.x, y: height - 10, radius: 1, maxRadius: Math.random() * 8 + 4, opacity: drop.opacity });
                    drop.y = -50; drop.x = Math.random() * width; 
                }
                if(drop.x > width + 20) { drop.x = -20; }
                ctx.beginPath(); ctx.strokeStyle = `rgba(${colorRGB}, ${drop.opacity})`; ctx.lineWidth = drop.thickness;
                ctx.moveTo(drop.x, drop.y); ctx.lineTo(drop.x + 1, drop.y + drop.length); ctx.stroke();
            }
            for(let i = splashes.length - 1; i >= 0; i--) {
                let s = splashes[i];
                ctx.beginPath(); ctx.strokeStyle = `rgba(${colorRGB}, ${s.opacity})`; ctx.lineWidth = 1;
                ctx.ellipse(s.x, s.y, s.radius * 2, s.radius, 0, 0, Math.PI * 2); ctx.stroke();
                s.radius += 0.5; s.opacity -= 0.02; 
                if (s.opacity <= 0) splashes.splice(i, 1); 
            }
        }
    }
    requestAnimationFrame(animateRain);
}
animateRain();

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