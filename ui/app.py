import asyncio
import tkinter as tk
from tkinter import messagebox, ttk

from core.adb_manager import ADBManager
from core.logger import Logger


class App:
    """Interface gráfica do desinstalador."""

    def __init__(self, root, loop):
        self.root = root
        self.loop = loop
        self.root.title("Desinstalador de Apps Android via ADB")
        self.root.geometry("700x600")

        self.search_var = tk.StringVar()
        self.checkbox_vars = {}

        # UI Components
        self.create_widgets()

        # ADB Manager e Logger
        self.logger = Logger(self.log_text)
        self.adb = ADBManager(self.logger)

        # Inicialização assíncrona
        self.loop.create_task(self.init_adb())

    async def init_adb(self):
        if not await self.adb.verificar_adb() or not await self.adb.conectar_dispositivo():
            self.root.destroy()

    def create_widgets(self):
        # Campo de pesquisa
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=10)
        tk.Label(frame_top, text="Pesquisar pacote:").pack(side=tk.LEFT, padx=5)
        tk.Entry(frame_top, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Listar", command=lambda: self.loop.create_task(self.update_package_list())).pack(side=tk.LEFT, padx=5)

        # Lista com rolagem
        frame_list = tk.Frame(self.root)
        frame_list.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(frame_list)
        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scroll_frame = tk.Frame(self.canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Scroll com a roda do mouse (cross-platform)
        def _on_mousewheel(event):
            if event.delta:  # Windows / Mac
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif event.num == 4:  # Linux scroll up
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:  # Linux scroll down
                self.canvas.yview_scroll(1, "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)  # Windows / Mac
        self.canvas.bind_all("<Button-4>", _on_mousewheel)    # Linux scroll up
        self.canvas.bind_all("<Button-5>", _on_mousewheel)    # Linux scroll down

        # Log de saída
        tk.Label(self.root, text="Log do ADB:").pack()
        self.log_text = tk.Text(self.root, height=10, state="disabled", bg="#f0f0f0")
        self.log_text.pack(fill="both", padx=5, pady=5, expand=True)

        # Botão de desinstalar
        tk.Button(self.root, text="Desinstalar Selecionados", command=lambda: self.loop.create_task(self.uninstall_selected()),
                  bg="red", fg="white").pack(pady=10)

    async def update_package_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()

        filtro = self.search_var.get().strip()
        self.logger.log(f"\n=== Pesquisando pacotes com: '{filtro}' ===")
        pacotes = await self.adb.listar_pacotes(filtro)

        if not pacotes:
            tk.Label(self.scroll_frame, text="Nenhum pacote encontrado.").pack()
            return

        for pkg in pacotes:
            var = tk.BooleanVar()
            self.checkbox_vars[pkg] = var
            tk.Checkbutton(self.scroll_frame, text=pkg, variable=var).pack(anchor="w")

    async def uninstall_selected(self):
        selecionados = [pkg for pkg, var in self.checkbox_vars.items() if var.get()]
        if not selecionados:
            messagebox.showwarning("Aviso", "Nenhum pacote selecionado.")
            return

        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja desinstalar {len(selecionados)} pacotes?")
        if not confirm:
            return

        await self.adb.desinstalar(selecionados)
        await self.update_package_list()
