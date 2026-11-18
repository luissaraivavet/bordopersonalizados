'use strict';
    const content = window.BORDO_CONTENT;
    const settings = content.settings;
    const PHONE = settings.whatsapp;
    const STORAGE_KEY = 'bordo_cart_v2';
    const GIFT_PRICE = settings.giftPrice;
    const collections = content.collections.filter(item => item.published);
    const products = content.products.filter(item => item.published && collections.some(group => group.id === item.collection));
    const pixPrice = value => Math.round(Math.round(value * 100) * (100 - settings.pixDiscount) / 100) / 100;
    const money = value => value.toLocaleString('pt-BR', {style:'currency', currency:'BRL'});
    const icon = name => `<span class="icon i-${name}" aria-hidden="true"></span>`;
    const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    const whatsApp = message => `https://wa.me/${PHONE}?text=${encodeURIComponent(message)}`;
    const pieces = count => `${count} ${count === 1 ? 'peça' : 'peças'}`;
    const countLabel = list => list.length && list.every(p => p.bundle) ? `${list.length} ${list.length === 1 ? 'kit' : 'kits'}` : pieces(list.length);
    // A opção genérica do catálogo não descreve a peça; ela fica fora das legendas e da mensagem.
    const isPlaceholderOption = option => /^acabamento a (confirmar|combinar)/i.test(option || '');
    const realOptions = p => p.options.filter(option => !isPlaceholderOption(option));
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    // Miniaturas leves em assets/thumbs; se faltar uma, a foto original entra no lugar.
    const thumbOf = image => `assets/thumbs/${image.split('/').pop().replace(/\.[^.]+$/, '')}.webp`;
    // "Laço bordado Daisy — Margarida e Borboleta" vira tipo, nome próprio e espécie.
    const titleParts = title => {
      const match = /^(.*)\s+(\S+)\s+—\s+(.+)$/.exec(title);
      return match ? {kind:match[1], name:match[2], species:match[3]} : {kind:'', name:title, species:''};
    };
    let toastTimer;
    function notify(message) {
      const toast = document.getElementById('toast');
      toast.textContent = message;
      toast.hidden = false;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => { toast.hidden = true; }, 3500);
    }

    // A lista de elementos é lida a cada Tab, porque a sacola é redesenhada com o diálogo aberto.
    function trapFocus(dialog) {
      dialog.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        const focusable = [...dialog.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')].filter(item => !item.disabled && item.tabIndex >= 0 && item.offsetParent !== null);
        if (!focusable.length) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
    }

    function titleHTML(p) {
      const parts = titleParts(p.title);
      if (!parts.species) return `<h3 class="plain">${escapeHTML(p.title)}</h3>`;
      return `<h3><em>${escapeHTML(parts.name)}</em><span class="sr"> — </span><span class="species">${escapeHTML(parts.species)}</span><span class="sr">, </span><span class="kind">${escapeHTML(parts.kind)}</span></h3>`;
    }
    function productCard(p) {
      const title=escapeHTML(p.title), image=escapeHTML(p.image), id=escapeHTML(p.id);
      const sentences=p.description.split(/(?<=[.!?])\s/);
      const members=p.bundle ? p.bundle.map(member=>products.find(item=>item.id===member)).filter(Boolean) : [];
      const figure=members.length
        ? `<figure class="product-figure kit-figure"><div class="kit-images">${members.map(item=>`<img src="${escapeHTML(item.image)}" alt="${escapeHTML(item.title)}" width="600" height="600" loading="lazy">`).join('')}</div></figure>`
        : `<figure class="product-figure"><span class="crop"><img src="${image}" alt="${title}" width="600" height="750" loading="lazy"></span><button class="icon-button zoom-button" data-zoom="${image}" data-title="${title}" aria-label="Ampliar ${title}" title="Ampliar imagem">${icon('zoom-in')}</button></figure>`;
      const buy=Number.isFinite(p.price)
        ? `<div class="product-price"><strong>${money(p.price)}</strong><small>${money(pixPrice(p.price))} no Pix</small></div>${p.options.length > 1 ? `<label class="field-label" for="var-${id}">Opção da peça</label><select id="var-${id}">${p.options.map(o => `<option>${escapeHTML(o)}</option>`).join('')}</select>` : realOptions(p).length ? `<p class="product-option">${escapeHTML(realOptions(p)[0])}</p>` : ''}<button class="button" data-add="${id}">${icon('plus')} Adicionar à sacola</button>`
        : `<a class="text-link" href="#personalizados" data-inquiry="Gostaria de consultar: ${title}.">Quero este encanto ${icon('arrow-right')}</a>`;
      return `<article class="product" id="p-${id}" tabindex="-1">${figure}<div class="product-info">${titleHTML(p)}<p class="desc">${escapeHTML(sentences[0])}</p>${sentences.length > 1 ? `<details class="product-details"><summary>Detalhes da peça</summary><p>${escapeHTML(p.description)}</p></details>` : ''}${buy}</div></article>`;
    }
    // Índice por espécie para as coleções grandes: leva à peça mesmo quando ela está recolhida.
    function speciesIndex(collection, list) {
      const entries=list.map(p=>({id:p.id, ...titleParts(p.title)})).sort((a,b)=>(a.species||a.name).localeCompare(b.species||b.name,'pt-BR'));
      return `<details class="species-index ficha"><summary>Índice da coleção ${icon('chevron-down')}</summary><ol>${entries.map(entry=>`<li><a href="#p-${escapeHTML(entry.id)}" data-goto="${escapeHTML(entry.id)}"><span>${escapeHTML(entry.species||entry.name)}</span>${entry.species ? `<i>${escapeHTML(entry.name)}</i>` : ''}</a></li>`).join('')}</ol></details>`;
    }
    function catalogSection(c) {
      const id=escapeHTML(c.id), list=products.filter(p => p.collection === c.id);
      return `<section class="section plate ${id}${list.length <= 2 ? ' compact' : ''}" id="${id}" aria-labelledby="${id}Title"><div class="wrap"><div class="section-heading"><div><h2 id="${id}Title">${escapeHTML(c.name)}</h2><p>${escapeHTML(c.description)}</p><p class="count">${countLabel(list)}</p></div><a class="text-link" href="#personalizados">Conversar sobre uma peça ${icon('arrow-right')}</a></div>${list.length > 9 ? speciesIndex(c, list) : ''}<div class="product-grid${list.length <= 2 ? ' few' : list.length === 5 ? ' five' : ''}" id="grid-${id}">${list.map(productCard).join('')}</div>${list.length > 6 ? `<button class="button secondary collection-more" data-expand="${id}" aria-expanded="false" aria-controls="grid-${id}">Ver coleção completa (${pieces(list.length)})</button>` : ''}<p class="collection-note">Disponibilidade, frete, materiais e prazo são confirmados no atendimento.</p>${c.id === 'sinfonia' ? document.getElementById('filmTemplate').innerHTML : ''}</div></section>`;
    }
    // A sacola acompanha as abas porque o cabeçalho não é fixo a partir de 768px.
    const bagTab = () => `<button type="button" class="tab-bag" data-open-bag aria-label="Abrir sacola" title="Abrir sacola">${icon('shopping-bag')}<span class="tab-bag-label">Sacola</span><span class="tab-bag-count">0</span></button>`;
    const tabLinks = () => collections.map(c=>({id:c.id,label:c.name.split(' ')[0],title:c.name})).concat({id:'personalizados',label:'Personalizados',title:'Projetos personalizados'}).map(entry=>`<a href="#${escapeHTML(entry.id)}" data-tab="${escapeHTML(entry.id)}" aria-label="${escapeHTML(entry.title)}" title="${escapeHTML(entry.title)}" style="--tab:var(--tab-${escapeHTML(entry.id)},var(--wine))">${escapeHTML(entry.label)}</a>`).join('');
    function renderProducts() {
      document.querySelector('.dropdown').innerHTML = '<a href="#mae-rainha">Mãe &amp; Rainha</a><a href="#colinho-do-ceu">Colinho do Céu</a>' + collections.map(c => `<a href="#${escapeHTML(c.id)}">${escapeHTML(c.name)}</a>`).join('');
      document.querySelector('.collection-grid').innerHTML = collections.filter(c => c.featured).map(c => `<a class="collection-link" href="#${escapeHTML(c.id)}"><figure class="collection-photo"><span class="crop"><img src="${escapeHTML(c.image)}" alt="${escapeHTML(c.name)}" width="1400" height="850" loading="lazy"></span></figure><div class="collection-caption"><h2>${escapeHTML(c.name)}</h2><span class="text-link">Conhecer a coleção ${icon('arrow-right')}</span><span class="count">${countLabel(products.filter(p => p.collection === c.id))}</span></div></a>`).join('');
      document.getElementById('catalogSections').innerHTML = `<nav class="tab-strip" aria-label="Abas das coleções">${tabLinks()}${bagTab()}</nav>` + collections.map(catalogSection).join('');
      document.getElementById('pageTitle').textContent=settings.headline.includes(settings.location) ? settings.headline : `${settings.headline} em ${settings.location}`;
      document.querySelector('.intro p').textContent=settings.intro;
      const story=document.querySelector('.story-copy'), link=story.querySelector('a');
      story.querySelectorAll('p, .story-more').forEach(p=>p.remove());
      // Dois parágrafos abrem a história; o restante fica a um toque.
      const storyParts=settings.story.split(/\n\s*\n/), paragraph=text=>{const p=document.createElement('p');p.textContent=text;return p;};
      storyParts.slice(0,2).forEach(text=>story.insertBefore(paragraph(text),link));
      if(storyParts.length>2){const more=document.createElement('details');more.className='story-more';more.innerHTML=`<summary class="text-link">Ler a história completa ${icon('chevron-down')}</summary>`;storyParts.slice(2).forEach(text=>more.append(paragraph(text)));story.insertBefore(more,link);}
      document.getElementById('storyPortrait').src=settings.storyImage||'assets/priscila-presentes.png';
      document.getElementById('storySecondary').src=settings.storyImageSecondary||'assets/priscila-sinfonia.png';
      document.querySelectorAll('a[href*="instagram.com"]').forEach(a=>a.href=settings.instagram);
      document.querySelectorAll('a[href^="https://wa.me/"]').forEach(a=>a.href=whatsApp('Olá, Bordô! Gostaria de saber mais sobre uma encomenda.'));
      const contact=document.querySelector('.footer-main>div:last-child a');
      contact.textContent=`WhatsApp: +${PHONE}`;
      document.querySelector('.footer-main>div:last-child p').textContent=`${settings.location}. Atendimento online e por encomenda. Envio sob consulta.`;
      document.querySelector('.footer-main>div:first-child p').textContent=`Laços e bordados personalizados. Atendimento online, por encomenda. ${settings.location}.`;
      document.querySelector('.gift span').textContent=`Adicionar embalagem kraft para presente (+ ${money(GIFT_PRICE)})`;
      document.querySelector('#giftTotalRow span:last-child').textContent=money(GIFT_PRICE);
      document.querySelector('.totals .pix span').textContent=`Ou no Pix (${settings.pixDiscount}% nas peças)`;
      const footerCollections=document.getElementById('footerCollections');
      footerCollections.innerHTML=collections.map(c=>`<a href="#${escapeHTML(c.id)}">${escapeHTML(c.name)}</a>`).join('');
      document.getElementById('paymentAnswer').textContent=`A sacola apresenta o total e a alternativa com ${settings.pixDiscount}% de desconto no Pix sobre as peças. A embalagem para presente é opcional, por ${money(GIFT_PRICE)} por pedido. Frete e condições finais são confirmados pelo WhatsApp. Não há cobrança pelo site.`;
      const reviews=content.testimonials.filter(i=>i.published), articles=content.articles.filter(i=>i.published);
      document.getElementById('editorialSections').innerHTML=(reviews.length ? `<section class="section"><div class="wrap"><div class="section-heading"><h2>Quem recebeu um encanto</h2></div><div class="editorial-grid">${reviews.map(r=>`<blockquote><p>“${escapeHTML(r.text)}”</p><footer>${escapeHTML(r.name)}</footer></blockquote>`).join('')}</div></div></section>` : '')+(articles.length ? `<section class="section"><div class="wrap"><div class="section-heading"><h2>Histórias e cuidados</h2></div><div class="editorial-grid">${articles.map(a=>`<article><img src="${escapeHTML(a.image)}" alt="${escapeHTML(a.title)}" loading="lazy"><h3>${escapeHTML(a.title)}</h3><p>${escapeHTML(a.excerpt)}</p><details class="article-text"><summary class="text-link">Ler artigo ${icon('arrow-right')}</summary>${a.body.split(/\n\s*\n/).map(p=>`<p>${escapeHTML(p)}</p>`).join('')}</details></article>`).join('')}</div></div></section>` : '');
      document.getElementById('extraLinks').innerHTML=content.links.filter(l=>l.published).map(l=>`<a href="${escapeHTML(l.url)}" target="_blank" rel="noopener">${escapeHTML(l.title)}</a>`).join('');
    }

    // Capa: o espécime em destaque troca pelo índice; a troca automática para ao primeiro gesto.
    function initHero() {
      const root=document.getElementById('heroSpecimen'), strip=document.getElementById('heroIndex'), pause=document.getElementById('heroPause');
      const lists=collections.filter(c=>c.featured).map(c=>products.filter(p=>p.collection===c.id && Number.isFinite(p.price) && !p.bundle && p.options.length<=1));
      const pool=[];
      for(let row=0; pool.length<8 && lists.some(list=>list[row]); row++) for(const list of lists) if(list[row] && pool.length<8) pool.push(list[row]);
      if(!pool.length){root.hidden=true;strip.hidden=true;return;}
      const field=id=>document.getElementById(id);
      let current=0, timer=null, swapTimer=null;
      strip.innerHTML=pool.map((p,index)=>{const parts=titleParts(p.title);return `<button type="button" data-specimen="${index}" aria-pressed="${index===0}"><span class="crop"><img src="${escapeHTML(thumbOf(p.image))}" data-full="${escapeHTML(p.image)}" alt="" width="160" height="160" decoding="async"></span><span class="name">${escapeHTML(parts.name)}</span>${parts.species ? `<span class="sr"> — ${escapeHTML(parts.species)}</span>` : ''}</button>`;}).join('');
      function fill(index) {
        const p=pool[index], parts=titleParts(p.title);
        field('heroPhoto').innerHTML=`<span class="crop"><img src="${escapeHTML(p.image)}" width="800" height="1000" alt="${escapeHTML(p.title)}"${index===0 ? ' fetchpriority="high"' : ''}></span>`;
        field('heroCollection').textContent=collections.find(c=>c.id===p.collection).name;
        field('heroName').textContent=parts.name;
        field('heroName').classList.toggle('plain',!parts.species);
        root.querySelectorAll('.tag[hidden]').forEach(tag=>{tag.hidden=false;});
        field('heroSpecies').textContent=parts.species;
        field('heroSpecies').hidden=!parts.species;
        const option=realOptions(p).join(' · ') || parts.kind;
        field('heroOption').textContent=option;
        field('heroOption').parentElement.hidden=!option;
        field('heroPrice').textContent=money(p.price);
        field('heroPix').textContent=`${money(pixPrice(p.price))} no Pix`;
        field('heroAdd').dataset.add=p.id;
        strip.querySelectorAll('button').forEach((button,position)=>button.setAttribute('aria-pressed',String(position===index)));
      }
      function show(index) {
        current=index;
        clearTimeout(swapTimer);
        if(reducedMotion.matches){fill(index);return;}
        new Image().src=pool[index].image;
        root.classList.add('is-changing');
        // A leitura de offsetWidth fixa o estado inicial; a volta anima sem depender do próximo quadro.
        swapTimer=setTimeout(()=>{fill(index);void root.offsetWidth;root.classList.remove('is-changing');},170);
      }
      function stop() {
        clearInterval(timer);
        timer=null;
        pause.textContent='Retomar a troca de peças';
      }
      function start() {
        if(timer || pool.length<2 || reducedMotion.matches) return;
        pause.textContent='Pausar a troca de peças';
        timer=setInterval(()=>{
          const busy=document.hidden || document.querySelector('dialog[open]') || root.matches(':hover') || strip.matches(':hover') || root.contains(document.activeElement) || strip.contains(document.activeElement);
          if(!busy) show((current+1)%pool.length);
        },6000);
      }
      strip.addEventListener('click',event=>{const button=event.target.closest('[data-specimen]');if(!button)return;stop();show(Number(button.dataset.specimen));});
      field('heroAdd').addEventListener('click',stop);
      pause.addEventListener('click',()=>timer ? stop() : start());
      fill(0);
      if(pool.length>1 && !reducedMotion.matches){pause.hidden=false;start();}
    }
    // Aba lateral: aparece depois da capa e marca a seção que cruza o meio da tela.
    function initRail() {
      const rail=document.getElementById('sectionRail');
      rail.innerHTML=tabLinks()+bagTab();
      renderCartUI();
      if(!('IntersectionObserver' in window)) return;
      new IntersectionObserver(([entry])=>rail.classList.toggle('visible',!entry.isIntersecting)).observe(document.querySelector('.cover'));
      const mark=(id,current)=>document.querySelectorAll(`[data-tab="${id}"]`).forEach(link=>{if(current)link.setAttribute('aria-current','true');else link.removeAttribute('aria-current');});
      const spy=new IntersectionObserver(items=>{for(const item of items){if(item.isIntersecting){document.querySelectorAll('[data-tab][aria-current]').forEach(link=>link.removeAttribute('aria-current'));mark(item.target.id,true);const tab=document.querySelector(`.tab-strip [data-tab="${item.target.id}"]`);if(tab)tab.parentElement.scrollLeft=tab.offsetLeft-tab.parentElement.offsetLeft-16;}else mark(item.target.id,false);}},{rootMargin:'-45% 0px -50% 0px'});
      rail.querySelectorAll('[data-tab]').forEach(link=>{const section=document.getElementById(link.dataset.tab);if(section)spy.observe(section);});
    }
    function setExpanded(grid, expanded) {
      grid.classList.toggle('expanded',expanded);
      const button=document.querySelector(`[data-expand="${grid.id.slice(5)}"]`);
      if(!button) return;
      button.setAttribute('aria-expanded',String(expanded));
      button.textContent=expanded ? 'Mostrar menos' : `Ver coleção completa (${pieces(grid.children.length)})`;
    }
    function revealProduct(id) {
      const card=document.getElementById(`p-${id}`);
      if(!card) return;
      if(card.offsetParent===null) setExpanded(card.closest('.product-grid'),true);
      card.scrollIntoView({block:'center'});
      card.focus({preventScroll:true});
    }
    // Reconcile saved bags with the catalog; never trust stored prices or image URLs.
    function loadCart() {
      try {
        const stored=JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]'); if(!Array.isArray(stored)) return [];
        const result=[];
        for(const item of stored){
          if(!item || typeof item!=='object') continue;
          const product=products.find(p=>p.id===item.id || p.title===item.title);
          if(!product || !Number.isFinite(product.price) || !product.options.includes(item.variation) || !Number.isInteger(item.qty) || item.qty<1) continue;
          const existing=result.find(p=>p.id===product.id && p.variation===item.variation);
          if(existing) existing.qty=Math.min(99,existing.qty+item.qty);
          else result.push({id:product.id,title:product.title,price:product.price,imgPath:product.image,variation:item.variation,qty:Math.min(99,item.qty)});
        }
        return result;
      } catch { return []; }
    }
    let cart=loadCart();
    function saveCart(){ try{localStorage.setItem(STORAGE_KEY,JSON.stringify(cart));}catch{notify('Sua sacola funciona nesta visita, mas não pôde ser salva neste navegador.');} renderCartUI(); }
    function cartTotals(){ const subtotal=cart.reduce((sum,item)=>sum+item.price*item.qty,0); const gift=cart.length && document.getElementById('cartGiftCheck').checked ? GIFT_PRICE : 0; return {subtotal,gift,total:subtotal+gift,pix:pixPrice(subtotal)+gift}; }
    function checkoutMessage(){
      const totals=cartTotals();
      return `Olá, Bordô! Gostaria de consultar este pedido:\n\n`+cart.map(item=>`${item.qty}x ${item.title}\n${isPlaceholderOption(item.variation)?'':`Opção: ${item.variation}\n`}Valor: ${money(item.price*item.qty)}`).join('\n\n')+`\n\nSubtotal: ${money(totals.subtotal)}\n`+(totals.gift?`Embalagem kraft para presente: ${money(totals.gift)}\n`:'Sem embalagem adicional\n')+`Total estimado: ${money(totals.total)}\nAlternativa no Pix (${settings.pixDiscount}% de desconto nas peças): ${money(totals.pix)}\n\nPor favor, confirmem disponibilidade, prazo, frete e formas de pagamento.`;
    }
    function renderCartUI(){
      const list=document.getElementById('cartItemsList'); const count=cart.reduce((sum,item)=>sum+item.qty,0); const totals=cartTotals();
      document.getElementById('cartCountBadge').textContent=count;
      document.querySelectorAll('.tab-bag-count').forEach(badge=>{badge.textContent=count;});
      document.querySelectorAll('.tab-bag').forEach(tab=>tab.setAttribute('aria-label',`Abrir sacola, ${count} ${count===1?'item':'itens'}`));
      // Uma sacola vazia não carrega a embalagem para o próximo pedido.
      if(!cart.length) document.getElementById('cartGiftCheck').checked=false;
      document.getElementById('bagButton').setAttribute('aria-label',`Abrir sacola, ${count} ${count===1?'item':'itens'}`);
      list.innerHTML=cart.length ? cart.map((item,index)=>`<article class="bag-item"><img src="${escapeHTML(item.imgPath)}" alt="${escapeHTML(item.title)}" width="84" height="105"><div><h3>${escapeHTML(item.title)}</h3>${isPlaceholderOption(item.variation)?'':`<p>${escapeHTML(item.variation)}</p>`}<strong>${money(item.price*item.qty)}</strong><div class="quantity"><button class="icon-button" data-qty="${index}" data-delta="-1" aria-label="Diminuir quantidade de ${escapeHTML(item.title)}" title="Diminuir quantidade">${icon('minus')}</button><output aria-label="Quantidade">${item.qty}</output><button class="icon-button" data-qty="${index}" data-delta="1" aria-label="Aumentar quantidade de ${escapeHTML(item.title)}" title="Aumentar quantidade">${icon('plus')}</button><button class="icon-button remove" data-remove="${index}" aria-label="Remover ${escapeHTML(item.title)}" title="Remover peça">${icon('trash-2')}</button></div></div></article>`).join(''):`<div class="empty">${icon('shopping-bag')}<p>Sua sacola está esperando<br>o primeiro encanto.</p><button class="button secondary" id="emptyCollection">Explorar a coleção ${icon('arrow-right')}</button><button class="text-button" id="emptyCustom">Ou descreva uma encomenda</button></div>`;
      document.getElementById('cartSubtotalText').textContent=money(totals.subtotal); document.getElementById('cartTotalText').textContent=money(totals.total); document.getElementById('cartPixText').textContent=money(totals.pix);
      document.getElementById('giftTotalRow').hidden=!totals.gift; document.getElementById('cartGiftCheck').disabled=!cart.length;
      const checkout=document.getElementById('cartCheckout'); checkout.setAttribute('aria-disabled',String(!cart.length)); checkout.tabIndex=cart.length?0:-1; checkout.href=whatsApp(checkoutMessage());
    }
    function addToCart(id){
      const product=products.find(item=>item.id===id); if(!product || !Number.isFinite(product.price)) return;
      const variation=document.getElementById(`var-${id}`)?.value || product.options[0]; const existing=cart.find(item=>item.id===id && item.variation===variation);
      if(existing){if(existing.qty>=99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;} existing.qty++;}
      else cart.push({id,title:product.title,price:product.price,variation,imgPath:product.image,qty:1});
      saveCart(); document.getElementById('cartDrawer').showModal();
    }
    function updateSimulatorPreview(){
      const form=document.getElementById('customForm'); const data=new FormData(form); const detail=String(data.get('details')||'').trim();
      const city=String(data.get('city')||'').trim();
      const date=String(data.get('date')||'').trim();
      const summary=`Projeto: ${data.get('project')}\nQuantidade: ${data.get('quantity')}`+(detail?`\nDetalhes: ${detail}`:'')+(city?`\nCidade de entrega: ${city}`:'')+(date?`\nData desejada: ${date.split('-').reverse().join('/')}`:'');
      document.getElementById('simMsgPreviewText').textContent=summary;
      document.getElementById('customWhatsApp').href=whatsApp(`Olá! Vim pelo site da Bordô e gostaria de um orçamento personalizado.\n\n${summary}\n\nPodem me informar possibilidades, valores e prazo?`);
    }
    function closeMenu(){document.getElementById('mainNav').classList.remove('open');document.getElementById('menuButton').setAttribute('aria-expanded','false');document.getElementById('menuButton').setAttribute('aria-label','Abrir menu');document.querySelector('.collection-nav').open=false;}
    document.getElementById('menuButton').addEventListener('click',()=>{const open=document.getElementById('mainNav').classList.toggle('open');document.getElementById('menuButton').setAttribute('aria-expanded',String(open));document.getElementById('menuButton').setAttribute('aria-label',open?'Fechar menu':'Abrir menu');});
    document.getElementById('mainNav').addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
    document.addEventListener('keydown',event=>{if(event.key==='Escape'){const menuWasOpen=document.getElementById('mainNav').classList.contains('open');closeMenu();if(menuWasOpen)document.getElementById('menuButton').focus();}});
    document.addEventListener('error',event=>{const image=event.target;if(image instanceof HTMLImageElement && image.dataset.full){image.src=image.dataset.full;delete image.dataset.full;}},true);
    // Fotos fora do padrão 4:5 ganham a própria moldura em vez de um corte às cegas.
    document.addEventListener('load',event=>{
      const image=event.target;
      const figure=image instanceof HTMLImageElement ? image.closest('.product-figure:not(.kit-figure)') : null;
      if(!figure || !image.naturalHeight) return;
      const ratio=image.naturalWidth/image.naturalHeight;
      figure.classList.toggle('landscape',ratio>1.15);
      figure.classList.toggle('tall',ratio<.7);
    },true);
    document.addEventListener('click',event=>{
      const button=event.target.closest('button');
      if(button?.dataset.expand){const grid=document.getElementById(`grid-${button.dataset.expand}`);const expanded=button.getAttribute('aria-expanded')==='true';const firstHidden=[...grid.children].find(item=>item.offsetParent===null);setExpanded(grid,!expanded);if(expanded)button.scrollIntoView({block:'center'});else firstHidden?.querySelector('button, a')?.focus();return;}
      if(button?.dataset.add){addToCart(button.dataset.add);return;}
      if(button?.dataset.close){document.getElementById(button.dataset.close).close();return;}
      if(button?.dataset.zoom){document.getElementById('lightboxImage').src=button.dataset.zoom;document.getElementById('lightboxImage').alt=button.dataset.title;document.getElementById('imageTitle').textContent=button.dataset.title;document.getElementById('imageDialog').showModal();return;}
      if(button?.hasAttribute('data-qty')){const index=Number(button.dataset.qty);const delta=Number(button.dataset.delta);const item=cart[index];if(!item)return;if(item.qty+delta>99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;}item.qty+=delta;if(item.qty<=0)cart.splice(index,1);saveCart();const replacement=document.querySelector(`[data-qty="${index}"][data-delta="${delta}"]`);(replacement||document.querySelector('[data-close="cartDrawer"]')).focus();return;}
      if(button?.hasAttribute('data-remove')){cart.splice(Number(button.dataset.remove),1);saveCart();document.querySelector('[data-close="cartDrawer"]').focus();return;}
      if(button?.id==='emptyCollection'){document.getElementById('cartDrawer').close();document.getElementById('colecoes').scrollIntoView();return;}
      if(button?.id==='emptyCustom'){document.getElementById('cartDrawer').close();document.getElementById('personalizados').scrollIntoView();document.getElementById('simDetailInput').focus({preventScroll:true});return;}
      if(button?.hasAttribute('data-open-bag')){document.getElementById('cartDrawer').showModal();return;}
      const goto=event.target.closest('[data-goto]');if(goto){event.preventDefault();revealProduct(goto.dataset.goto);return;}
      const inquiry=event.target.closest('[data-inquiry]');if(inquiry){const project=inquiry.dataset.project||'Laços e coleções';document.querySelectorAll('input[name="project"]').forEach(input=>input.checked=input.value===project);document.getElementById('simDetailInput').value=inquiry.dataset.inquiry;updateSimulatorPreview();}
      if(!event.target.closest('.collection-nav')) document.querySelector('.collection-nav').open=false;
    });
    document.getElementById('bagButton').addEventListener('click',()=>{closeMenu();document.getElementById('cartDrawer').showModal();});
    document.getElementById('cartGiftCheck').addEventListener('change',renderCartUI);
    document.getElementById('cartCheckout').addEventListener('click',event=>{if(!cart.length)event.preventDefault();});
    document.getElementById('customForm').addEventListener('input',()=>{updateSimulatorPreview();if(document.getElementById('simDetailInput').value.trim())setDetailError(false);});
    // Sem nenhum detalhe a conversa começa no escuro; o link só segue com a ideia descrita.
    function setDetailError(show){const input=document.getElementById('simDetailInput'),error=document.getElementById('detailError');error.hidden=!show;input.setAttribute('aria-invalid',String(show));}
    document.getElementById('customWhatsApp').addEventListener('click',event=>{const input=document.getElementById('simDetailInput');if(input.value.trim())return;event.preventDefault();setDetailError(true);input.focus();});
    document.getElementById('customForm').addEventListener('submit',event=>{event.preventDefault();document.getElementById('customWhatsApp').click();});
    for(const dialog of document.querySelectorAll('dialog')){trapFocus(dialog);dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();});}
    window.addEventListener('storage',event=>{if(event.key===STORAGE_KEY || event.key===null){cart=loadCart();renderCartUI();}});
    document.getElementById('year').textContent=new Date().getFullYear();renderProducts();updateSimulatorPreview();renderCartUI();initHero();initRail();
