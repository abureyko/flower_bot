const API = "/api/products";
const cartBtn = document.getElementById("cart-btn");
const cartEl = document.getElementById("cart");
const closeCart = document.getElementById("close-cart");
const cartItemsEl = document.getElementById("cart-items");
const cartCount = document.getElementById("cart-count");
const cartTotal = document.getElementById("cart-total");
const toast = document.getElementById("toast");
const openTelegram = document.getElementById("open-telegram");

let products = [];
let cart = JSON.parse(localStorage.getItem("cart_v1")) || [];

function showToast(text){
  toast.textContent = text;
  toast.classList.add("show");
  setTimeout(()=> toast.classList.remove("show"), 1500);
}

function saveCart(){
  localStorage.setItem("cart_v1", JSON.stringify(cart));
  cartCount.textContent = cart.reduce((s,i)=> s + i.qty, 0);
  cartTotal.textContent = cart.reduce((s,i)=> s + i.qty * i.price, 0);
}

function renderProducts(){
  const root = document.getElementById("products");
  root.innerHTML = "";
  products.forEach(p=>{
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `
      <div class="img"><img src="${p.image || 'https://picsum.photos/seed/' + p.id + '/600/400'}" alt="${p.title}"></div>
      <div class="meta">
        <h4>${p.title}</h4>
        <div class="price">${p.price} ₽</div>
      </div>
      <div class="desc">${p.description || ''}</div>
      <div class="actions">
        <div class="left">
          <button class="add-btn" data-id="${p.id}">Добавить</button>
        </div>
        <div class="right"></div>
      </div>
    `;
    root.appendChild(card);
  });

  root.querySelectorAll(".add-btn").forEach(btn=>{
    btn.addEventListener("click", e=>{
      const id = btn.dataset.id;
      const prod = products.find(x=> String(x.id) === String(id));
      const found = cart.find(c=> String(c.id) === String(id));
      if(found) found.qty += 1;
      else cart.push({ id: prod.id, title: prod.title, price: prod.price, image: prod.image, qty: 1});
      saveCart();
      showToast("Добавлено в корзину");
      renderCart();
    });
  });
}

function renderCart(){
  cartItemsEl.innerHTML = "";
  if(cart.length === 0){
    cartItemsEl.innerHTML = `<div style="color:var(--muted);padding:12px">Корзина пуста</div>`;
    saveCart();
    return;
  }
  cart.forEach(item=>{
    const row = document.createElement("div");
    row.className = "cart-row";
    row.innerHTML = `
      <img src="${item.image || 'https://picsum.photos/seed/' + item.id + '/200/200'}" />
      <div class="info">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <strong>${item.title}</strong>
          <div>${item.price} ₽</div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px">
          <div class="qty">
            <button class="qty-dec" data-id="${item.id}">−</button>
            <div style="padding:0 8px">${item.qty}</div>
            <button class="qty-inc" data-id="${item.id}">+</button>
          </div>
          <button class="remove" data-id="${item.id}">Удалить</button>
        </div>
      </div>
    `;
    cartItemsEl.appendChild(row);
  });

  cartItemsEl.querySelectorAll(".qty-inc").forEach(b=>{
    b.addEventListener("click", ()=>{
      const id = b.dataset.id; cart.find(x=> String(x.id)===String(id)).qty += 1; saveCart(); renderCart();
    });
  });
  cartItemsEl.querySelectorAll(".qty-dec").forEach(b=>{
    b.addEventListener("click", ()=>{
      const id = b.dataset.id; const item = cart.find(x=> String(x.id)===String(id));
      item.qty = Math.max(1, item.qty - 1); saveCart(); renderCart();
    });
  });
  cartItemsEl.querySelectorAll(".remove").forEach(b=>{
    b.addEventListener("click", ()=>{
      const id = b.dataset.id; cart = cart.filter(x=> String(x.id)!==String(id)); saveCart(); renderCart();
    });
  });
  saveCart();
}

cartBtn.addEventListener("click", ()=> cartEl.classList.toggle("open"));
closeCart.addEventListener("click", ()=> cartEl.classList.remove("open"));
document.getElementById("checkout").addEventListener("click", ()=>{
  if(cart.length === 0) { showToast("Корзина пуста"); return; }
  // Простая заглушка оформления: отправляем JSON в Telegram через web app / почту или API
  showToast("Оформлено! (демо)");
  cart = []; saveCart(); renderCart(); cartEl.classList.remove("open");
});

async function fetchProducts(){
  try{
    const res = await fetch(API);
    if(!res.ok) throw new Error("no products");
    products = await res.json();
    if(!Array.isArray(products) || products.length === 0) {
      products = [{
        id:1,title:"Букет «Рассвет»",price:1299,description:"Сборный букет из пионов и роз",image:"/static/products/photo_2025-11-26 11.28.40.jpeg"
      }]
    }
  }catch(e){
    // fallback demo products
    products = [
      {id:101,title:"Букет «Рассвет»",price:1299,description:"Сборный из пионов и роз",image:"https://picsum.photos/seed/1/800/600"},
      {id:102,title:"Монстера в горшке",price:2199,description:"Зелёное крупное растение",image:"https://picsum.photos/seed/2/800/600"},
      {id:103,title:"Мини-таблица",price:599,description:"Небольшой букет в коробке",image:"https://picsum.photos/seed/3/800/600"}
    ];
  }
  renderProducts();
  renderCart();
}

function init(){
  saveCart();
  fetchProducts();
  // Подставляем ссылку для открытия webapp в Telegram
  // WEBAPP_URL берётся с env в bot — но сюда можно подставить прямую ссылку:
  const webapp = window.location.origin;
  openTelegram.href = `https://t.me/your_bot_username?startweb=${encodeURIComponent(webapp)}`;
}

init();