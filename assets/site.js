'use strict';
    const content = window.BORDO_CONTENT;
    const settings = content.settings;
    const PHONE = settings.whatsapp;
    const STORAGE_KEY = 'bordo_cart_v2';
    const GIFT_PRICE = settings.giftPrice;
    const collections = content.collections.filter(item => item.published);
    const products = content.products.filter(item => item.published && collections.some(group => group.id === item.collection));
    const money = value => value.toLocaleString('pt-BR', {style:'currency', currency:'BRL'});
    const icon = name => `<img class="icon" src="assets/icons/${name}.svg" alt="">`;
    const escapeHTML = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
    const whatsApp = message => `https://wa.me/${PHONE}?text=${encodeURIComponent(message)}`;
    let toastTimer;
    function notify(message) { const toast=document.getElementById('toast'); toast.textContent=message; toast.hidden=false; clearTimeout(toastTimer); toastTimer=setTimeout(()=>{toast.hidden=true;},3500); }
    function productCard(p) {
      const title=escapeHTML(p.title), image=escapeHTML(p.image), id=escapeHTML(p.id);
      if(p.bundle) {
        const members=p.bundle.map(id=>products.find(item=>item.id===id)).filter(Boolean);
        const photos=members.map(item=>`<img src="${escapeHTML(item.image)}" alt="${escapeHTML(item.title)}" width="600" height="600" loading="lazy">`).join('');
        const card=productCard({...p,bundle:null});
        return card.replace(/<figure class="product-figure">[\s\S]*?<\/figure>/, `<figure class="product-figure kit-figure"><div class="kit-images">${photos}</div></figure>`);
      }
      return `<article class="product"><figure class="product-figure"><img src="${image}" alt="${title}" width="600" height="600" loading="lazy"><button class="icon-button zoom-button" data-zoom="${image}" data-title="${title}" aria-label="Ampliar ${title}" title="Ampliar imagem">${icon('zoom-in')}</button></figure><div class="product-info"><h3>${title}</h3><p>${escapeHTML(p.description)}</p>${Number.isFinite(p.price) ? `<div class="product-price"><strong>${money(p.price)}</strong><small>${money(p.price*(1-settings.pixDiscount/100))} no Pix</small></div><label class="field-label" for="var-${id}">Opção da peça</label><select id="var-${id}">${p.options.map(o => `<option>${escapeHTML(o)}</option>`).join('')}</select><button class="button" data-add="${id}">${icon('plus')} Adicionar à sacola</button>` : `<a class="text-link" href="#personalizados" data-inquiry="Gostaria de consultar: ${title}.">Quero este encanto ${icon('arrow-right')}</a>`}</div></article>`;
    }
    function renderProducts() {
      document.querySelector('.dropdown').innerHTML = collections.map(c => `<a href="#${escapeHTML(c.id)}">${escapeHTML(c.name)}</a>`).join('');
      document.querySelector('.collection-grid').innerHTML = collections.filter(c => c.featured).map((c,index) => `<a class="collection-link" href="#${escapeHTML(c.id)}"><figure class="collection-photo"><img src="${escapeHTML(c.image)}" alt="${escapeHTML(c.name)}" width="1400" height="850" ${index ? '' : 'fetchpriority="high"'}></figure><div class="collection-caption"><h2>${escapeHTML(c.name)}</h2><span class="text-link">Conhecer a coleção ${icon('arrow-right')}</span></div></a>`).join('');
      document.getElementById('catalogSections').innerHTML = collections.map(c => `<section class="section ${escapeHTML(c.id)}" id="${escapeHTML(c.id)}" aria-labelledby="${escapeHTML(c.id)}Title"><div class="wrap"><div class="section-heading"><div><div class="eyebrow">Uma coleção Bordô</div><h2 id="${escapeHTML(c.id)}Title">${escapeHTML(c.name)}</h2><p>${escapeHTML(c.description)}</p></div><a class="text-link" href="#personalizados">Conversar sobre uma peça ${icon('arrow-up-right')}</a></div><div class="product-grid">${products.filter(p => p.collection === c.id).map(productCard).join('')}</div><p class="collection-note">Disponibilidade, frete, materiais e prazo são confirmados no atendimento.</p>${c.id === 'sinfonia' ? document.getElementById('filmTemplate').innerHTML : ''}</div></section>`).join('');
      document.getElementById('pageTitle').textContent=settings.headline;
      document.querySelector('.intro p').textContent=settings.intro;
      const story=document.querySelector('.story-copy'), link=story.querySelector('a');
      story.querySelectorAll('p').forEach(p=>p.remove());
      settings.story.split(/\n\s*\n/).forEach(text=>{const p=document.createElement('p');p.textContent=text;story.insertBefore(p,link);});
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
      document.querySelector('.intro>.button').href='#colecoes';
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
    function saveCart(){ try{localStorage.setItem(STORAGE_KEY,JSON.stringify(cart));}catch{notify('Sua sacola funciona nesta visita, mas não pôde ser salva neste navegador.');} renderCartUI(); }
    function cartTotals(){ const subtotal=cart.reduce((sum,item)=>sum+item.price*item.qty,0); const gift=cart.length && document.getElementById('cartGiftCheck').checked ? GIFT_PRICE : 0; return {subtotal,gift,total:subtotal+gift,pix:Math.round(subtotal*(100-settings.pixDiscount))/100+gift}; }
    function checkoutMessage(){
      const totals=cartTotals();
      return `Olá, Bordô! Gostaria de consultar este pedido:\n\n`+cart.map(item=>`${item.qty}x ${item.title}\nAcabamento: ${item.variation}\nValor: ${money(item.price*item.qty)}`).join('\n\n')+`\n\nSubtotal: ${money(totals.subtotal)}\n`+(totals.gift?`Embalagem kraft para presente: ${money(totals.gift)}\n`:'Sem embalagem adicional\n')+`Total estimado: ${money(totals.total)}\nAlternativa no Pix (${settings.pixDiscount}% de desconto nas peças): ${money(totals.pix)}\n\nPor favor, confirmem disponibilidade, prazo, frete e formas de pagamento.`;
    }
    function renderCartUI(){
      const list=document.getElementById('cartItemsList'); const count=cart.reduce((sum,item)=>sum+item.qty,0); const totals=cartTotals();
      document.getElementById('cartCountBadge').textContent=count;
      document.getElementById('bagButton').setAttribute('aria-label',`Abrir sacola, ${count} ${count===1?'item':'itens'}`);
      list.innerHTML=cart.length ? cart.map((item,index)=>`<article class="bag-item"><img src="${item.imgPath}" alt="${escapeHTML(item.title)}" width="84" height="105"><div><h3>${escapeHTML(item.title)}</h3><p>${escapeHTML(item.variation)}</p><strong>${money(item.price*item.qty)}</strong><div class="quantity"><button class="icon-button" data-qty="${index}" data-delta="-1" aria-label="Diminuir quantidade de ${escapeHTML(item.title)}" title="Diminuir quantidade">${icon('minus')}</button><output aria-label="Quantidade">${item.qty}</output><button class="icon-button" data-qty="${index}" data-delta="1" aria-label="Aumentar quantidade de ${escapeHTML(item.title)}" title="Aumentar quantidade">${icon('plus')}</button><button class="icon-button remove" data-remove="${index}" aria-label="Remover ${escapeHTML(item.title)}" title="Remover peça">${icon('trash-2')}</button></div></div></article>`).join(''):`<div class="empty">${icon('shopping-bag')}<p>Sua sacola está esperando<br>o primeiro encanto.</p><button class="button secondary" id="emptyCollection">Explorar a coleção ${icon('arrow-right')}</button></div>`;
      document.getElementById('cartSubtotalText').textContent=money(totals.subtotal); document.getElementById('cartTotalText').textContent=money(totals.total); document.getElementById('cartPixText').textContent=money(totals.pix);
      document.getElementById('giftTotalRow').hidden=!totals.gift; document.getElementById('cartGiftCheck').disabled=!cart.length;
      const checkout=document.getElementById('cartCheckout'); checkout.setAttribute('aria-disabled',String(!cart.length)); checkout.tabIndex=cart.length?0:-1; checkout.href=whatsApp(checkoutMessage());
    }
    function addToCart(id){
      const product=products.find(item=>item.id===id); if(!product || !Number.isFinite(product.price)) return;
      const variation=document.getElementById(`var-${id}`).value; const existing=cart.find(item=>item.id===id && item.variation===variation);
      if(existing){if(existing.qty>=99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;} existing.qty++;}
      else cart.push({id,title:product.title,price:product.price,variation,imgPath:product.image,qty:1});
      saveCart(); document.getElementById('cartDrawer').showModal();
    }
    function updateSimulatorPreview(){
      const form=document.getElementById('customForm'); const data=new FormData(form); const detail=String(data.get('details')||'').trim();
      const summary=`Projeto: ${data.get('project')}\nQuantidade: ${data.get('quantity')}`+(detail?`\nDetalhes: ${detail}`:'');
      document.getElementById('simMsgPreviewText').textContent=summary;
      document.getElementById('customWhatsApp').href=whatsApp(`Olá! Vim pelo site da Bordô e gostaria de um orçamento personalizado.\n\n${summary}\n\nPodem me informar possibilidades, valores e prazo?`);
    }
    function closeMenu(){document.getElementById('mainNav').classList.remove('open');document.getElementById('menuButton').setAttribute('aria-expanded','false');document.getElementById('menuButton').setAttribute('aria-label','Abrir menu');document.querySelector('.collection-nav').open=false;}
    document.getElementById('menuButton').addEventListener('click',()=>{const open=document.getElementById('mainNav').classList.toggle('open');document.getElementById('menuButton').setAttribute('aria-expanded',String(open));document.getElementById('menuButton').setAttribute('aria-label',open?'Fechar menu':'Abrir menu');});
    document.querySelectorAll('#mainNav a').forEach(link=>link.addEventListener('click',closeMenu));
    document.addEventListener('keydown',event=>{if(event.key==='Escape'){const menuWasOpen=document.getElementById('mainNav').classList.contains('open');closeMenu();if(menuWasOpen)document.getElementById('menuButton').focus();}});
    document.addEventListener('click',event=>{
      const button=event.target.closest('button');
      if(button?.dataset.add){addToCart(button.dataset.add);return;}
      if(button?.dataset.close){document.getElementById(button.dataset.close).close();return;}
      if(button?.dataset.zoom){document.getElementById('lightboxImage').src=button.dataset.zoom;document.getElementById('lightboxImage').alt=button.dataset.title;document.getElementById('imageTitle').textContent=button.dataset.title;document.getElementById('imageDialog').showModal();return;}
      if(button?.hasAttribute('data-qty')){const index=Number(button.dataset.qty);const delta=Number(button.dataset.delta);const item=cart[index];if(!item)return;if(item.qty+delta>99){notify('Para mais de 99 peças, consulte um projeto personalizado.');return;}item.qty+=delta;if(item.qty<=0)cart.splice(index,1);saveCart();const replacement=document.querySelector(`[data-qty="${index}"][data-delta="${delta}"]`);(replacement||document.querySelector('[data-close="cartDrawer"]')).focus();return;}
      if(button?.hasAttribute('data-remove')){cart.splice(Number(button.dataset.remove),1);saveCart();document.querySelector('[data-close="cartDrawer"]').focus();return;}
      if(button?.id==='emptyCollection'){document.getElementById('cartDrawer').close();document.getElementById('colecoes').scrollIntoView();return;}
      const inquiry=event.target.closest('[data-inquiry]');if(inquiry){document.querySelector('input[name="project"][value="Laços e coleções"]').checked=true;document.getElementById('simDetailInput').value=inquiry.dataset.inquiry;updateSimulatorPreview();}
      if(!event.target.closest('.collection-nav')) document.querySelector('.collection-nav').open=false;
    });
    document.getElementById('bagButton').addEventListener('click',()=>{closeMenu();document.getElementById('cartDrawer').showModal();});
    document.getElementById('cartGiftCheck').addEventListener('change',renderCartUI);
    document.getElementById('cartCheckout').addEventListener('click',event=>{if(!cart.length)event.preventDefault();});
    document.getElementById('customForm').addEventListener('input',updateSimulatorPreview);
    document.getElementById('customForm').addEventListener('submit',event=>event.preventDefault());
    for(const dialog of document.querySelectorAll('dialog')) dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const rect=dialog.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)dialog.close();});
    window.addEventListener('storage',event=>{if(event.key===STORAGE_KEY || event.key===null){cart=loadCart();renderCartUI();}});
    document.getElementById('year').textContent=new Date().getFullYear();renderProducts();updateSimulatorPreview();renderCartUI();
