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

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

THEMES = {
    "Warm Chocolate": {
        "BG_PRIMARY": "#FAF6F0",
        "BG_CONTAINER": "#FFFFFF",
        "COLOR_TEXT": "#3E2723",
        "COLOR_ACCENT": "#8D6E63",
        "COLOR_SECONDARY": "#D7CCC8",
        "COLOR_SUCCESS": "#6E8B3D",
        "COLOR_DANGER": "#CD5C5C",
        "COLOR_BLUE": "#5F9EA0",
        "ACTIVE_BLUE": "#4682B4",
        "ACTIVE_DANGER": "#CD2626",
        "ACTIVE_SUCCESS": "#556B2F"
    },
    "Ocean Blue": {
        "BG_PRIMARY": "#EEF6FB",
        "BG_CONTAINER": "#FFFFFF",
        "COLOR_TEXT": "#1E3A5F",
        "COLOR_ACCENT": "#3B82F6",
        "COLOR_SECONDARY": "#BFDBFE",
        "COLOR_SUCCESS": "#10B981",
        "COLOR_DANGER": "#EF4444",
        "COLOR_BLUE": "#2563EB",
        "ACTIVE_BLUE": "#1D4ED8",
        "ACTIVE_DANGER": "#DC2626",
        "ACTIVE_SUCCESS": "#059669"
    },
    "Emerald Green": {
        "BG_PRIMARY": "#F0FDF4",
        "BG_CONTAINER": "#FFFFFF",
        "COLOR_TEXT": "#14532D",
        "COLOR_ACCENT": "#10B981",
        "COLOR_SECONDARY": "#BBF7D0",
        "COLOR_SUCCESS": "#16A34A",
        "COLOR_DANGER": "#DC2626",
        "COLOR_BLUE": "#0EA5E9",
        "ACTIVE_BLUE": "#0284C7",
        "ACTIVE_DANGER": "#B91C1C",
        "ACTIVE_SUCCESS": "#15803D"
    }
}


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

# Tema 1: Warm / Chocolate
BG_PRIMARY = "#FAF6F0"
BG_CONTAINER = "#FFFFFF"
COLOR_TEXT = "#3E2723"
COLOR_ACCENT = "#8D6E63"
COLOR_SECONDARY = "#D7CCC8"
COLOR_SUCCESS = "#6E8B3D"
COLOR_DANGER = "#CD5C5C"
COLOR_BLUE = "#5F9EA0"

# Tema 2: Ocean Blue
# BG_PRIMARY="#EEF6FB" COLOR_ACCENT="#3B82F6"

# Tema 3: Emerald Green
# BG_PRIMARY="#F0FDF4" COLOR_ACCENT="#10B981"

class ProductManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Manager - Pengelola Produk")
        
        # Load window geometry
        self.load_window_geometry()
        
        # Load theme from config or default
        self.current_theme = self.load_theme_config()
        self.apply_theme_colors(self.current_theme)
        
        self.root.configure(bg=self.bg_primary)
        self.root.resizable(True, True)

        # Bind close event to save window position and resolution
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Mengatur icon jika ada (opsional, fallback aman)
        try:
            self.root.iconbitmap("")
        except:
            pass

        self.products = []
        self.selected_product_id = None
        self.selected_local_image_path = None
        self.is_edit_mode = False
        self.editing_product_id = None

        self.setup_styles()
        self.create_widgets()
        self.refresh_product_list()

    def load_window_geometry(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    geometry = config.get("geometry", "950x650")
                    self.root.geometry(geometry)
                    if config.get("zoomed", False):
                        self.root.state("zoomed")
                    return
            except Exception as e:
                print(f"Gagal membaca geometry dari config.json: {str(e)}")
        self.root.geometry("950x650")

    def save_window_geometry(self):
        try:
            state = self.root.state()
            # If minimized/iconified, don't save
            if state == "iconic":
                return
                
            config = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
            
            if state == "zoomed":
                config["zoomed"] = True
                # Keep the previous non-maximized geometry if it exists, so we don't overwrite it with screen resolution
                if "geometry" not in config:
                    config["geometry"] = self.root.geometry()
            else:
                config["geometry"] = self.root.geometry()
                config["zoomed"] = False

            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan geometry ke config.json: {str(e)}")

    def on_close(self):
        self.save_window_geometry()
        self.root.destroy()

    def load_theme_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    theme = config.get("theme", "Warm Chocolate")
                    if theme in THEMES:
                        return theme
            except Exception as e:
                print(f"Gagal membaca config.json: {str(e)}")
        return "Warm Chocolate"

    def save_theme_config(self, theme_name):
        try:
            config = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
            config["theme"] = theme_name
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan config.json: {str(e)}")

    def apply_theme_colors(self, theme_name):
        theme_colors = THEMES.get(theme_name, THEMES["Warm Chocolate"])
        self.bg_primary = theme_colors["BG_PRIMARY"]
        self.bg_container = theme_colors["BG_CONTAINER"]
        self.color_text = theme_colors["COLOR_TEXT"]
        self.color_accent = theme_colors["COLOR_ACCENT"]
        self.color_secondary = theme_colors["COLOR_SECONDARY"]
        self.color_success = theme_colors["COLOR_SUCCESS"]
        self.color_danger = theme_colors["COLOR_DANGER"]
        self.color_blue = theme_colors["COLOR_BLUE"]
        self.active_blue = theme_colors["ACTIVE_BLUE"]
        self.active_danger = theme_colors["ACTIVE_DANGER"]
        self.active_success = theme_colors["ACTIVE_SUCCESS"]

    def on_theme_change(self, event=None):
        selected_theme = self.theme_var.get()
        self.apply_theme_colors(selected_theme)
        self.save_theme_config(selected_theme)
        self.update_widget_colors()

    def update_widget_colors(self):
        # Update styles
        self.setup_styles()
        
        # Root
        self.root.configure(bg=self.bg_primary)
        
        # Header widgets
        if hasattr(self, 'header_frame'):
            self.header_frame.configure(bg=self.color_text)
        if hasattr(self, 'title_lbl'):
            self.title_lbl.configure(fg=self.bg_primary, bg=self.color_text)
        if hasattr(self, 'theme_lbl'):
            self.theme_lbl.configure(fg=self.bg_primary, bg=self.color_text)
        if hasattr(self, 'web_btn'):
            self.web_btn.configure(bg=self.color_blue, activebackground=self.active_blue)
            
        # Main layout
        if hasattr(self, 'main_frame'):
            self.main_frame.configure(bg=self.bg_primary)
        if hasattr(self, 'left_panel'):
            self.left_panel.configure(bg=self.bg_primary)
        if hasattr(self, 'list_title'):
            self.list_title.configure(fg=self.color_text, bg=self.bg_primary)
        if hasattr(self, 'btn_action_frame'):
            self.btn_action_frame.configure(bg=self.bg_primary)
            
        # Action Buttons
        if hasattr(self, 'delete_btn'):
            self.delete_btn.configure(bg=self.color_danger, activebackground=self.active_danger)
        if hasattr(self, 'edit_btn'):
            self.edit_btn.configure(bg=self.color_blue, activebackground=self.active_blue)
            
        # Right form
        if hasattr(self, 'right_panel'):
            self.right_panel.configure(fg=self.color_text, bg=self.bg_container)
            
        # Form Labels
        for lbl_attr in ['lbl_name', 'lbl_desc', 'lbl_price', 'lbl_img', 'lbl_img_hint']:
            if hasattr(self, lbl_attr):
                lbl = getattr(self, lbl_attr)
                if lbl_attr == 'lbl_img_hint':
                    lbl.configure(bg=self.bg_container)
                else:
                    lbl.configure(fg=self.color_text, bg=self.bg_container)
                    
        # Form Fields
        for entry_attr in ['ent_name', 'ent_price', 'ent_img']:
            if hasattr(self, entry_attr):
                getattr(self, entry_attr).configure(bg=self.bg_primary, fg=self.color_text)
        if hasattr(self, 'txt_desc'):
            self.txt_desc.configure(bg=self.bg_primary, fg=self.color_text)
            
        if hasattr(self, 'img_select_frame'):
            self.img_select_frame.configure(bg=self.bg_container)
            
        # Buttons
        if hasattr(self, 'browse_btn'):
            self.browse_btn.configure(bg=self.color_accent, activebackground=self.color_text)
        if hasattr(self, 'add_btn'):
            if self.is_edit_mode:
                self.add_btn.configure(bg=self.color_blue, activebackground=self.active_blue)
            else:
                self.add_btn.configure(bg=self.color_success, activebackground=self.active_success)
        if hasattr(self, 'cancel_edit_btn'):
            self.cancel_edit_btn.configure(bg=self.color_danger, activebackground=self.active_danger)

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
                             background=self.bg_container, 
                             foreground=self.color_text, 
                             fieldbackground=self.bg_container, 
                             rowheight=28,
                             font=("Segoe UI", 10))
        self.style.map("Treeview", background=[("selected", self.color_accent)], foreground=[("selected", "#FFFFFF")])
        self.style.configure("Treeview.Heading", 
                             background=self.color_secondary, 
                             foreground=self.color_text, 
                             font=self.header_font,
                             borderwidth=1)

    def create_widgets(self):
        # --- HEADER BANNER ---
        self.header_frame = tk.Frame(self.root, bg=self.color_text, height=70)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)

        self.title_lbl = tk.Label(self.header_frame, text="📦 PRODUCT MANAGER - PENGELOLA PRODUK", 
                             font=self.title_font, fg=self.bg_primary, bg=self.color_text)
        self.title_lbl.pack(pady=10, side=tk.LEFT, padx=20)

        self.web_btn = tk.Button(self.header_frame, text="🌐 Buka Website", font=self.button_font,
                            bg=self.color_blue, fg="#FFFFFF", activebackground=self.active_blue, activeforeground="#FFFFFF",
                            padx=15, borderwidth=0, cursor="hand2", command=self.open_website)
        self.web_btn.pack(pady=15, side=tk.RIGHT, padx=20)

        # Combo Box for Theme Selection
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_combo = ttk.Combobox(self.header_frame, textvariable=self.theme_var, values=list(THEMES.keys()), state="readonly", width=15, font=("Segoe UI", 9, "bold"))
        self.theme_combo.pack(pady=18, side=tk.RIGHT, padx=(0, 10))
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        self.theme_lbl = tk.Label(self.header_frame, text="🎨 Tema:", font=self.button_font, fg=self.bg_primary, bg=self.color_text)
        self.theme_lbl.pack(pady=15, side=tk.RIGHT, padx=(10, 5))

        # --- MAIN BODY SPLIT PANELS ---
        self.main_frame = tk.Frame(self.root, bg=self.bg_primary)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 1. LEFT PANEL - TABLE/LIST
        self.left_panel = tk.Frame(self.main_frame, bg=self.bg_primary)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.list_title = tk.Label(self.left_panel, text="Daftar Produk Saat Ini:", font=self.header_font, 
                              fg=self.color_text, bg=self.bg_primary)
        self.list_title.pack(anchor=tk.W, pady=(0, 5))

        # Treeview Table
        self.table_frame = tk.Frame(self.left_panel)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "name", "price", "desc")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Nama Produk")
        self.tree.heading("price", text="Harga (Rp)")
        self.tree.heading("desc", text="Deskripsi Singkat")

        self.tree.column("id", width=50, minwidth=40, anchor=tk.CENTER)
        self.tree.column("name", width=180, minwidth=150, anchor=tk.W)
        self.tree.column("price", width=100, minwidth=80, anchor=tk.E)
        self.tree.column("desc", width=250, minwidth=200, anchor=tk.W)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<ButtonPress-1>", self.on_drag_start)
        self.tree.bind("<B1-Motion>", self.on_drag_motion)
        self.tree.bind("<ButtonRelease-1>", self.on_drag_end)

        # Action Buttons under Table
        self.btn_action_frame = tk.Frame(self.left_panel, bg=self.bg_primary)
        self.btn_action_frame.pack(fill=tk.X, pady=(10, 0))

        self.edit_btn = tk.Button(self.btn_action_frame, text="✏️ Edit Produk", font=self.button_font,
                                  bg=self.color_blue, fg="#FFFFFF", activebackground=self.active_blue, activeforeground="#FFFFFF",
                                  pady=8, borderwidth=0, cursor="hand2", state=tk.DISABLED, command=self.enter_edit_mode)
        self.edit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.delete_btn = tk.Button(self.btn_action_frame, text="🗑️ Hapus Produk", font=self.button_font,
                                    bg=self.color_danger, fg="#FFFFFF", activebackground=self.active_danger, activeforeground="#FFFFFF",
                                    pady=8, borderwidth=0, cursor="hand2", state=tk.DISABLED, command=self.delete_selected_product)
        self.delete_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # 2. RIGHT PANEL - FORM ENTRY
        self.right_panel = tk.LabelFrame(self.main_frame, text=" Formulir Produk Baru ", font=self.header_font,
                                    fg=self.color_text, bg=self.bg_container, padx=15, pady=15, borderwidth=1, relief=tk.SOLID,
                                    width=380)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))

        # Fields
        # 1. Nama
        self.lbl_name = tk.Label(self.right_panel, text="Nama Produk *", font=self.label_font, fg=self.color_text, bg=self.bg_container)
        self.lbl_name.pack(anchor=tk.W, pady=(5, 2))
        self.ent_name = tk.Entry(self.right_panel, font=("Segoe UI", 10), bg=self.bg_primary, fg=self.color_text, borderwidth=1, relief=tk.SOLID)
        self.ent_name.pack(fill=tk.X, ipady=4, pady=(0, 10))

        # 2. Deskripsi
        self.lbl_desc = tk.Label(self.right_panel, text="Deskripsi *", font=self.label_font, fg=self.color_text, bg=self.bg_container)
        self.lbl_desc.pack(anchor=tk.W, pady=(5, 2))
        self.txt_desc = tk.Text(self.right_panel, font=("Segoe UI", 10), height=3, bg=self.bg_primary, fg=self.color_text, borderwidth=1, relief=tk.SOLID)
        self.txt_desc.pack(fill=tk.X, pady=(0, 10))

        # 3. Harga
        self.lbl_price = tk.Label(self.right_panel, text="Harga (Rupiah) *", font=self.label_font, fg=self.color_text, bg=self.bg_container)
        self.lbl_price.pack(anchor=tk.W, pady=(5, 2))
        self.ent_price = tk.Entry(self.right_panel, font=("Segoe UI", 10), bg=self.bg_primary, fg=self.color_text, borderwidth=1, relief=tk.SOLID)
        self.ent_price.pack(fill=tk.X, ipady=4, pady=(0, 10))

        # 4. Gambar (URL / File)
        self.lbl_img = tk.Label(self.right_panel, text="Gambar Produk *", font=self.label_font, fg=self.color_text, bg=self.bg_container)
        self.lbl_img.pack(anchor=tk.W, pady=(5, 2))
        
        self.img_select_frame = tk.Frame(self.right_panel, bg=self.bg_container)
        self.img_select_frame.pack(fill=tk.X, pady=(0, 10))

        self.ent_img = tk.Entry(self.img_select_frame, font=("Segoe UI", 10), bg=self.bg_primary, fg=self.color_text, borderwidth=1, relief=tk.SOLID)
        self.ent_img.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        self.browse_btn = tk.Button(self.img_select_frame, text="Cari File...", font=("Segoe UI", 9, "bold"),
                               bg=self.color_accent, fg="#FFFFFF", activebackground=self.color_text, activeforeground="#FFFFFF",
                               borderwidth=0, cursor="hand2", padx=10, command=self.browse_local_image)
        self.browse_btn.pack(side=tk.RIGHT, padx=(5, 0), ipady=3)

        self.lbl_img_hint = tk.Label(self.right_panel, text="Bisa paste URL gambar online atau cari file lokal komputer.", 
                                font=self.subtitle_font, fg="#888888", bg=self.bg_container)
        self.lbl_img_hint.pack(anchor=tk.W, pady=(0, 15))

        # Submit & Cancel Buttons
        self.submit_frame = tk.Frame(self.right_panel, bg=self.bg_container)
        self.submit_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.add_btn = tk.Button(self.submit_frame, text="➕ Tambahkan Produk", font=self.button_font,
                                 bg=self.color_success, fg="#FFFFFF", activebackground=self.active_success, activeforeground="#FFFFFF",
                                 pady=10, borderwidth=0, cursor="hand2", command=self.add_product)
        self.add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.cancel_edit_btn = tk.Button(self.submit_frame, text="❌ Batal", font=self.button_font,
                                         bg=self.color_danger, fg="#FFFFFF", activebackground=self.active_danger, activeforeground="#FFFFFF",
                                         pady=10, borderwidth=0, cursor="hand2", command=self.exit_edit_mode)

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
        self.edit_btn.configure(state=tk.DISABLED)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_product_id = int(selected[0])
            self.delete_btn.configure(state=tk.NORMAL)
            self.edit_btn.configure(state=tk.NORMAL)
            if self.is_edit_mode:
                self.load_product_to_form(self.selected_product_id)
        else:
            self.selected_product_id = None
            self.delete_btn.configure(state=tk.DISABLED)
            self.edit_btn.configure(state=tk.DISABLED)

    def load_product_to_form(self, product_id):
        product = next((p for p in self.products if p["id"] == product_id), None)
        if not product:
            return
        
        self.editing_product_id = product["id"]
        
        self.ent_name.delete(0, tk.END)
        self.ent_name.insert(0, product["name"])
        
        self.txt_desc.delete("1.0", tk.END)
        self.txt_desc.insert("1.0", product["desc"])
        
        self.ent_price.delete(0, tk.END)
        self.ent_price.insert(0, str(product["price"]))
        
        self.ent_img.delete(0, tk.END)
        self.ent_img.insert(0, product["image"])
        self.selected_local_image_path = None
        
        self.right_panel.configure(text=f" Edit Produk (ID: {product['id']}) ")

    def enter_edit_mode(self):
        if self.selected_product_id is None:
            return
        self.is_edit_mode = True
        self.load_product_to_form(self.selected_product_id)
        self.add_btn.configure(text="💾 Simpan Perubahan", bg=self.color_blue, activebackground=self.active_blue)
        self.cancel_edit_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

    def exit_edit_mode(self):
        self.is_edit_mode = False
        self.editing_product_id = None
        
        self.right_panel.configure(text=" Formulir Produk Baru ")
        self.add_btn.configure(text="➕ Tambahkan Produk", bg=self.color_success, activebackground=self.active_success)
        self.cancel_edit_btn.pack_forget()
        
        self.ent_name.delete(0, tk.END)
        self.txt_desc.delete("1.0", tk.END)
        self.ent_price.delete(0, tk.END)
        self.ent_img.delete(0, tk.END)
        self.selected_local_image_path = None

    def on_drag_start(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region not in ("tree", "cell"):
            self.drag_item = None
            return
        self.drag_item = self.tree.identify_row(event.y)
        if self.drag_item:
            self.tree.configure(cursor="size_ns")

    def on_drag_motion(self, event):
        if not hasattr(self, 'drag_item') or not self.drag_item:
            return
        target_item = self.tree.identify_row(event.y)
        if target_item and target_item != self.drag_item:
            parent = ""
            target_idx = self.tree.index(target_item)
            self.tree.move(self.drag_item, parent, target_idx)
        return "break"

    def on_drag_end(self, event):
        if hasattr(self, 'drag_item') and self.drag_item:
            # Reconstruct the order based on visual positions in Treeview
            ordered_ids = []
            for item in self.tree.get_children():
                try:
                    ordered_ids.append(int(item))
                except ValueError:
                    pass
            
            # Reorder the products array
            products_dict = {p["id"]: p for p in self.products}
            new_ordered_products = []
            for pid in ordered_ids:
                if pid in products_dict:
                    new_ordered_products.append(products_dict[pid])
            
            # Add any missing products
            seen = set(ordered_ids)
            for p in self.products:
                if p["id"] not in seen:
                    new_ordered_products.append(p)
            
            # Reassign sequential IDs (1 to N) and track the dragged item's new ID
            old_drag_id = int(self.drag_item)
            new_drag_id = None
            for idx, p in enumerate(new_ordered_products):
                if p["id"] == old_drag_id:
                    new_drag_id = idx + 1
                p["id"] = idx + 1
            
            self.products = new_ordered_products
            save_products(self.products)
            
            # Reset cursor
            self.tree.configure(cursor="")
            
            # Refresh products list in Treeview with the new sequential IDs
            self.refresh_product_list()
            
            # Re-select the dragged item with its new ID to preserve focus
            if new_drag_id is not None:
                self.tree.selection_set(str(new_drag_id))
                
            self.drag_item = None

    def browse_local_image(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar Produk",
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

        if self.is_edit_mode:
            # Edit existing product
            product_to_edit = next((p for p in self.products if p["id"] == self.editing_product_id), None)
            if product_to_edit:
                # If image changed and previous image was local, we can delete the old local image file
                old_image = product_to_edit.get("image", "")
                if old_image != image_path_for_json and old_image.startswith("images/"):
                    full_old_img_path = os.path.join(BASE_DIR, old_image)
                    try:
                        if os.path.exists(full_old_img_path):
                            os.remove(full_old_img_path)
                    except Exception as e:
                        print(f"Gagal menghapus file gambar lama: {str(e)}")

                product_to_edit["name"] = name
                product_to_edit["desc"] = desc
                product_to_edit["price"] = price
                product_to_edit["image"] = image_path_for_json
                
                if save_products(self.products):
                    messagebox.showinfo("Berhasil", f"Produk '{name}' berhasil diperbarui! 💾")
                    self.exit_edit_mode()
                    self.refresh_product_list()
        else:
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

            # Exit edit mode if the deleted product was being edited
            if self.is_edit_mode and self.selected_product_id == self.editing_product_id:
                self.exit_edit_mode()

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
    app = ProductManagerApp(root)
    root.mainloop()
