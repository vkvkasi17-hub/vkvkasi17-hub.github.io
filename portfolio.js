'use strict';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { mobileNav.hidden = true; menuButton.setAttribute('aria-expanded', 'false'); }
menuButton.addEventListener('click', () => {
  mobileNav.hidden = !mobileNav.hidden;
  menuButton.setAttribute('aria-expanded', String(!mobileNav.hidden));
});
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
if ('IntersectionObserver' in window) {
  document.body.classList.add('motion-ready');
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('visible'); revealObserver.unobserve(entry.target); } });
  }, { threshold: 0.07 });
  document.querySelectorAll('.reveal').forEach(element => revealObserver.observe(element));
  const navObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) document.querySelectorAll('.desktop-nav a').forEach(link => link.classList.toggle('active', link.hash === '#' + entry.target.id));
    });
  }, { rootMargin: '-15% 0px -55% 0px' });
  document.querySelectorAll('main > section[id]').forEach(section => navObserver.observe(section));
}
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-filter]').forEach(item => {
    const selected = item === button;
    item.classList.toggle('active', selected);
    item.setAttribute('aria-pressed', String(selected));
  });
  document.querySelectorAll('[data-project]').forEach(card => {
    card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter;
    if (!card.hidden) card.classList.add('visible');
  });
  document.querySelector('.project-outro').hidden = button.dataset.filter !== 'all';
}));
const projects = JSON.parse(document.getElementById('project-data').textContent);
const dialog = document.getElementById('project-dialog');
document.querySelectorAll('[data-project]').forEach(card => card.addEventListener('click', () => {
  const project = projects[Number(card.dataset.project)];
  document.getElementById('dialog-category').textContent = project.category + ' / SELECTED PROJECT';
  document.getElementById('dialog-title').textContent = project.title;
  document.getElementById('dialog-tech').textContent = project.tech;
  // Overview markup is authored in the local portfolio_data.json file.
  document.getElementById('dialog-overview').innerHTML = project.overview;
  const links = document.getElementById('dialog-links');
  links.replaceChildren();
  for (const [url, label] of [[project.github_link, project.github_link === 'https://github.com/vkvkasi17-hub' ? 'GitHub profile ↗' : 'View source ↗'], [project.website_link, 'Live project ↗']]) {
    if (!url) continue;
    const a = document.createElement('a');
    a.href = url; a.textContent = label; a.className = 'pill'; a.target = '_blank'; a.rel = 'noopener'; links.append(a);
  }
  dialog.showModal();
  document.body.style.overflow = 'hidden';
}));
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const rect = dialog.getBoundingClientRect(); if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close(); } });
dialog.addEventListener('close', () => { document.body.style.overflow = ''; });
let toastTimer;
document.getElementById('copy-email').addEventListener('click', async () => {
  const toast = document.getElementById('toast');
  try { await navigator.clipboard.writeText('vkvkasi17@gmail.com'); toast.textContent = 'Email address copied.'; }
  catch { toast.textContent = 'Email: vkvkasi17@gmail.com'; }
  clearTimeout(toastTimer); toast.classList.add('show'); toastTimer = setTimeout(() => toast.classList.remove('show'), 3500);
});
document.getElementById('year').textContent = new Date().getFullYear();
// Ray-marched 3D sculpture: torus and floating spheres, lit in world space.
// No remote libraries or model downloads. The CSS background is the fallback.
const scene = document.getElementById('scene-canvas');
const gl = scene.getContext('webgl', { alpha: true, antialias: false, powerPreference: 'low-power' });
if (gl) {
  const vertex = 'attribute vec2 position; void main(){gl_Position=vec4(position,0.,1.);}';
  const fragment = `precision mediump float;
    uniform vec2 resolution; uniform float time; uniform vec2 pointer;
    mat2 rotate(float a){return mat2(cos(a),-sin(a),sin(a),cos(a));}
    float model(vec3 p){
      float spread=min(resolution.x/resolution.y/1.8,1.);vec3 q=p-vec3(3.5*spread,0.45,0.0);q.xz=rotate(0.6+time*0.13+pointer.x*0.2)*q.xz;q.xy=rotate(0.5)*q.xy;
      float ring=length(vec2(length(q.xz)-1.28,q.y))-0.34;
      float orb=length(p-vec3(-3.7*spread,-1.35+sin(time*0.4)*0.18,0.0))-0.8;
      float small=length(p-vec3(0.0,1.75+cos(time*0.3)*0.12,-1.1))-0.36;
      return min(ring,min(orb,small));
    }
    vec3 normal(vec3 p){vec2 e=vec2(0.004,0.0);return normalize(vec3(model(p+e.xyy)-model(p-e.xyy),model(p+e.yxy)-model(p-e.yxy),model(p+e.yyx)-model(p-e.yyx)));}
    void main(){vec2 uv=(gl_FragCoord.xy*2.-resolution)/resolution.y;
      vec3 ro=vec3(pointer.x*0.13,pointer.y*0.13,6.8);vec3 rd=normalize(vec3(uv,-2.1));
      float t=0.;float d=0.;for(int i=0;i<64;i++){d=model(ro+rd*t);if(d<0.004||t>14.)break;t+=d*0.85;}
      if(t>14.){gl_FragColor=vec4(0.);return;}
      vec3 p=ro+rd*t;vec3 n=normal(p);vec3 light=normalize(vec3(-3.,5.,5.));
      float diffuse=max(dot(n,light),0.);float shine=pow(max(dot(reflect(-light,n),-rd),0.),40.);
      float edge=pow(1.-max(dot(n,-rd),0.),2.);
      vec3 color=mix(vec3(0.32,0.43,0.29),vec3(0.74,0.75,0.54),n.x*0.5+0.5);
      color=color*(0.7+diffuse*0.32)+shine*0.48+edge*vec3(0.14,0.20,0.25);
      gl_FragColor=vec4(color,0.9);
    }`;
  function compile(type, source) { const shader=gl.createShader(type); gl.shaderSource(shader,source);gl.compileShader(shader);if(!gl.getShaderParameter(shader,gl.COMPILE_STATUS)){gl.deleteShader(shader);return null;}return shader; }
  const vs=compile(gl.VERTEX_SHADER,vertex),fs=compile(gl.FRAGMENT_SHADER,fragment);
  if (vs && fs) {
    const program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);
    if (gl.getProgramParameter(program,gl.LINK_STATUS)) {
      gl.useProgram(program);const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
      const pos=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
      const r=gl.getUniformLocation(program,'resolution'),t=gl.getUniformLocation(program,'time'),m=gl.getUniformLocation(program,'pointer');
      let pointerX=0,pointerY=0,animation=null,last=0,elapsed=0;
      function draw(){gl.uniform2f(r,scene.width,scene.height);gl.uniform1f(t,elapsed);gl.uniform2f(m,pointerX,pointerY);gl.drawArrays(gl.TRIANGLES,0,6);}
      function resize(){const scale=Math.min(window.devicePixelRatio||1,1)*0.65;const bounds=scene.getBoundingClientRect();scene.width=Math.round(bounds.width*scale);scene.height=Math.round(bounds.height*scale);gl.viewport(0,0,scene.width,scene.height);draw();}
      function loop(now){animation=null;if(document.hidden||reducedMotion.matches)return;if(now-last>32){elapsed+=Math.min((now-last)/1000,0.05);last=now;draw();}animation=requestAnimationFrame(loop);}
      function sync(){if(animation!==null)cancelAnimationFrame(animation);animation=null;last=performance.now();draw();if(!document.hidden&&!reducedMotion.matches)animation=requestAnimationFrame(loop);}
      window.addEventListener('pointermove',event=>{if(reducedMotion.matches)return;pointerX=event.clientX/innerWidth*2-1;pointerY=1-event.clientY/innerHeight*2;},{passive:true});
      window.addEventListener('resize',resize,{passive:true});document.addEventListener('visibilitychange',sync);reducedMotion.addEventListener('change',sync);
      scene.addEventListener('webglcontextlost',()=>{if(animation!==null)cancelAnimationFrame(animation);scene.style.display='none';});resize();sync();
    }
  }
}
// Pin long cards only after their full contents have scrolled into view.
// Shorter cards stack under the navigation; all content remains in normal flow.
const experienceCards = [...document.querySelectorAll('.experience-card')];
function sizeExperienceStack() {
  const headerBottom = document.querySelector('.site-header').getBoundingClientRect().height + 20;
  experienceCards.forEach((card, index) => {
    const desiredTop = headerBottom + index * 12;
    const readableTop = window.innerHeight - card.offsetHeight - 24;
    card.style.setProperty('--stack-top', Math.min(desiredTop, readableTop) + 'px');
  });
}
if ('ResizeObserver' in window) {
  const stackResize = new ResizeObserver(sizeExperienceStack);
  experienceCards.forEach(card => stackResize.observe(card));
}
window.addEventListener('resize', sizeExperienceStack, { passive: true });
sizeExperienceStack();
