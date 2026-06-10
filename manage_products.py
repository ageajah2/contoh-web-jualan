import os
import json
import shutil
import time
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

# Konfigurasi Path File
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_JS_PATH = os.path.join(BASE_DIR, "products.js")
INDEX_HTML_PATH = os.path.join(BASE_DIR, "index.html")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Load products from products.js
def load_products():
    if not os.path.exists(PRODUCTS_JS_PATH):
        return []
    try:
        with open(PRODUCTS_JS_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract the JSON array
        # Format is: const products = [ ... ];
        start_idx = content.find("[")
        end_idx = content.rfind("]")
        if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
            raise ValueError("Format array products di products.js tidak valid.")
        
        json_str = content[start_idx:end_idx+1]
        return json.loads(json_str)
    except Exception as e:
        print(f"Gagal membaca products.js: {str(e)}")
        return []

# Save products to products.js
def save_products(products_list):
    try:
        json_str = json.dumps(products_list, indent=4, ensure_ascii=False)
        content = f"const products = {json_str};\n"
        with open(PRODUCTS_JS_PATH, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Gagal menyimpan ke products.js: {str(e)}")
        return False

# Setup warna estetika Boba Barokah (Warm / Chocolate Theme)
BG_PRIMARY = "#FAF6F0"       # Krem sangat muda
BG_CONTAINER = "#FFFFFF"     # Putih bersih untuk card/container
COLOR_TEXT = "#3E2723"       # Cokelat gelap untuk teks utama
COLOR_ACCENT = "#8D6E63"     # Cokelat boba untuk aksen
COLOR_SECONDARY = "#D7CCC8"  # Aksen terang
COLOR_SUCCESS = "#6E8B3D"    # Hijau matcha untuk tombol tambah
COLOR_DANGER = "#CD5C5C"     # Merah soft untuk tombol hapus
COLOR_BLUE = "#5F9EA0"       # Biru laut soft untuk tombol buka web

class BobaProductManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Boba Barokah - Pengelola Menu Produk 🧋")
        self.root.geometry("950x650")
        self.root.configure(bg=BG_PRIMARY)
        self.root.resizable(True, True)

        # Mengatur icon jika ada (opsional, fallback aman)
        try:
            self.root.iconbitmap("")
        except:
            pass

        self.products = []
        self.selected_product_id = None
        self.selected_local_image_path = None

        self.setup_styles()
        self.create_widgets()
        self.refresh_product_list()

    def setup_styles(self):
        # Configure fonts and styles
        self.title_font = ("Segoe UI", 16, "bold")
        self.subtitle_font = ("Segoe UI", 10, "italic")
        self.header_font = ("Segoe UI", 11, "bold")
        self.label_font = ("Segoe UI", 10, "bold")
        self.button_font = ("Segoe UI", 10, "bold")
        
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Treeview styling
        self.style.configure("Treeview", 
                             background=BG_CONTAINER, 
                             foreground=COLOR_TEXT, 
                             fieldbackground=BG_CONTAINER, 
                             rowheight=28,
                             font=("Segoe UI", 10))
        self.style.map("Treeview", background=[("selected", COLOR_ACCENT)], foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", 
                             background=COLOR_SECONDARY, 
                             foreground=COLOR_TEXT, 
                             font=self.header_font,
                             borderwidth=1)

    def create_widgets(self):
        # --- HEADER BANNER ---
        header_frame = tk.Frame(self.root, bg=COLOR_TEXT, height=70)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(header_frame, text="🧋 BOBA BAROKAH - PENGELOLA MENU", 
                             font=self.title_font, fg=BG_PRIMARY, bg=COLOR_TEXT)
        title_lbl.pack(pady=10, side=tk.LEFT, padx=20)

        web_btn = tk.Button(header_frame, text="🌐 Buka Website", font=self.button_font,
                            bg=COLOR_BLUE, fg="#FFFFFF", activebackground="#4682B4", activeforeground="#FFFFFF",
                            padx=15, borderwidth=0, cursor="hand2", command=self.open_website)
        web_btn.pack(pady=15, side=tk.RIGHT, padx=20)

        # --- MAIN BODY SPLIT PANELS ---
        main_frame = tk.Frame(self.root, bg=BG_PRIMARY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 1. LEFT PANEL - TABLE/LIST
        left_panel = tk.Frame(main_frame, bg=BG_PRIMARY)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        list_title = tk.Label(left_panel, text="Daftar Menu Boba Saat Ini:", font=self.header_font, 
                              fg=COLOR_TEXT, bg=BG_PRIMARY)
        list_title.pack(anchor=tk.W, pady=(0, 5))

        # Treeview Table
        table_frame = tk.Frame(left_panel)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "price", "desc")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nama Menu")
        self.tree.heading("price", text="Harga (Rp)")
        self.tree.heading("desc", text="Deskripsi Singkat")

        self.tree.column("id", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("name", width=180, minwidth=150, anchor=tk.W)
        self.tree.column("price", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("desc", width=250, minwidth=200, anchor=tk.W)

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Action Buttons under Table
        btn_action_frame = tk.Frame(left_panel, bg=BG_PRIMARY)
        btn_action_frame.pack(fill=tk.X, pady=(10, 0))

        self.delete_btn = tk.Button(btn_action_frame, text="🗑️ Hapus Produk Terpilih", font=self.button_font,
                                    bg=COLOR_DANGER, fg="#FFFFFF", activebackground="#CD2626", activeforeground="#FFFFFF",
                                    pady=8, borderwidth=0, cursor="hand2", state=tk.DISABLED, command=self.delete_selected_product)
        self.delete_btn.pack(fill=tk.X)

        # 2. RIGHT PANEL - FORM ENTRY
        right_panel = tk.LabelFrame(main_frame, text=" Formulir Produk Baru ", font=self.header_font,
                                    fg=COLOR_TEXT, bg=BG_CONTAINER, padx=15, pady=15, borderwidth=1, relief=tk.SOLID,
                                    width=380)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Fields
        # 1. Nama
        lbl_name = tk.Label(right_panel, text="Nama Produk *", font=self.label_font, fg=COLOR_TEXT, bg=BG_CONTAINER)
        lbl_name.pack(anchor=tk.W, pady=(5, 2))
        self.ent_name = tk.Entry(right_panel, font=("Segoe UI", 10), bg=BG_PRIMARY, fg=COLOR_TEXT, borderwidth=1, relief=tk.SOLID)
        self.ent_name.pack(fill=tk.X, ipady=4, pady=(0, 10))

        # 2. Deskripsi
        lbl_desc = tk.Label(right_panel, text="Deskripsi *", font=self.label_font, fg=COLOR_TEXT, bg=BG_CONTAINER)
        lbl_desc.pack(anchor=tk.W, pady=(5, 2))
        self.txt_desc = tk.Text(right_panel, font=("Segoe UI", 10), height=3, bg=BG_PRIMARY, fg=COLOR_TEXT, borderwidth=1, relief=tk.SOLID)
        self.txt_desc.pack(fill=tk.X, pady=(0, 10))

        # 3. Harga
        lbl_price = tk.Label(right_panel, text="Harga (Rupiah) *", font=self.label_font, fg=COLOR_TEXT, bg=BG_CONTAINER)
        lbl_price.pack(anchor=tk.W, pady=(5, 2))
        self.ent_price = tk.Entry(right_panel, font=("Segoe UI", 10), bg=BG_PRIMARY, fg=COLOR_TEXT, borderwidth=1, relief=tk.SOLID)
        self.ent_price.pack(fill=tk.X, ipady=4, pady=(0, 10))

        # 4. Gambar (URL / File)
        lbl_img = tk.Label(right_panel, text="Gambar Produk *", font=self.label_font, fg=COLOR_TEXT, bg=BG_CONTAINER)
        lbl_img.pack(anchor=tk.W, pady=(5, 2))
        
        img_select_frame = tk.Frame(right_panel, bg=BG_CONTAINER)
        img_select_frame.pack(fill=tk.X, pady=(0, 10))

        self.ent_img = tk.Entry(img_select_frame, font=("Segoe UI", 10), bg=BG_PRIMARY, fg=COLOR_TEXT, borderwidth=1, relief=tk.SOLID)
        self.ent_img.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        browse_btn = tk.Button(img_select_frame, text="Cari File...", font=("Segoe UI", 9, "bold"),
                               bg=COLOR_ACCENT, fg="#FFFFFF", activebackground=COLOR_TEXT, activeforeground="#FFFFFF",
                               borderwidth=0, cursor="hand2", padx=10, command=self.browse_local_image)
        browse_btn.pack(side=tk.RIGHT, padx=(5, 0), ipady=3)

        lbl_img_hint = tk.Label(right_panel, text="Bisa paste URL gambar online atau cari file lokal komputer.", 
                                font=self.subtitle_font, fg="#888888", bg=BG_CONTAINER)
        lbl_img_hint.pack(anchor=tk.W, pady=(0, 15))

        # Submit Button
        self.add_btn = tk.Button(right_panel, text="➕ Tambahkan Produk", font=self.button_font,
                                 bg=COLOR_SUCCESS, fg="#FFFFFF", activebackground="#556B2F", activeforeground="#FFFFFF",
                                 pady=10, borderwidth=0, cursor="hand2", command=self.add_product)
        self.add_btn.pack(fill=tk.X, side=tk.BOTTOM)

    # --- ACTIONS & LOGICS ---

    def refresh_product_list(self):
        # Clear current tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.products = load_products()
        for p in self.products:
            # Format price nicely for table display
            formatted_price = f"Rp {p['price']:,}".replace(",", ".")
            self.tree.insert("", tk.END, iid=p["id"], values=(p["id"], p["name"], formatted_price, p["desc"]))
        
        # Reset selection
        self.selected_product_id = None
        self.delete_btn.configure(state=tk.DISABLED)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_product_id = int(selected[0])
            self.delete_btn.configure(state=tk.NORMAL)
        else:
            self.selected_product_id = None
            self.delete_btn.configure(state=tk.DISABLED)

    def browse_local_image(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Produk Boba",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.gif")]
        )
        if file_path:
            self.selected_local_image_path = file_path
            # Tampilkan nama file di input
            self.ent_img.delete(0, tk.END)
            self.ent_img.insert(0, file_path)

    def add_product(self):
        name = self.ent_name.get().strip()
        desc = self.txt_desc.get("1.0", tk.END).strip()
        price_str = self.ent_price.get().strip()
        img_source = self.ent_img.get().strip()

        # Validasi
        if not name or not desc or not price_str or not img_source:
            messagebox.showwarning("Formulir Kosong", "Harap isi semua kolom formulir bintang (*)!")
            return

        try:
            price = int(price_str)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Harga Tidak Valid", "Harga harus berupa angka bulat positif!")
            return

        # Handle Gambar (Lokal vs URL)
        image_path_for_json = img_source
        if self.selected_local_image_path and img_source == self.selected_local_image_path:
            # Pengguna memilih file lokal, salin ke folder images/
            try:
                if not os.path.exists(IMAGES_DIR):
                    os.makedirs(IMAGES_DIR)

                ext = os.path.splitext(self.selected_local_image_path)[1].lower()
                # Buat nama file unik dengan timestamp agar tidak bentrok
                safe_name = name.lower().replace(" ", "_")
                # Hapus karakter non-alphanumeric untuk keamanan file
                safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
                filename = f"{safe_name}_{int(time.time())}{ext}"
                
                dest_path = os.path.join(IMAGES_DIR, filename)
                shutil.copy2(self.selected_local_image_path, dest_path)
                image_path_for_json = f"images/{filename}"
            except Exception as e:
                messagebox.showerror("Gagal Menyalin Gambar", f"Gagal memproses gambar lokal:\n{str(e)}")
                return

        # Generate ID Unik (ID tertinggi + 1)
        new_id = 1
        if self.products:
            new_id = max(p["id"] for p in self.products) + 1

        # Buat objek produk baru
        new_product = {
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": price,
            "image": image_path_for_json
        }

        # Simpan ke daftar dan write ke file
        self.products.append(new_product)
        if save_products(self.products):
            messagebox.showinfo("Berhasil", f"Produk '{name}' berhasil ditambahkan! ✨")
            # Reset Form
            self.ent_name.delete(0, tk.END)
            self.txt_desc.delete("1.0", tk.END)
            self.ent_price.delete(0, tk.END)
            self.ent_img.delete(0, tk.END)
            self.selected_local_image_path = None
            # Refresh List
            self.refresh_product_list()

    def delete_selected_product(self):
        if self.selected_product_id is None:
            return

        # Cari produk untuk konfirmasi nama
        product_to_delete = next((p for p in self.products if p["id"] == self.selected_product_id), None)
        if not product_to_delete:
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Hapus", 
            f"Apakah Anda yakin ingin menghapus produk '{product_to_delete['name']}'?"
        )
        
        if confirm:
            # Jika gambar produk berada di folder images/ lokal, hapus file gambarnya (opsional tetapi bersih)
            # Catatan: Kita hanya hapus jika filenya ada di sub-folder images/ lokal proyek kita.
            img_path = product_to_delete.get("image", "")
            if img_path.startswith("images/"):
                full_img_path = os.path.join(BASE_DIR, img_path)
                try:
                    if os.path.exists(full_img_path):
                        os.remove(full_img_path)
                except Exception as e:
                    print(f"Gagal menghapus file gambar: {str(e)}")

            # Filter produk yang tersisa
            self.products = [p for p in self.products if p["id"] != self.selected_product_id]
            if save_products(self.products):
                messagebox.showinfo("Berhasil", "Produk berhasil dihapus! 🗑️")
                self.refresh_product_list()

    def open_website(self):
        if os.path.exists(INDEX_HTML_PATH):
            webbrowser.open(f"file:///{INDEX_HTML_PATH.replace(os.sep, '/')}")
        else:
            messagebox.showerror("Error", "File index.html tidak ditemukan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BobaProductManagerApp(root)
    root.mainloop()
