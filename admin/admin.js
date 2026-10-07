'use strict';
const sections={products:'Produtos',collections:'Coleções',media:'Fotos',testimonials:'Depoimentos',articles:'Artigos',links:'Links',settings:'Configurações'};
const schemas={
  products:[['title','Nome'],['collection','Coleção','collection'],['price','Preço em reais','price'],['description','Descrição','textarea'],['options','Opções da peça (uma por linha)','options'],['image','Foto','image'],['illustrative','Imagem ilustrativa','bool'],['published','Ativo no site','bool']],
  collections:[['name','Nome'],['description','Descrição','textarea'],['image','Capa','image'],['featured','Destaque na abertura','bool'],['illustrative','Imagem ilustrativa','bool'],['published','Ativa no site','bool']],
  testimonials:[['name','Nome do cliente'],['text','Depoimento autorizado','textarea'],['published','Ativo no site','bool']],
  articles:[['title','Título'],['excerpt','Resumo','textarea'],['body','Artigo','long'],['image','Foto','image'],['published','Ativo no site','bool']],
  links:[['title','Nome'],['url','Endereço https://','url'],['published','Ativo no site','bool']],
  settings:[['headline','Título da página'],['intro','Texto de abertura'],['location','Cidade e estado'],['whatsapp','WhatsApp (55 + DDD + número)'],['instagram','Instagram','url'],['pixDiscount','Desconto Pix (%)','number'],['giftPrice','Embalagem para presente (R$)','number'],['story','História da marca','long']]
};
let data,revision,csrf,active='products',dirty=false,editing=null,imageField=null,busy=false;
const $=id=>document.getElementById(id);
const escape=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const icon=name=>`<img src="../assets/icons/${name}.svg" alt="">`;
const tool=(action,name,label,id)=>`<button class="icon-button" data-action="${action}" data-id="${escape(id)}" aria-label="${escape(label)}" title="${escape(label)}">${icon(name)}</button>`;
function toast(text){$('toast').textContent=text;$('toast').hidden=false;setTimeout(()=>$('toast').hidden=true,7000);}
function changed(){dirty=true;$('saveState').textContent='Alterações ainda não salvas';}
async function request(path,body){
  const response=await fetch(path,body?{method:'POST',headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},body:JSON.stringify(body)}:{});
  const result=await response.json();if(!response.ok)throw Error(result.error||'A operação não foi concluída.');return result;
}
function fieldHTML(field,item){
  const [key,label,type='text']=field,value=item[key];
  if(type==='bool')return `<label class="switch field wide"><input type="checkbox" name="${key}" ${value?'checked':''}>${label}</label>`;
  if(type==='image')return `<div class="field wide"><span>${label}</span><div class="photo-field"><img id="selectedPhoto" src="/${escape(value||'assets/brand-logo.png')}" alt="Foto selecionada"><input name="${key}" value="${escape(value||'')}" type="hidden"><button class="button secondary" type="button" data-action="choose-photo">${icon('plus')}Escolher foto</button></div></div>`;
  if(type==='collection')return `<label class="field">${label}<select name="${key}">${data.collections.map(c=>`<option value="${escape(c.id)}" ${value===c.id?'selected':''}>${escape(c.name)}</option>`).join('')}</select></label>`;
  if(['textarea','long','options'].includes(type))return `<label class="field wide">${label}<textarea name="${key}" rows="${type==='long'?8:3}" required maxlength="${type==='long'?20000:4000}">${escape(type==='options'?(value||['Padrão']).join('\n'):value)}</textarea></label>`;
  return `<label class="field">${label}<input name="${key}" value="${escape(value??'')}" type="${['price','number'].includes(type)?'number':type==='url'?'url':'text'}" ${['price','number'].includes(type)?'min="0" step="0.01"':''} ${type==='price'?'placeholder="Vazio: sob consulta"':'required'} maxlength="250"></label>`;
}
function parseForm(form,group,item){
  const values=new FormData(form),result={...item};
  for(const [key,,type] of schemas[group]){
    const value=values.get(key);
    result[key]=type==='bool'?values.has(key):type==='options'?String(value).split('\n').map(v=>v.trim()).filter(Boolean):['price','number'].includes(type)?(type==='price'&&value===''?null:Number(value)):String(value||'').trim();
  }
  return result;
}
function render(){
  $('sectionTitle').textContent=sections[active];$('search').value='';$('search').parentElement.hidden=active==='settings'||active==='media';$('create').hidden=active==='settings';$('create').innerHTML=icon('plus')+(active==='media'?'Enviar foto':'Adicionar');
  $('navigation').innerHTML=Object.entries(sections).map(([key,label])=>`<button data-section="${key}" ${key===active?'aria-current="page"':''}>${icon(({settings:'settings',media:'image',products:'shopping-bag',collections:'image',testimonials:'quote',articles:'file-text',links:'link'})[key])}${label}</button>`).join('');
  if(active==='settings'){$('content').innerHTML=`<form id="settingsForm" class="settings">${schemas.settings.map(field=>fieldHTML(field,data.settings)).join('')}<button class="button" type="submit">${icon('check')}Concluir ajustes</button></form>`;return;}
  if(active==='media'){showMedia('content',false);return;}renderList();
}
function renderList(){
  const query=$('search').value.toLocaleLowerCase('pt-BR'),items=data[active].filter(i=>JSON.stringify(i).toLocaleLowerCase('pt-BR').includes(query));
  $('content').innerHTML=items.length?`<div class="list">${items.map(item=>`<div class="row">${item.image?`<img class="row-photo" src="/${escape(item.image)}" alt="">`:`<span class="row-photo" style="display:grid;place-items:center">${icon('arrow-right')}</span>`}<div><h2>${escape(item.title||item.name)}</h2><p>${escape(item.description||item.excerpt||item.text||item.url||'')}</p></div><span class="price">${active==='products'?(item.price==null?'Sob consulta':Number(item.price).toLocaleString('pt-BR',{style:'currency',currency:'BRL'})):''}</span><span class="badge ${item.published?'':'draft'}">${item.published?'Ativo':'Oculto'}</span><div class="row-tools">${tool('up','arrow-up','Mover para cima',item.id)}${tool('down','arrow-down','Mover para baixo',item.id)}${tool('edit','pencil','Editar '+(item.title||item.name),item.id)}${tool('toggle','check',item.published?'Ocultar':'Ativar',item.id)}${tool('delete','trash-2','Excluir '+(item.title||item.name),item.id)}</div></div>`).join('')}</div>`:'<div class="empty">Nenhum item encontrado.</div>';
}
async function showMedia(target,selecting){
  try{const files=await request('/api/media');$(target).innerHTML=`<div class="media-grid">${files.map(path=>selecting?`<button data-image="${escape(path)}" aria-label="Selecionar ${escape(path.split('/').pop())}"><img src="/${escape(path)}" alt="${escape(path.split('/').pop())}" loading="lazy"></button>`:`<figure style="margin:0"><img src="/${escape(path)}" alt="${escape(path.split('/').pop())}" loading="lazy"><figcaption style="font-size:10px;overflow-wrap:anywhere">${escape(path.split('/').pop())}</figcaption></figure>`).join('')}</div>`;}catch(error){toast(error.message);}
}
function edit(id){
  const item=id?data[active].find(i=>i.id===id):{id:`${active}-${Date.now().toString(36)}`,published:false,illustrative:true,featured:false,options:['Padrão'],collection:data.collections[0]?.id};
  editing={group:active,id,isNew:!id,item};$('editorTitle').textContent=(id?'Editar ':'Adicionar ')+sections[active].toLowerCase();$('fields').innerHTML=schemas[active].map(field=>fieldHTML(field,item)).join('');$('editor').showModal();
}
async function save(){
  if(busy)return false;
  if(active==='settings'&&$('settingsForm')){
    if(!$('settingsForm').reportValidity())return false;
    data.settings=parseForm($('settingsForm'),'settings',data.settings);
  }
  busy=true;$('save').disabled=true;
  try{const result=await request('/api/save',{content:data,revision});revision=result.revision;dirty=false;$('saveState').textContent='Rascunho salvo às '+new Date().toLocaleTimeString('pt-BR');return true;}catch(error){toast(error.message);return false;}finally{busy=false;$('save').disabled=false;}
}
document.addEventListener('click',event=>{
  const close=event.target.closest('[data-close]');if(close){$(close.dataset.close).close();return;}
  const nav=event.target.closest('[data-section]');if(nav){
    if(active==='settings'&&$('settingsForm')){if(!$('settingsForm').reportValidity())return;const updated=parseForm($('settingsForm'),'settings',data.settings);if(JSON.stringify(updated)!==JSON.stringify(data.settings)){data.settings=updated;changed();}}
    active=nav.dataset.section;render();return;
  }
  const photo=event.target.closest('[data-image]');if(photo){imageField.value=photo.dataset.image;$('selectedPhoto').src='/'+photo.dataset.image;$('media').close();return;}
  const button=event.target.closest('[data-action]');if(!button)return;
  const action=button.dataset.action,id=button.dataset.id;
  if(action==='choose-photo'){imageField=$('editForm').elements.image;showMedia('mediaGrid',true);$('media').showModal();return;}
  if(action==='edit'){edit(id);return;}
  const list=data[active],index=list.findIndex(i=>i.id===id);if(index<0)return;
  if(action==='delete'){
    if(active==='collections'&&data.products.some(p=>p.collection===id)){toast('Mova ou exclua os produtos desta coleção antes de excluí-la.');return;}
    if(!confirm('Excluir este item do rascunho?'))return;list.splice(index,1);
  }else if(action==='toggle')list[index].published=!list[index].published;
  else {const next=index+(action==='up'?-1:1);if(next<0||next>=list.length)return;[list[index],list[next]]=[list[next],list[index]];}
  changed();renderList();
});
document.addEventListener('submit',event=>{
  event.preventDefault();
  if(event.target.id==='settingsForm'){data.settings=parseForm(event.target,'settings',data.settings);changed();toast('Ajustes concluídos. Salve o rascunho.');return;}
  if(event.target.id==='editForm'){
    const result=parseForm(event.target,editing.group,editing.item);if(!result.image&&['products','collections','articles'].includes(editing.group)){toast('Escolha uma foto.');return;}
    if(editing.isNew)data[editing.group].push(result);else data[editing.group][data[editing.group].findIndex(i=>i.id===editing.id)]=result;
    changed();$('editor').close();renderList();
  }
});
$('create').addEventListener('click',()=>{if(active==='media'){imageField=null;$('upload').click();}else edit();});$('search').addEventListener('input',renderList);$('save').addEventListener('click',save);
document.addEventListener('input',event=>{if(event.target.closest('#settingsForm'))changed();});
document.querySelector('a[href="/preview/"]').addEventListener('click',async event=>{event.preventDefault();const tab=window.open('about:blank','_blank');if(await save()){if(tab){tab.opener=null;tab.location='/preview/';}else window.location='/preview/';}else tab?.close();});
document.querySelector('.export').addEventListener('click',async event=>{event.preventDefault();if(await save())window.location='/api/export';});
$('upload').addEventListener('change',async event=>{
  const file=event.target.files[0];if(!file)return;
  if(file.size>10*1024*1024){toast('Escolha uma foto de até 10 MB.');return;}
  try{const response=await fetch('/api/upload',{method:'POST',headers:{'Content-Type':file.type,'X-CSRF-Token':csrf},body:file});const result=await response.json();if(!response.ok)throw Error(result.error);if(imageField){imageField.value=result.path;$('selectedPhoto').src='/'+result.path;$('media').close();}else{showMedia('content',false);toast('Foto disponível na biblioteca.');}}catch(error){toast(error.message);}finally{event.target.value='';}
});
$('publish').addEventListener('click',async()=>{if(await save())$('confirmPublish').showModal();});
$('confirmPublishButton').addEventListener('click',async()=>{
  if(busy)return;busy=true;$('confirmPublishButton').disabled=true;
  try{await request('/api/publish',{content:data,revision});$('confirmPublish').close();toast('Conteúdo enviado ao GitHub. A atualização pública depende do GitHub Pages.');}catch(error){toast(error.message);}finally{busy=false;$('confirmPublishButton').disabled=false;}
});
window.addEventListener('beforeunload',event=>{if(dirty){event.preventDefault();event.returnValue='';}});
request('/api/content').then(result=>{data=result.content;revision=result.revision;csrf=result.csrf;$('saveState').textContent='Rascunho carregado';$('publish').disabled=!result.canPublish;$('publishStatus').textContent=result.canPublish?'Publicação disponível para o site da Bordô.':'Publicação disponível após integrar a versão inicial ao main. Rascunhos, prévia e exportação já estão disponíveis.';render();}).catch(error=>{toast(error.message);$('saveState').textContent='Não foi possível carregar o painel';$('save').disabled=true;$('publish').disabled=true;});
