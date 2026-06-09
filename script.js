// DAFTAR PRODUK MINUMAN BOBA
const products = [
    {
        id: 1,
        name: "Classic Milk Boba",
        desc: "Teh susu karamel dengan boba kenyal",
        price: 25000,
        image: "https://th.bing.com/th/id/OIP.4nWo-hNVNZRObHCfXEC2zwHaLH?w=203&h=304&c=7&r=0&o=7&pid=1.7&rm=3"
    },
    {
        id: 2,
        name: "Taro Boba Bliss",
        desc: "Taro creamy topping boba & grass jelly",
        price: 28000,
        image: "https://img.freepik.com/premium-photo/beverage-known-as-bubble-tea-is-prepared-by-mixing-milk-black-currant-berries-together-along_908985-69075.jpg"
    },
    {
        id: 3,
        name: "Matcha Latte Boba",
        desc: "Matcha autentik + susu + pearl hitam",
        price: 30000,
        image: "https://images.healthshots.com/healthshots/en/uploads/2024/11/14212707/Boba-tea.jpg"
    },
    {
        id: 4,
        name: "Brown Sugar Boba",
        desc: "Gula aren asli, caramel sauce, extra chewy",
        price: 27000,
        image: "https://images.unsplash.com/photo-1541658016709-82535e94bc69?w=600&auto=format&fit=crop&q=80"
    },
    {
        id: 5,
        name: "Lychee Pop Boba",
        desc: "Segar leci dengan popping boba rasa buah",
        price: 29000,
        image: "https://images.unsplash.com/photo-1595981267035-7b04ca84a82d?w=600&auto=format&fit=crop&q=80"
    },
    {
        id: 6,
        name: "Choco Banana Boba",
        desc: "Coklat pisang, whipped cream, pearl hitam",
        price: 32000,
        image: "https://thumbs.dreamstime.com/b/vibrant-yellow-banana-bubble-tea-clear-plastic-cup-refreshing-summer-beverage-perfect-culinary-photography-indulge-354870184.jpg"
    }
];

// Keranjang state: array { id, name, price, quantity }
let cart = [];

// Helper: simpan ke localStorage
function saveCart() {
    localStorage.setItem("bobaCart", JSON.stringify(cart));
    updateCartUI();
    updateCartBadge();
}

// load cart dari local storage
function loadCart() {
    const stored = localStorage.getItem("bobaCart");
    if (stored) {
        try {
            cart = JSON.parse(stored);
            if (!Array.isArray(cart)) cart = [];
        } catch (e) { cart = []; }
    } else {
        cart = [];
    }
    updateCartUI();
    updateCartBadge();
}

// update badge icon
function updateCartBadge() {
    const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.getElementById("cartCountBadge");
    if (badge) badge.innerText = totalQty;
}

// Format Rupiah
function formatRupiah(amount) {
    return "Rp " + amount.toLocaleString("id-ID");
}

