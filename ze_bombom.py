import tkinter as tk
from tkinter import font as tkfont
import math

# ── Paleta de cores ──────────────────────────────────────────
CREAM   = "#F5EFE0"
CHOC    = "#2C1A0E"
CARA    = "#C47A2B"
GOLD    = "#E8A830"
BLUSH   = "#E8C49A"
DARK    = "#1A0F06"
CARDBG  = "#FDF7EE"
LIGHTBG = "#FBF0DC"
RED_ERR = "#C0392B"

# ── Frases aleatórias do Zé ──────────────────────────────────
import random
FRASES = [
    lambda v: f"{v} bombons na mochila, bora distribuir!",
    lambda v: f"Carregando {v} bombons. Costas tão boas!",
    lambda v: f"{v} bombons? Deixa com o Zé! 🚀",
    lambda v: f"Recebido! {v} bombons prontos pra marcha.",
    lambda v: f"Missão aceita: {v} bombons pra entregar!",
]

class ZeBombomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zé Bombom · Marcha & Bombons")
        self.root.configure(bg=CREAM)
        self.root.resizable(False, False)

        # Centralizar na tela
        w, h = 520, 720
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._anim_phase = 0
        self._build_fonts()
        self._build_ui()
        self._animate_mascot(0)

    # ── Fontes ──────────────────────────────────────────────
    def _build_fonts(self):
        self.f_title  = tkfont.Font(family="Georgia", size=22, weight="bold")
        self.f_sub    = tkfont.Font(family="Courier", size=8)
        self.f_badge  = tkfont.Font(family="Courier", size=7, weight="bold")
        self.f_label  = tkfont.Font(family="Courier", size=8)
        self.f_input  = tkfont.Font(family="Courier", size=18, weight="bold")
        self.f_btn    = tkfont.Font(family="Helvetica", size=11, weight="bold")
        self.f_card_t = tkfont.Font(family="Georgia", size=11, weight="bold")
        self.f_card_s = tkfont.Font(family="Courier", size=8)
        self.f_count  = tkfont.Font(family="Courier", size=24, weight="bold")
        self.f_sum_v  = tkfont.Font(family="Courier", size=16, weight="bold")
        self.f_sum_k  = tkfont.Font(family="Courier", size=7)
        self.f_bubble = tkfont.Font(family="Helvetica", size=9)
        self.f_reset  = tkfont.Font(family="Helvetica", size=9)

    # ── UI principal ─────────────────────────────────────────
    def _build_ui(self):
        pad = dict(padx=20)

        # ── Header: mascote + nome ──
        header = tk.Frame(self.root, bg=CREAM)
        header.pack(fill="x", padx=20, pady=(18, 0))

        # Canvas mascote
        self.canvas = tk.Canvas(header, width=90, height=110,
                                bg=CREAM, highlightthickness=0)
        self.canvas.pack(side="left")
        self._draw_mascot(0)

        # Texto marca
        brand = tk.Frame(header, bg=CREAM)
        brand.pack(side="left", padx=(12, 0), anchor="w")

        tk.Label(brand, text="Zé Bombom", font=self.f_title,
                 bg=CREAM, fg=CHOC).pack(anchor="w")
        tk.Label(brand, text="MARCHA & BOMBONS · EST. 2025",
                 font=self.f_sub, bg=CREAM, fg=CARA).pack(anchor="w")

        badge_frame = tk.Frame(brand, bg=CHOC, padx=8, pady=3)
        badge_frame.pack(anchor="w", pady=(4, 0))
        tk.Label(badge_frame, text="SISTEMA DE ESTOQUE OFICIAL",
                 font=self.f_badge, bg=CHOC, fg=GOLD).pack()

        # Balão de fala do Zé
        self.bubble_var = tk.StringVar(value="")
        self.bubble_lbl = tk.Label(
            self.root, textvariable=self.bubble_var,
            font=self.f_bubble, bg=CHOC, fg=CREAM,
            wraplength=460, justify="left",
            padx=14, pady=8
        )
        self.bubble_lbl.pack(fill="x", padx=20, pady=(10, 0))
        self.bubble_lbl.pack_forget()   # escondido até calcular

        # ── Input card ──
        ic = tk.Frame(self.root, bg=CHOC, padx=20, pady=14)
        ic.pack(fill="x", padx=20, pady=(12, 0))

        tk.Label(ic, text="QUANTIDADE TOTAL DE BOMBONS",
                 font=self.f_label, bg=CHOC, fg=BLUSH).pack(anchor="w")

        row = tk.Frame(ic, bg=CHOC)
        row.pack(fill="x", pady=(6, 0))

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            row, textvariable=self.entry_var,
            font=self.f_input, bg="#3D2010", fg=GOLD,
            insertbackground=GOLD, bd=0, highlightthickness=1,
            highlightcolor=GOLD, highlightbackground="#6B3A18",
            width=12
        )
        self.entry.pack(side="left", ipady=6, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._calcular())

        btn = tk.Button(
            row, text="Calcular", font=self.f_btn,
            bg=GOLD, fg=DARK, activebackground="#F0B534",
            activeforeground=DARK, relief="flat", bd=0,
            cursor="hand2", command=self._calcular,
            padx=16, pady=6
        )
        btn.pack(side="left")

        self.err_lbl = tk.Label(ic, text="", font=self.f_label,
                                bg=CHOC, fg=RED_ERR)
        self.err_lbl.pack(anchor="w", pady=(4, 0))

        # ── Resultado (escondido inicialmente) ──
        self.result_frame = tk.Frame(self.root, bg=CREAM)

        # título
        tk.Label(self.result_frame, text="Distribuição de caixas",
                 font=tkfont.Font(family="Georgia", size=12, weight="bold"),
                 bg=CREAM, fg=CHOC).pack(anchor="w", padx=2, pady=(14, 6))

        # grid 2x2
        grid = tk.Frame(self.result_frame, bg=CREAM)
        grid.pack(fill="x")

        self.lbl_G = self._make_box_card(grid, 0, 0, "📦", "Grande", "30 bombons / caixa")
        self.lbl_M = self._make_box_card(grid, 0, 1, "🗃️", "Média",  "10 bombons / caixa")
        self.lbl_P = self._make_box_card(grid, 1, 0, "🧁", "Pequena","2 bombons / caixa")
        self.lbl_R = self._make_leftover(grid, 1, 1)

        grid.columnconfigure(0, weight=1, minsize=220)
        grid.columnconfigure(1, weight=1, minsize=220)

        # barra resumo
        self._make_summary_bar()

        # botão reset
        reset_btn = tk.Button(
            self.result_frame, text="↩  Nova consulta",
            font=self.f_reset, bg=CREAM, fg=CHOC,
            activebackground=LIGHTBG, relief="flat", bd=1,
            highlightbackground=CARA, cursor="hand2",
            command=self._resetar, padx=14, pady=5
        )
        reset_btn.pack(pady=(10, 0))

    # ── Card de caixa ─────────────────────────────────────────
    def _make_box_card(self, parent, row, col, icon, name, cap):
        frame = tk.Frame(parent, bg=CARDBG, bd=0,
                         highlightthickness=1,
                         highlightbackground=CARA,
                         padx=12, pady=10)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        tk.Label(frame, text=icon, font=tkfont.Font(size=20),
                 bg=CARDBG).pack(anchor="w")
        tk.Label(frame, text=name.upper(), font=self.f_card_s,
                 bg=CARDBG, fg=CARA).pack(anchor="w")
        tk.Label(frame, text=name, font=self.f_card_t,
                 bg=CARDBG, fg=CHOC).pack(anchor="w")
        tk.Label(frame, text=cap, font=self.f_card_s,
                 bg=CARDBG, fg="#8C6A3A").pack(anchor="w", pady=(0, 6))

        count_lbl = tk.Label(frame, text="0 caixas",
                             font=self.f_count, bg=CARDBG, fg=CHOC)
        count_lbl.pack(anchor="w")

        return count_lbl

    # ── Card sobra ────────────────────────────────────────────
    def _make_leftover(self, parent, row, col):
        frame = tk.Frame(parent, bg=CHOC, padx=12, pady=10)
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        tk.Label(frame, text="RESTANTE", font=self.f_card_s,
                 bg=CHOC, fg=BLUSH).pack(anchor="w")
        tk.Label(frame, text="Sem caixa", font=self.f_card_t,
                 bg=CHOC, fg=CREAM).pack(anchor="w", pady=(2, 10))

        count_lbl = tk.Label(frame, text="0 un.",
                             font=self.f_count, bg=CHOC, fg=GOLD)
        count_lbl.pack(anchor="e")
        return count_lbl

    # ── Barra resumo ──────────────────────────────────────────
    def _make_summary_bar(self):
        bar = tk.Frame(self.result_frame, bg=LIGHTBG,
                       highlightthickness=1,
                       highlightbackground=CARA,
                       padx=16, pady=10)
        bar.pack(fill="x", pady=(8, 0))

        self.s_caixas = self._sum_item(bar, "0", "Caixas usadas")
        tk.Frame(bar, bg=CARA, width=1).pack(side="left", fill="y", padx=12)
        self.s_emb    = self._sum_item(bar, "0", "Embalados")
        tk.Frame(bar, bg=CARA, width=1).pack(side="left", fill="y", padx=12)
        self.s_efic   = self._sum_item(bar, "0%", "Eficiência")

    def _sum_item(self, parent, val, key):
        f = tk.Frame(parent, bg=LIGHTBG)
        f.pack(side="left", expand=True)
        v = tk.Label(f, text=val, font=self.f_sum_v, bg=LIGHTBG, fg=CHOC)
        v.pack()
        tk.Label(f, text=key.upper(), font=self.f_sum_k,
                 bg=LIGHTBG, fg=CARA).pack()
        return v

    # ── Lógica de cálculo ─────────────────────────────────────
    def _calcular(self):
        raw = self.entry_var.get().strip()
        if not raw.isdigit():
            self.err_lbl.config(text="⚠ Insira um número válido.")
            return
        self.err_lbl.config(text="")

        total = int(raw)

        grandes  = total // 30
        resto    = total % 30
        medias   = resto  // 10
        resto    = resto  % 10
        pequenas = resto  // 2
        sobra    = resto  % 2

        embalados   = total - sobra
        total_cx    = grandes + medias + pequenas
        efic        = round((embalados / total) * 100) if total > 0 else 0

        # atualizar labels
        self.lbl_G.config(text=f"{grandes} caixa{'s' if grandes!=1 else ''}")
        self.lbl_M.config(text=f"{medias} caixa{'s' if medias!=1 else ''}")
        self.lbl_P.config(text=f"{pequenas} caixa{'s' if pequenas!=1 else ''}")
        self.lbl_R.config(text=f"{sobra} un.")
        self.s_caixas.config(text=str(total_cx))
        self.s_emb.config(text=str(embalados))
        self.s_efic.config(text=f"{efic}%")

        # balão do Zé
        frase = random.choice(FRASES)(total)
        self.bubble_var.set(frase)
        self.bubble_lbl.pack(fill="x", padx=20, pady=(10, 0))

        # mostrar resultados
        self.result_frame.pack(fill="x", padx=20, pady=(0, 20))

    def _resetar(self):
        self.entry_var.set("")
        self.err_lbl.config(text="")
        self.result_frame.pack_forget()
        self.bubble_lbl.pack_forget()
        self.entry.focus()

    # ── Animação do mascote ───────────────────────────────────
    def _draw_mascot(self, offset):
        c = self.canvas
        c.delete("all")
        y = offset  # sobe/desce

        # sombra
        c.create_oval(17, 105+y, 73, 112+y, fill="#2C1A0E", outline="", stipple="gray25")

        # botas
        c.create_rectangle(26, 90+y, 42, 100+y, fill="#2C1A0E", outline="", width=0)
        c.create_rectangle(48, 90+y, 64, 100+y, fill="#2C1A0E", outline="", width=0)
        c.create_oval(18, 95+y, 46, 105+y, fill="#1A0F06", outline="")
        c.create_oval(44, 95+y, 72, 105+y, fill="#1A0F06", outline="")

        # pernas
        c.create_rectangle(28, 68+y, 42, 92+y, fill="#3D2B1F", outline="")
        c.create_rectangle(48, 68+y, 62, 92+y, fill="#3D2B1F", outline="")

        # torso
        c.create_rectangle(18, 44+y, 72, 72+y, fill="#C47A2B", outline="")
        c.create_rectangle(41, 45+y, 49, 71+y, fill="#A86220", outline="")
        c.create_rectangle(22, 56+y, 38, 67+y, fill="#A86220", outline="")

        # pescoço
        c.create_rectangle(37, 36+y, 53, 46+y, fill="#D4956A", outline="")

        # braço esquerdo + caixas
        sx = int(math.sin(self._anim_phase * 0.5) * 4)
        c.create_rectangle(4, 46+y+sx, 20, 54+y+sx, fill="#C47A2B", outline="")
        c.create_oval(0, 52+y+sx, 16, 62+y+sx, fill="#D4906A", outline="")
        # braço direito
        c.create_rectangle(70, 46+y-sx, 86, 54+y-sx, fill="#C47A2B", outline="")
        c.create_oval(74, 52+y-sx, 90, 62+y-sx, fill="#D4906A", outline="")

        # caixas (flutuam com braços)
        bx = sx // 2
        # grande
        c.create_rectangle(8, 28+y+bx, 82, 46+y+bx, fill="#E8C49A", outline="#C47A2B")
        c.create_line(8, 37+y+bx, 82, 37+y+bx, fill="#C47A2B")
        # média
        c.create_rectangle(14, 16+y+bx, 76, 30+y+bx, fill="#FDF7EE", outline="#C47A2B")
        # pequena
        c.create_rectangle(22, 6+y+bx, 68, 18+y+bx, fill="#FBF0DC", outline="#E8A830")

        # cabeça
        c.create_oval(19, 5+y, 71, 36+y, fill="#E8A870", outline="")
        # orelhas
        c.create_oval(13, 12+y, 23, 28+y, fill="#D4906A", outline="")
        c.create_oval(67, 12+y, 77, 28+y, fill="#D4906A", outline="")

        # boné aba
        c.create_rectangle(15, 8+y, 75, 14+y, fill="#2C1A0E", outline="")
        # boné topo
        c.create_arc(18, 1+y, 72, 22+y, start=0, extent=180, fill="#C47A2B", outline="")
        # badge
        c.create_oval(39, 3+y, 51, 13+y, fill="#E8A830", outline="")
        c.create_text(45, 8+y, text="ZB", font=("Courier", 5, "bold"), fill="#2C1A0E")

        # sobrancelhas
        c.create_line(30, 17+y, 40, 14+y, fill="#2C1A0E", width=2, capstyle="round")
        c.create_line(50, 14+y, 60, 17+y, fill="#2C1A0E", width=2, capstyle="round")

        # olhos
        blink = abs(math.sin(self._anim_phase * 0.3)) > 0.97
        ey = 3 if not blink else 0
        c.create_oval(29, 20+y, 41, 20+ey+y, fill="white", outline="")
        c.create_oval(49, 20+y, 61, 20+ey+y, fill="white", outline="")
        if not blink:
            c.create_oval(33, 22+y, 39, 28+y, fill="#3D2B1F", outline="")
            c.create_oval(53, 22+y, 59, 28+y, fill="#3D2B1F", outline="")
            c.create_oval(33, 22+y, 36, 25+y, fill="white", outline="")
            c.create_oval(53, 22+y, 56, 25+y, fill="white", outline="")

        # sorriso
        c.create_arc(32, 27+y, 58, 38+y, start=200, extent=140,
                     style="arc", outline="#2C1A0E", width=2)

    def _animate_mascot(self, frame):
        self._anim_phase = frame * 0.08
        offset = int(math.sin(self._anim_phase) * 4)
        self._draw_mascot(offset)
        self.root.after(50, self._animate_mascot, frame + 1)


if __name__ == "__main__":
    root = tk.Tk()
    app = ZeBombomApp(root)
    root.mainloop()