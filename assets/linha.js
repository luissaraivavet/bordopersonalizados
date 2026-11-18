'use strict';
// A linha que costura: um fio em ponto corrido desce pela margem da página,
// se borda com a rolagem, dá um laço em cada costura e termina num nó junto
// ao link do WhatsApp no fim da página. Sem SVG ou com movimento reduzido,
// o fio aparece pronto.
(function(){
  const NS='http://www.w3.org/2000/svg';
  const start=document.querySelector('.feature');
  const end=document.querySelector('#faq a[href*="wa.me"]');
  if(!start||!end||!document.createElementNS) return;

  const reduce=window.matchMedia('(prefers-reduced-motion: reduce)');
  const svg=document.createElementNS(NS,'svg');
  svg.setAttribute('class','linha');
  svg.setAttribute('aria-hidden','true');
  svg.innerHTML='<defs><mask id="linhaMascara" maskUnits="userSpaceOnUse"><path class="linha-guia" fill="none" stroke="#fff" pathLength="1"/></mask></defs>'+
    '<path class="linha-fio" fill="none" mask="url(#linhaMascara)"/>'+
    '<circle class="linha-agulha" r="3"/><circle class="linha-no" r="4.5"/>';
  document.body.appendChild(svg);
  const guide=svg.querySelector('.linha-guia'), thread=svg.querySelector('.linha-fio');
  const needle=svg.querySelector('.linha-agulha'), knot=svg.querySelector('.linha-no');

  let total=0, samples=[], frame=0, top=0, bottom=0, x=0;
  const pageY=element=>element.getBoundingClientRect().top+window.scrollY;

  function build(){
    const wrap=document.querySelector('.feature .wrap')||start;
    const gutter=wrap.getBoundingClientRect().left+parseFloat(getComputedStyle(wrap).paddingLeft);
    x=Math.max(7,Math.round(gutter/2));
    top=pageY(start)+24;
    const endBox=end.getBoundingClientRect();
    bottom=endBox.top+window.scrollY+endBox.height/2;
    const amp=Math.min(6,x*.6), step=140;
    const loops=[...document.querySelectorAll('main > .costura')].map(c=>pageY(c)+c.offsetHeight/2).filter(y=>y>top+80&&y<bottom-80);
    let d=`M${x} ${top}`, y=top, side=1;
    const wave=to=>{while(y+step<to){y+=step;d+=` Q${x+amp*side} ${y-step/2} ${x} ${y}`;side*=-1;}d+=` L${x} ${to}`;y=to;};
    loops.forEach(ly=>{
      wave(ly-26);
      // Laço: o fio sobe pela costura, contorna e volta ao eixo.
      // Na margem estreita do celular o laço encolhe para não sair da tela.
      const k=Math.min(1,(x-2)/22);
      d+=` C${x+30*k} ${ly-26} ${x+30*k} ${ly+16} ${x} ${ly+16} C${x-22*k} ${ly+16} ${x-20*k} ${ly-10} ${x+2*k} ${ly-4} C${x+12*k} ${ly} ${x+6*k} ${ly+20} ${x} ${ly+30}`;
      y=ly+30;
    });
    wave(bottom);
    const endX=Math.min(endBox.left-12,x+40);
    d+=` Q${x} ${bottom+18} ${endX} ${bottom}`;
    guide.setAttribute('d',d); thread.setAttribute('d',d);
    svg.style.height=`${Math.ceil(bottom+40)}px`;
    knot.setAttribute('cx',endX); knot.setAttribute('cy',bottom);
    total=thread.getTotalLength();
    // Tabela altura -> comprimento, para o fio acompanhar a tela mesmo nos laços.
    samples=[];
    for(let l=0;l<=total;l+=12){samples.push([thread.getPointAtLength(l).y,l]);}
    draw();
  }

  function lengthAt(targetY){
    if(targetY<=top) return 0;
    let best=0;
    for(const [py,l] of samples){if(py<=targetY) best=l; else if(py>targetY+40) break;}
    return best;
  }

  function draw(){
    frame=0;
    const done=reduce.matches;
    const reach=done?total:lengthAt(window.scrollY+window.innerHeight*.72);
    const progress=total?reach/total:1;
    guide.style.strokeDashoffset=String(1-progress);
    const head=thread.getPointAtLength(reach);
    needle.setAttribute('cx',head.x); needle.setAttribute('cy',head.y);
    svg.classList.toggle('is-tied',progress>.995);
    svg.classList.toggle('is-started',progress>0);
  }

  const schedule=()=>{if(!frame) frame=requestAnimationFrame(draw);};
  let resizeTimer=0;
  const rebuild=()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(build,150);};
  window.addEventListener('scroll',schedule,{passive:true});
  window.addEventListener('resize',rebuild);
  if('ResizeObserver' in window) new ResizeObserver(rebuild).observe(document.querySelector('main')||document.body);
  if(reduce.addEventListener) reduce.addEventListener('change',draw);
  window.addEventListener('load',build);
  build();
})();
