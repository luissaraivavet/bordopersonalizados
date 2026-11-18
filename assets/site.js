'use strict';
    // Sem o conteúdo (rede instável, bloqueio), a página avisa e oferece o WhatsApp em vez de ficar vazia.
    const content = window.BORDO_CONTENT || (() => {
      const box=document.getElementById('catalogSections'), whats=document.getElementById('customWhatsApp');
      if(box){box.innerHTML='<p class="wrap catalog-fallback">Não conseguimos carregar as coleções agora. Recarregue a página ou <a></a>.</p>';const link=box.querySelector('a');link.textContent='fale com a Bordô pelo WhatsApp';link.href=whats?whats.href:'https://wa.me/';link.target='_blank';link.rel='noopener';}
      throw new Error('Bordô: assets/content.js não carregou.');
    })();
    const settings = content.settings;
    const PHONE = settings.whatsapp;
    const STORAGE_KEY = 'bordo_cart_v2';
    const GIFT_PRICE = settings.giftPrice;
    const collections = content.collections.filter(item => item.published);
    const products = content.products.filter(item => item.published && collections.some(group => group.id === item.collection));
    const pixPrice = value => Math.round(Math.round(value * 100) * (100 - settings.pixDiscount) / 100) / 100;
    const money = value => value.toLocaleString('pt-BR', {style:'currency', currency:'BRL'});
    const icon = name => `<img class="icon" src="assets/icons/${name}.svg" alt="">`;
    const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    // Títulos do catálogo usam travessão entre nome e motivo; na página viram duas linhas ou vírgula.
    const plain = value => String(value).replace(/\s+[—–]\s+/g, ', ');
    const titleHTML = value => { const [name, ...rest] = String(value).split(/\s+[—–]\s+/); return rest.length ? `${escapeHTML(name)}<span class="visually-hidden">, </span><span class="product-sub">${escapeHTML(rest.join(', '))}</span>` : escapeHTML(name); };
    // A opção genérica do catálogo não descreve a peça; ela fica fora das legendas e da mensagem.
    const isPlaceholderOption = option => /^acabamento a (confirmar|combinar)/i.test(option || '');
    const whatsApp = message => `https://wa.me/${PHONE}?text=${encodeURIComponent(message)}`;
    let toastTimer;
    function notify(message) { const toast=document.getElementById('toast'); toast.textContent=message; toast.hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>{toast.hidden=true;},3500); }
    function productCard(p) {
      const title=escapeHTML(plain(p.title)), image=escapeHTML(p.image), id=escapeHTML(p.id);
      if(p.bundle) {
        const members=p.bundle.map(id=>products.find(item=>item.id===id)).filter(Boolean);
        const photos=members.map(item=>`<img src="${escapeHTML(item.image)}" alt="${escapeHTML(plain(item.title))}" width="600" height="600" loading="lazy">`).join('');
        const card=productCard({...p,bundle:null});
        return card.replace(/<figure class="product-figure">[\s\S]*?<\/figure>/, `<figure class="product-figure kit-figure"><div class="kit-images">${photos}</div></figure>`);
      }
      return `<article class="product"><figure class="product-figure"><img src="${image}" alt="${title}" width="600" height="600" loading="lazy"><button class="icon-button zoom-button" data-zoom="${image}" data-title="${title}" aria-label="Ampliar ${title}" title="Ampliar imagem">${icon('zoom-in')}</button></figure><div class="product-info"><h3>${titleHTML(p.title)}</h3><p>${escapeHTML(p.description.split(/(?<=[.!?])\s/)[0])}</p>${p.description.split(/(?<=[.!?])\s/).length > 1 ? `<details class="product-details"><summary>Detalhes da peça</summary><p>${escapeHTML(p.description)}</p></details>` : ''}${Number.isFinite(p.price) ? `<div class="product-price"><strong>${money(p.price)}</strong><small>${money(pixPrice(p.price))} no Pix</small></div>${p.options.length > 1 ? `<label class="field-label" for="var-${id}">Opção da peça</label><select id="var-${id}">${p.options.map(o => `<option>${escapeHTML(o)}</option>`).join('')}</select>` : `<p class="product-option">${escapeHTML(plain(p.options[0] || 'Detalhes no atendimento'))}</p>`.replace(/<p class="product-option">Acabamento a (confirmar|combinar)[^<]*<\/p>/i,'')}<button class="button secondary" type="button" data-add="${id}">${icon('plus')} Adicionar à sacola</button>` : `<a class="text-link" href="#personalizados" data-inquiry="Gostaria de consultar: ${title}.">Quero este encanto ${icon('arrow-right')}</a>`}</div></article>`;
    }
    function renderProducts() {
      document.querySelector('.dropdown').innerHTML = collections.map(c => `<a href="#${escapeHTML(c.id)}">${escapeHTML(c.name)}</a>`).join('');
      document.querySelector('.collection-grid').innerHTML = [...collections].sort((a,b) => Number(b.featured) - Number(a.featured)).map(c => `<a class="collection-link" href="#${escapeHTML(c.id)}"><figure class="collection-photo"><img src="${escapeHTML(c.image)}" alt="" width="128" height="160"></figure><span class="collection-name">${escapeHTML(c.name)}</span></a>`).join('');
      // No celular a faixa rola: o esmaecido na borda some quando chega ao fim.
      const strip=document.querySelector('.collection-grid');
      const stripEdge=()=>strip.classList.toggle('is-end',strip.scrollLeft+strip.clientWidth>=strip.scrollWidth-4);
      strip.addEventListener('scroll',stripEdge,{passive:true}); window.addEventListener('resize',stripEdge); stripEdge();
      document.getElementById('catalogSections').innerHTML = collections.map(c => `<section class="section ${escapeHTML(c.id)}" id="${escapeHTML(c.id)}" aria-labelledby="${escapeHTML(c.id)}Title"><div class="wrap"><div class="section-heading"><h2 id="${escapeHTML(c.id)}Title">${escapeHTML(c.name)}</h2><div><p class="lead">${escapeHTML(c.description)}</p><a class="text-link" href="#personalizados">Conversar sobre uma peça ${icon('arrow-up-right')}</a></div></div><div class="product-grid" id="grid-${escapeHTML(c.id)}">${products.filter(p => p.collection === c.id).map((p,index) => productCard(p).replace('<article class="product">', `<article class="product"${index >= 8 ? ' hidden data-extra-product' : ''}>`)).join('')}</div>${products.filter(p => p.collection === c.id).length > 8 ? `<button class="button secondary collection-more" type="button" data-expand="${escapeHTML(c.id)}" aria-expanded="false" aria-controls="grid-${escapeHTML(c.id)}">Ver coleção completa (${products.filter(p => p.collection === c.id).length} peças)</button>` : ''}<p class="collection-note">Disponibilidade, frete, materiais e prazo são confirmados no atendimento.</p>${c.id === 'sinfonia' ? document.getElementById('filmTemplate').innerHTML : ''}</div></section>`).join('');
      // A cidade fica na linha de apoio: a Bordô vende para todo o Brasil.
      const head=escapeHTML(settings.headline), lastWord=head.lastIndexOf(' ');
      document.getElementById('pageTitle').innerHTML=lastWord>0 ? `${head.slice(0,lastWord)} <em>${head.slice(lastWord+1)}</em>` : head;
      document.querySelector('.intro p').textContent=settings.intro;
      document.querySelector('.intro .intro-place').textContent=`Bordados em ${settings.location}, com envio para todo o Brasil.`;
      const story=document.querySelector('.story-copy'), link=story.querySelector('a');
      story.querySelectorAll('p').forEach(p=>p.remove());
      const storyParts=settings.story.split(/\n\s*\n/), storyMore=document.createElement('details');
      storyMore.className='story-more';storyMore.innerHTML='<summary>Ler a história completa</summary>';
      storyParts.forEach((text,index)=>{const p=document.createElement('p');p.textContent=text;if(index)storyMore.append(p);else story.insertBefore(p,link);});
      if(storyParts.length>1)story.insertBefore(storyMore,link);
      document.getElementById('storyPortrait').src=settings.storyImage||'assets/priscila-presentes.png';
      document.getElementById('storySecondary').src=settings.storyImageSecondary||'assets/priscila-sinfonia.png';
      document.querySelectorAll('a[href*="instagram.com"]').forEach(a=>a.href=settings.instagram);
      document.querySelectorAll('a[href^="https://wa.me/"]').forEach(a=>a.href=whatsApp('Olá, Bordô! Gostaria de saber mais sobre uma encomenda.'));
      const contact=document.querySelector('.footer-main>div:last-child a');
      contact.textContent=`WhatsApp: +${PHONE}`;
      document.querySelector('.footer-main>div:last-child p').textContent=`${settings.location}. Atendimento online e por encomenda, com envio para todo o Brasil.`;
      document.querySelector('.footer-main>div:first-child p').textContent=`Laços e bordados personalizados. Atendimento online, por encomenda. ${settings.location}.`;
      document.querySelector('.gift span').textContent=`Adicionar embalagem kraft para presente (+ ${money(GIFT_PRICE)})`;
      document.querySelector('#giftTotalRow span:last-child').textContent=money(GIFT_PRICE);
      document.querySelector('.totals .pix span').textContent=`Ou no Pix (${settings.pixDiscount}% nas peças)`;
      
      const footerCollections=document.getElementById('footerCollections');
      footerCollections.innerHTML=collections.map(c=>`<a href="#${escapeHTML(c.id)}">${escapeHTML(c.name)}</a>`).join('');
      document.getElementById('paymentAnswer').textContent=`A sacola apresenta o total e a alternativa com ${settings.pixDiscount}% de desconto no Pix sobre as peças. A embalagem para presente é opcional, por ${money(GIFT_PRICE)} por pedido. Frete e condições finais são confirmados pelo WhatsApp. Não há cobrança pelo site.`;
      const reviews=content.testimonials.filter(i=>i.published), articles=content.articles.filter(i=>i.published);
      document.getElementById('editorialSections').innerHTML=(reviews.length ? `<section class="section"><div class="wrap"><div class="section-heading"><h2>Quem recebeu um encanto</h2></div><div class="product-grid">${reviews.map(r=>`<blockquote><p>“${escapeHTML(r.text)}”</p><footer>${escapeHTML(r.name)}</footer></blockquote>`).join('')}</div></div></section>` : '')+(articles.length ? `<section class="section"><div class="wrap"><div class="section-heading"><h2>Histórias e cuidados</h2></div><div class="product-grid">${articles.map(a=>`<article><img src="${escapeHTML(a.image)}" alt="${escapeHTML(a.title)}" loading="lazy" style="width:100%;aspect-ratio:4/3;object-fit:cover"><h3 style="margin-top:18px">${escapeHTML(a.title)}</h3><p>${escapeHTML(a.excerpt)}</p><details class="article-text"><summary class="text-link">Ler artigo ${icon('arrow-right')}</summary>${a.body.split(/\n\s*\n/).map(p=>`<p>${escapeHTML(p)}</p>`).join('')}</details></article>`).join('')}</div></div></section>` : '');
      document.getElementById('extraLinks').innerHTML=content.links.filter(l=>l.published).map(l=>`<a href="${escapeHTML(l.url)}" target="_blank" rel="noopener">${escapeHTML(l.title)}</a>`).join('');
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
    // Marca a peça recém-adicionada ou alterada para a sacola animar só ela.
    let cartMark=null;
    function saveCart(){ try{localStorage.setItem(STORAGE_KEY,JSON.stringify(cart));}catch{notify('Sua sacola funciona nesta visita, mas não pôde ser salva neste navegador.');} renderCartUI(); cartMark=null; }
    function cartTotals(){ const subtotal=cart.reduce((sum,item)=>sum+item.price*item.qty,0); const gift=cart.length && document.getElementById('cartGiftCheck').checked ? GIFT_PRICE : 0; return {subtotal,gift,total:subtotal+gift,pix:pixPrice(subtotal)+gift}; }
    function checkoutMessage(){
      const totals=cartTotals();
      return `Olá, Bordô! Gostaria de consultar este pedido:\n\n`+cart.map(item=>`${item.qty}x ${item.title}\n${isPlaceholderOption(item.variation)?'':`Opção: ${item.variation}\n`}Valor: ${money(item.price*item.qty)}`).join('\n\n')+`\n\nSubtotal: ${money(totals.subtotal)}\n`+(totals.gift?`Embalagem kraft para presente: ${money(totals.gift)}\n`:'Sem embalagem adicional\n')+`Total estimado: ${money(totals.total)}\nAlternativa no Pix (${settings.pixDiscount}% de desconto nas peças): ${money(totals.pix)}\n\nPor favor, confirmem disponibilidade, prazo, frete e formas de pagamento.`;
    }
    function renderCartUI(){
      const list=document.getElementById('cartItemsList'); const count=cart.reduce((sum,item)=>sum+item.qty,0); const totals=cartTotals();
      document.getElementById('cartCountBadge').textContent=count;
      document.getElementById('bagButton').setAttribute('aria-label',`Abrir sacola, ${count} ${count===1?'item':'itens'}`);
      list.innerHTML=cart.length ? cart.map((item,index)=>`<article class="bag-item${cartMark?.index===index?` is-${cartMark.kind}`:''}"><img src="${item.imgPath}" alt="${escapeHTML(plain(item.title))}" width="84" height="105"><div><h3>${escapeHTML(plain(item.title))}</h3>${isPlaceholderOption(item.variation)?'':`<p>${escapeHTML(item.variation)}</p>`}<strong>${money(item.price*item.qty)}</strong><div class="quantity"><button class="icon-button" data-qty="${index}" data-delta="-1" aria-label="Diminuir quantidade de ${escapeHTML(item.title)}" title="Diminuir quantidade">${icon('minus')}</button><output aria-label="Quantidade">${item.qty}</output><button class="icon-button" data-qty="${index}" data-delta="1" aria-label="Aumentar quantidade de ${escapeHTML(item.title)}" title="Aumentar quantidade">${icon('plus')}</button><button class="icon-button remove" data-remove="${index}" aria-label="Remover ${escapeHTML(item.title)}" title="Remover peça">${icon('trash-2')}</button></div></div></article>`).join(''):`<div class="empty">${icon('shopping-bag')}<p>Sua sacola está esperando<br>o primeiro encanto.</p><button class="button secondary" id="emptyCollection">Explorar a coleção ${icon('arrow-right')}</button><button class="text-link" type="button" id="emptyCustom">Ou descreva uma encomenda</button></div>`;
      document.getElementById('cartSubtotalText').textContent=money(totals.subtotal); document.getElementById('cartTotalText').textContent=money(totals.total); document.getElementById('cartPixText').textContent=money(totals.pix);
      document.getElementById('giftTotalRow').hidden=!totals.gift; document.getElementById('cartGiftCheck').disabled=!cart.length;
      // Uma sacola vazia não carrega a embalagem para o próximo pedido.
      if(!cart.length) document.getElementById('cartGiftCheck').checked=false;
      const checkout=document.getElementById('cartCheckout'); checkout.setAttribute('aria-disabled',String(!cart.length)); checkout.tabIndex=cart.length?0:-1; checkout.href=whatsApp(checkoutMessage());
    }
    function addToCart(id){
      const product=products.find(item=>item.id===id); if(!product || !Number.isFinite(product.price)) return;
      const variation=document.getElementById(`var-${id}`)?.value || product.options[0]; const existing=cart.find(item=>item.id===id && item.variation===variation);
      if(existing){if(existing.qty>=99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;} existing.qty++;cartMark={index:cart.indexOf(existing),kind:'changed'};}
      else {cart.push({id,title:product.title,price:product.price,variation,imgPath:product.image,qty:1});cartMark={index:cart.length-1,kind:'new'};}
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
    // One collection is open at a time; any link to a collection id switches to it.
    function showCollection(id){
      if(!collections.some(c=>c.id===id)) return false;
      document.querySelectorAll('#catalogSections>section').forEach(section=>{section.hidden=section.id!==id;if(section.hidden)section.querySelectorAll('video').forEach(video=>video.pause());});
      document.querySelectorAll('.collection-grid a').forEach(link=>{if(link.getAttribute('href')===`#${id}`){link.setAttribute('aria-current','true');link.scrollIntoView({block:'nearest',inline:'nearest'});}else link.removeAttribute('aria-current');});
      return true;
    }
    function closeMenu(){document.getElementById('mainNav').classList.remove('open');document.getElementById('menuButton').setAttribute('aria-expanded','false');document.getElementById('menuButton').setAttribute('aria-label','Abrir menu');document.querySelector('.collection-nav').open=false;}
    document.getElementById('menuButton').addEventListener('click',()=>{const open=document.getElementById('mainNav').classList.toggle('open');document.getElementById('menuButton').setAttribute('aria-expanded',String(open));document.getElementById('menuButton').setAttribute('aria-label',open?'Fechar menu':'Abrir menu');});
    document.getElementById('mainNav').addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
    document.addEventListener('keydown',event=>{if(event.key==='Escape'){const menuWasOpen=document.getElementById('mainNav').classList.contains('open');closeMenu();if(menuWasOpen)document.getElementById('menuButton').focus();}});
    document.addEventListener('click',event=>{
      const anchor=event.target.closest('a[href^="#"]');
      if(anchor && showCollection(anchor.getAttribute('href').slice(1)) && anchor.closest('.collection-grid')){event.preventDefault();history.replaceState(null,'',anchor.getAttribute('href'));}
      const button=event.target.closest('button');
      if(button?.dataset.expand){const grid=document.getElementById(`grid-${button.dataset.expand}`);const expanded=button.getAttribute('aria-expanded')==='true';grid.querySelectorAll('[data-extra-product]').forEach(item=>item.hidden=expanded);button.setAttribute('aria-expanded',String(!expanded));button.textContent=expanded?`Ver coleção completa (${grid.children.length} peças)`:'Mostrar menos';if(!expanded)grid.querySelector('[data-extra-product] button')?.focus();return;}
      if(button?.dataset.add){addToCart(button.dataset.add);return;}
      if(button?.dataset.close){document.getElementById(button.dataset.close).close();return;}
      if(button?.dataset.zoom){document.getElementById('lightboxImage').src=button.dataset.zoom;document.getElementById('lightboxImage').alt=button.dataset.title;document.getElementById('imageTitle').textContent=button.dataset.title;document.getElementById('imageDialog').showModal();return;}
      if(button?.hasAttribute('data-qty')){const index=Number(button.dataset.qty);const delta=Number(button.dataset.delta);const item=cart[index];if(!item)return;if(item.qty+delta>99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;}item.qty+=delta;if(item.qty<=0)cart.splice(index,1);else cartMark={index,kind:'changed'};saveCart();const replacement=document.querySelector(`[data-qty="${index}"][data-delta="${delta}"]`);(replacement||document.querySelector('[data-close="cartDrawer"]')).focus();return;}
      if(button?.hasAttribute('data-remove')){cart.splice(Number(button.dataset.remove),1);saveCart();document.querySelector('[data-close="cartDrawer"]').focus();return;}
      if(button?.id==='emptyCustom'){document.getElementById('cartDrawer').close();document.getElementById('personalizados').scrollIntoView();document.getElementById('simDetailInput').focus({preventScroll:true});return;}
      if(button?.id==='emptyCollection'){document.getElementById('cartDrawer').close();document.getElementById('colecoes').scrollIntoView();return;}
      const inquiry=event.target.closest('[data-inquiry]');if(inquiry){const project=inquiry.dataset.project||'Laços e coleções';document.querySelectorAll('input[name="project"]').forEach(input=>input.checked=input.value===project);document.getElementById('simDetailInput').value=inquiry.dataset.inquiry;updateSimulatorPreview();}
      if(!event.target.closest('.collection-nav')) document.querySelector('.collection-nav').open=false;
    });
    document.getElementById('bagButton').addEventListener('click',()=>{closeMenu();document.getElementById('cartDrawer').showModal();});
    document.getElementById('cartGiftCheck').addEventListener('change',renderCartUI);
    document.getElementById('cartCheckout').addEventListener('click',event=>{if(!cart.length)event.preventDefault();});
    document.getElementById('customForm').addEventListener('input',updateSimulatorPreview);
    // Sem nenhum detalhe a conversa começa no escuro; o link só segue com a ideia descrita.
    function setDetailError(show){document.getElementById('detailError').hidden=!show;document.getElementById('simDetailInput').setAttribute('aria-invalid',String(show));}
    document.getElementById('customForm').addEventListener('input',()=>{if(document.getElementById('simDetailInput').value.trim())setDetailError(false);});
    document.getElementById('customWhatsApp').addEventListener('click',event=>{const input=document.getElementById('simDetailInput');if(input.value.trim())return;event.preventDefault();setDetailError(true);input.focus();});
    document.getElementById('customForm').addEventListener('submit',event=>{event.preventDefault();document.getElementById('customWhatsApp').click();});
    for(const dialog of document.querySelectorAll('dialog')) dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();});
    window.addEventListener('storage',event=>{if(event.key===STORAGE_KEY || event.key===null){cart=loadCart();renderCartUI();}});
    window.addEventListener('hashchange',()=>{showCollection(location.hash.slice(1));});
    document.getElementById('year').textContent=new Date().getFullYear();renderProducts();updateSimulatorPreview();renderCartUI();
    showCollection(location.hash.slice(1)) || showCollection((collections.find(c=>c.featured)||collections[0]).id);
    // Lookbook das cores Mãe & Rainha: cada botão troca a foto da seção.
    (function(){
      const list=document.getElementById('toneList'), frame=document.getElementById('tonePhoto'), img=document.getElementById('toneImg'), caption=document.getElementById('toneCaption');
      if(!list||!frame||!img) return;
      const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      let swap=null;
      list.addEventListener('click',event=>{
        const button=event.target.closest('.tone'); if(!button||button.getAttribute('aria-pressed')==='true') return;
        list.querySelectorAll('.tone').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
        const apply=()=>{img.src=button.dataset.src;img.alt=button.dataset.alt;caption.textContent=button.dataset.caption;frame.classList.toggle('is-solo',!button.classList.contains('tone-all'));};
        new Image().src=button.dataset.src;
        if(reduce){apply();return;}
        clearTimeout(swap); frame.classList.add('is-changing');
        swap=setTimeout(()=>{apply();void frame.offsetWidth;frame.classList.remove('is-changing');},520);
      });
    })();
    // Lanterna da capa: o ponteiro abre um círculo com o risco do bordado (só com mouse e movimento liberado).
    (function(){
      const hero=document.querySelector('.hero'), risco=document.querySelector('.hero-risco');
      if(!hero||!risco||!matchMedia('(hover:hover) and (pointer:fine) and (min-width:60.0625rem) and (prefers-reduced-motion:no-preference)').matches) return;
      const RAIO=240, SEGUE=.14, ABRE=.1;
      let x=0,y=0,r=0,tx=0,ty=0,tr=0,dentro=false,quadro=0;
      const pinta=()=>{risco.style.setProperty('--lx',x.toFixed(1)+'px');risco.style.setProperty('--ly',y.toFixed(1)+'px');risco.style.setProperty('--lr',r.toFixed(1)+'px');};
      const passo=()=>{x+=(tx-x)*SEGUE;y+=(ty-y)*SEGUE;r+=(tr-r)*ABRE;pinta();
        quadro=(Math.abs(tx-x)>.3||Math.abs(ty-y)>.3||Math.abs(tr-r)>.3)?requestAnimationFrame(passo):0;};
      hero.addEventListener('pointermove',e=>{
        const box=risco.getBoundingClientRect(), k=risco.offsetWidth/box.width;
        tx=(e.clientX-box.left)*k; ty=(e.clientY-box.top)*k; tr=RAIO;
        if(!dentro){x=tx;y=ty;dentro=true;}
        if(!quadro) quadro=requestAnimationFrame(passo);
      });
      hero.addEventListener('pointerleave',()=>{tr=0;dentro=false;if(!quadro) quadro=requestAnimationFrame(passo);});
    })();
    // Filme da capa no celular: o risco a lápis se desenha e vira a foto bordada, uma vez.
    (function(){
      const film=document.querySelector('.hero-film');
      const lite=navigator.connection&&navigator.connection.saveData;
      if(!film||lite||!matchMedia('(max-width:60rem) and (prefers-reduced-motion:no-preference)').matches) return;
      const fim=()=>{film.classList.add('is-done');setTimeout(()=>film.remove(),600);};
      film.addEventListener('ended',fim);
      film.addEventListener('error',()=>film.remove());
      film.addEventListener('playing',()=>film.classList.add('is-on'),{once:true});
      film.src='assets/hero-risco.mp4';
      const p=film.play(); if(p&&p.catch) p.catch(()=>film.remove());
    })();
    // Reveal on scroll runs only after everything above succeeded, so a failed script never hides content.
    if('IntersectionObserver' in window){
      document.documentElement.classList.add('js');
      const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-in');reveal.unobserve(entry.target);}}),{rootMargin:'0px 0px -8% 0px'});
      document.querySelectorAll('[data-reveal]').forEach(element=>reveal.observe(element));
    }