// tampilkan produk di grid
function renderProducts() {
    const grid = document.getElementById("productGrid");
    if (!grid) return;
    grid.innerHTML = "";
    products.forEach(prod => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
        <div class="product-img">
            <img src="${prod.image}" alt="${prod.name}">
        </div>
        <div class="product-info">
            <div class="product-title">${prod.name}</div>
            <div class="product-desc">${prod.desc}</div>
            <div class="price-row">
                <span class="price">${formatRupiah(prod.price)}</span>
                <button class="add-to-cart" data-id="${prod.id}">
                    <i class="fas fa-plus-circle"></i> Tambah
                </button>
            </div>
        </div>
    `;
        grid.appendChild(card);
    });

    // attach event listener ke semua tombol tambah
    document.querySelectorAll(".add-to-cart").forEach(btn => {
        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const id = parseInt(btn.getAttribute("data-id"));
            addToCart(id);
        });
    });
}

// fungsi tambah ke keranjang
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (!product) return;
    const existingItem = cart.find(item => item.id === productId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1
        });
    }
    saveCart();
    showToast(`${product.name} ditambahkan ke keranjang! 🧋`);
}

// update tampilan keranjang (sidebar)
function updateCartUI() {
    const container = document.getElementById("cartItemsContainer");
    const totalSpan = document.getElementById("cartTotalPrice");
    const checkoutForm = document.getElementById("checkoutForm");
    if (!container) return;

    if (cart.length === 0) {
        container.innerHTML = `<div class="empty-cart">Keranjang masih kosong <i class="fas fa-mug-hot"></i></div>`;
        if (totalSpan) totalSpan.innerText = formatRupiah(0);
        if (checkoutForm) checkoutForm.style.display = "none";
        return;
    }

    if (checkoutForm) checkoutForm.style.display = "flex";

    let totalPrice = 0;
    let cartHtml = "";
    cart.forEach((item, idx) => {
        const itemTotal = item.price * item.quantity;
        totalPrice += itemTotal;
        cartHtml += `
        <div class="cart-item" data-id="${item.id}">
            <div class="cart-item-info">
                <h4>${item.name}</h4>
                <div class="cart-item-price">${formatRupiah(item.price)}</div>
            </div>
            <div class="cart-item-actions">
                <button class="decr-qty" data-id="${item.id}">-</button>
                <span class="item-qty">${item.quantity}</span>
                <button class="incr-qty" data-id="${item.id}">+</button>
                <button class="remove-item" data-id="${item.id}"><i class="fas fa-trash-alt"></i></button>
            </div>
        </div>
    `;
    });
    container.innerHTML = cartHtml;
    if (totalSpan) totalSpan.innerText = formatRupiah(totalPrice);

    // event tombol + - hapus di dalam cart
    document.querySelectorAll(".incr-qty").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const id = parseInt(btn.getAttribute("data-id"));
            changeQuantity(id, 1);
        });
    });
    document.querySelectorAll(".decr-qty").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const id = parseInt(btn.getAttribute("data-id"));
            changeQuantity(id, -1);
        });
    });
    document.querySelectorAll(".remove-item").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const id = parseInt(btn.getAttribute("data-id"));
            removeItemCompletely(id);
        });
    });
}

function changeQuantity(id, delta) {
    const index = cart.findIndex(i => i.id === id);
    if (index !== -1) {
        const newQty = cart[index].quantity + delta;
        if (newQty <= 0) {
            cart.splice(index, 1);
        } else {
            cart[index].quantity = newQty;
        }
        saveCart();
    }
}

function removeItemCompletely(id) {
    cart = cart.filter(item => item.id !== id);
    saveCart();
    showToast("Item dihapus dari keranjang");
}

// toast notifikasi
let toastTimeout = null;
function showToast(message) {
    const toast = document.getElementById("toastMsg");
    if (!toast) return;
    toast.innerText = message;
    toast.style.opacity = "1";
    if (toastTimeout) clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.style.opacity = "0";
    }, 2000);
}

// ----- Checkout ke WhatsApp dengan nomor 085263749805 -----
function sendWhatsAppOrder() {
    if (cart.length === 0) {
        showToast("Keranjang masih kosong, tambahkan menu dulu ya! 🧋");
        return;
    }

    // Ambil data nama & alamat
    const nameInput = document.getElementById("custName");
    const addressInput = document.getElementById("custAddress");
    const name = nameInput ? nameInput.value.trim() : "";
    const address = addressInput ? addressInput.value.trim() : "";

    if (!name || !address) {
        showToast("Harap isi nama dan alamat terlebih dahulu! 📋");
        if (!name && nameInput) nameInput.focus();
        else if (!address && addressInput) addressInput.focus();
        return;
    }

    // Simpan nama & alamat ke localStorage agar tidak perlu ngetik ulang lain kali
    localStorage.setItem("custName", name);
    localStorage.setItem("custAddress", address);

    // hitung total & buat pesan
    let itemsList = "";
    let grandTotal = 0;
    cart.forEach(item => {
        const subtotal = item.price * item.quantity;
        grandTotal += subtotal;
        itemsList += `- ${item.name} (x${item.quantity}) = ${formatRupiah(subtotal)}\n`;
    });
    const orderSummary = `Halo Boba Barokah! Saya ingin memesan:\n\n*Detail Pelanggan:*\n- Nama: ${name}\n- Alamat: ${address}\n\n*Pesanan:*\n${itemsList}\n*Total: ${formatRupiah(grandTotal)}*\n\nTerima kasih.`;
    const encodedMsg = encodeURIComponent(orderSummary);
    const phoneNumber = "6285263749805"; // 085263749805 -> 6285263749805 format internasional tanpa '+'
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMsg}`;

    // Buka WhatsApp di tab baru / redirect
    window.open(whatsappUrl, "_blank");
    // Opsional: reset keranjang jika ingin setelah checkout? biar tidak reset otomatis agar tidak mengganggu, 
    // namun kita bisa beri opsi clear? tapi sesuai preferensi. Lebih baik tidak reset otomatis, user bisa clear manual.
    // Tampilkan notifikasi.
    showToast("Mengarahkan ke WhatsApp... selesaikan pesanan Anda 😊");
    // tutup sidebar keranjang biar nyaman
    closeCartSidebar();
}

// Sidebar control
function openCartSidebar() {
    document.getElementById("cartOverlay").classList.add("open");
    document.getElementById("cartSidebar").classList.add("open");
}
function closeCartSidebar() {
    document.getElementById("cartOverlay").classList.remove("open");
    document.getElementById("cartSidebar").classList.remove("open");
}

// Event binding
document.addEventListener("DOMContentLoaded", () => {
    renderProducts();
    loadCart();

    // Load data nama & alamat yang tersimpan
    const nameInput = document.getElementById("custName");
    const addressInput = document.getElementById("custAddress");
    if (nameInput) nameInput.value = localStorage.getItem("custName") || "";
    if (addressInput) addressInput.value = localStorage.getItem("custAddress") || "";

    // Event listener untuk auto-save nama & alamat saat diketik
    if (nameInput) {
        nameInput.addEventListener("input", () => {
            localStorage.setItem("custName", nameInput.value.trim());
        });
    }
    if (addressInput) {
        addressInput.addEventListener("input", () => {
            localStorage.setItem("custAddress", addressInput.value.trim());
        });
    }

    const cartIcon = document.getElementById("cartIconBtn");
    const closeBtn = document.getElementById("closeCartBtn");
    const overlay = document.getElementById("cartOverlay");
    const checkoutBtn = document.getElementById("checkoutBtn");

    if (cartIcon) cartIcon.addEventListener("click", openCartSidebar);
    if (closeBtn) closeBtn.addEventListener("click", closeCartSidebar);
    if (overlay) overlay.addEventListener("click", closeCartSidebar);
    if (checkoutBtn) checkoutBtn.addEventListener("click", sendWhatsAppOrder);
});

// update cart badge juga saat load & perubahan
window.updateCartBadge = updateCartBadge;
// jika ada perubahan dari loadCart sudah panggil update
// untuk sinkronisasi fungsi manual saveCart panggil update
// override saveCart agar selalu merender ulang cart UI dan badge
// simpan function asli jika perlu, tapi sudah ditimpa
const originalSaveCart = saveCart;
window.saveCart = saveCart;

// panggil render ulang cart setiap ada perubahan
// sudah fine.
