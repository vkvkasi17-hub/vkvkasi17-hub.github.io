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

// Interactive, locally rendered 3D sculpture. No external rendering dependency.
const scene = document.getElementById('scene-canvas');
const stage = document.querySelector('.sculpture-drag');
const motionButton = document.querySelector('.motion-toggle');
let paused = reducedMotion.matches;
let rotation = 0, paletteIndex = 0, requestRender = () => {};
function updateMotion() {
  document.body.classList.toggle('motion-paused', paused || reducedMotion.matches);
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.disabled = reducedMotion.matches;
  motionButton.innerHTML = reducedMotion.matches ? 'Reduced motion' : paused ? 'Resume motion <span>▶</span>' : 'Pause motion <span>Ⅱ</span>';
  requestRender();
}
motionButton.addEventListener('click', () => { paused = !paused; updateMotion(); });
reducedMotion.addEventListener('change', () => { paused = reducedMotion.matches; updateMotion(); });
const palettes = [ ['#baf88b','186,248,139','#a390ff'], ['#ffba86','255,186,134','#f28aba'], ['#7ce8e1','124,232,225','#7ea2ff'] ];
document.querySelectorAll('.palette').forEach(button => button.addEventListener('click', () => {
  paletteIndex = Number(button.dataset.palette);
  const colors = palettes[paletteIndex];
  document.documentElement.style.setProperty('--accent', colors[0]);
  document.documentElement.style.setProperty('--accent-rgb', colors[1]);
  document.documentElement.style.setProperty('--secondary', colors[2]);
  document.querySelectorAll('.palette').forEach(item => { item.classList.toggle('active', item === button); item.setAttribute('aria-pressed', String(item === button)); });
  requestRender();
}));
function setRotation(value) {
  rotation = ((value + 180) % 360 + 360) % 360 - 180;
  stage.setAttribute('aria-valuenow', String(Math.round(rotation)));
  stage.setAttribute('aria-valuetext', Math.round(rotation) + ' degrees'); requestRender();
}
let dragX = null;
stage.addEventListener('pointerdown', event => { if(event.button !== 0) return; dragX=event.clientX; stage.setPointerCapture(event.pointerId); });
stage.addEventListener('pointermove', event => { if(dragX === null) return; setRotation(rotation+(event.clientX-dragX)*0.65); dragX=event.clientX; });
function releaseDrag(){dragX=null;}
stage.addEventListener('pointerup',releaseDrag);stage.addEventListener('pointercancel',releaseDrag);stage.addEventListener('lostpointercapture',releaseDrag);
stage.addEventListener('keydown', event => {
  if (['ArrowLeft','ArrowRight','Home'].includes(event.key)) { event.preventDefault();setRotation(event.key === 'Home' ? 0 : rotation + (event.key === 'ArrowLeft' ? -15 : 15)); }
});
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('pointermove', event => {
    if(reducedMotion.matches || paused || !finePointer.matches) return;
    const box=card.getBoundingClientRect(), x=(event.clientX-box.left)/box.width, y=(event.clientY-box.top)/box.height;
    card.style.setProperty('--rx', (0.5-y)*9+'deg');card.style.setProperty('--ry',(x-0.5)*11+'deg');
    card.style.setProperty('--shine-x',x*100+'%');card.style.setProperty('--shine-y',y*100+'%');
  });
  card.addEventListener('pointerleave',()=>{card.style.setProperty('--rx','0deg');card.style.setProperty('--ry','0deg');});
});
let scrollFrame;
function trackScroll(){if(scrollFrame)return;scrollFrame=requestAnimationFrame(()=>{scrollFrame=null;const max=document.documentElement.scrollHeight-innerHeight;document.documentElement.style.setProperty('--progress',max>0?scrollY/max:0);requestRender();});}
window.addEventListener('scroll',trackScroll,{passive:true});trackScroll();
const gl = scene.getContext('webgl', {alpha:true, antialias:false, powerPreference:'low-power',premultipliedAlpha:false});
if (gl) {
  const vertex='attribute vec2 position;void main(){gl_Position=vec4(position,0.,1.);}';
  const fragment=`precision mediump float;
    uniform vec2 resolution,focus;uniform float radius,time,turn,palette,scroll;
    mat2 spin(float a){return mat2(cos(a),-sin(a),sin(a),cos(a));}
    float sculpture(vec3 p){
      p.xy=spin(-0.45+sin(time*0.2)*0.12)*p.xy;
      p.xz=spin(0.55+turn+time*0.18+scroll*0.00025)*p.xz;
      p.yz=spin(0.7)*p.yz;
      p.xz=spin(p.y*0.75)*p.xz;
      float angle=atan(p.z,p.x);
      float loop=1.12+0.18*cos(angle*3.);
      return length(vec2(length(p.xz)-loop,p.y))-0.35;
    }
    vec3 norm(vec3 p){vec2 e=vec2(.004,0.);return normalize(vec3(sculpture(p+e.xyy)-sculpture(p-e.xyy),sculpture(p+e.yxy)-sculpture(p-e.yxy),sculpture(p+e.yyx)-sculpture(p-e.yyx)));}
    void main(){
      vec2 uv=(gl_FragCoord.xy-focus)/radius;if(length(uv)>1.8){gl_FragColor=vec4(0.);return;}
      vec3 ro=vec3(0.,0.,5.5),rd=normalize(vec3(uv,-3.));float t=0.;float d=0.;
      for(int i=0;i<72;i++){d=sculpture(ro+rd*t);if(d<.003||t>10.)break;t+=d*.8;}
      if(t>10.||d>.015){gl_FragColor=vec4(0.);return;}
      vec3 p=ro+rd*t,n=norm(p);vec3 light=normalize(vec3(-3.,4.,5.));
      float diffuse=max(dot(n,light),0.);float rim=pow(1.-max(dot(n,-rd),0.),2.);
      float spec=pow(max(dot(reflect(-light,n),-rd),0.),55.);
      float bands=sin(dot(n,vec3(3.,2.,4.))+p.y*1.5)*.5+.5;
      vec3 a=vec3(.37,.18,.95),b=vec3(.28,.93,.83);
      if(palette>.5&&palette<1.5){a=vec3(.88,.15,.48);b=vec3(1.,.65,.27);}
      if(palette>1.5){a=vec3(.1,.35,.95);b=vec3(.25,.96,.86);}
      vec3 c=mix(a,b,bands);c=c*(.3+diffuse*.75)+spec*.85+rim*mix(b,vec3(.75,.7,1.),.4)*.7;
      float strip=pow(max(0.,sin(n.x*3.+n.y*5.)),14.);c+=strip*.28;
      gl_FragColor=vec4(c,1.);
    }`;
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){gl.deleteShader(s);return null;}return s;}
  const vs=shader(gl.VERTEX_SHADER,vertex),fs=shader(gl.FRAGMENT_SHADER,fragment);
  if(vs&&fs){
    const program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);
    if(gl.getProgramParameter(program,gl.LINK_STATUS)){
      gl.useProgram(program);const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
      const position=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(position);gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
      const uniforms={};['resolution','focus','radius','time','turn','palette','scroll'].forEach(name=>uniforms[name]=gl.getUniformLocation(program,name));
      let scale=.8,elapsed=0,frame=null,last=0,lost=false;
      function draw(){
        if(lost)return;
        const box=stage.getBoundingClientRect();const visible=box.bottom>0&&box.top<innerHeight;
        const cx=visible?box.left+box.width/2:innerWidth*.88;
        const cy=visible?box.top+box.height/2:innerHeight*.5;
        const size=visible?Math.min(box.width,box.height)*(innerWidth<650?.66:.76):Math.min(innerWidth,innerHeight)*.42;
        gl.uniform2f(uniforms.resolution,scene.width,scene.height);gl.uniform2f(uniforms.focus,cx*scale,(innerHeight-cy)*scale);gl.uniform1f(uniforms.radius,size*scale);
        gl.uniform1f(uniforms.time,elapsed);gl.uniform1f(uniforms.turn,rotation*Math.PI/180);gl.uniform1f(uniforms.palette,paletteIndex);gl.uniform1f(uniforms.scroll,reducedMotion.matches?0:scrollY);
        gl.drawArrays(gl.TRIANGLES,0,6);
      }
      function loop(now){frame=null;if(document.hidden||paused||reducedMotion.matches||lost)return;if(now-last>=33){elapsed+=Math.min((now-last)/1000,.05);last=now;draw();}frame=requestAnimationFrame(loop);}
      requestRender=()=>{if(frame!==null)cancelAnimationFrame(frame);frame=null;draw();last=performance.now();if(!document.hidden&&!paused&&!reducedMotion.matches&&!lost)frame=requestAnimationFrame(loop);};
      function resize(){scale=Math.min(window.devicePixelRatio||1,innerWidth<650?1:1.25);scene.width=Math.round(innerWidth*scale);scene.height=Math.round(innerHeight*scale);gl.viewport(0,0,scene.width,scene.height);requestRender();}
      window.addEventListener('resize',resize,{passive:true});document.addEventListener('visibilitychange',requestRender);
      scene.addEventListener('webglcontextlost',()=>{lost=true;if(frame!==null)cancelAnimationFrame(frame);scene.style.display='none';document.body.classList.add('scene-fallback');});
      document.body.classList.add('scene-ready');resize();
    }
  }
}
if(!document.body.classList.contains('scene-ready'))document.body.classList.add('scene-fallback');
updateMotion();
