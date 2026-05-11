"""
Password Position Calculator v1.0
Laboratorium Elektroniki | laboratoriumelektroniki.pl
Author: Krystian Zarzecki

Shows the exact brute-force position of any password and estimated crack time.
Educational tool for digital forensics and security research.
"""
import tkinter as tk
from tkinter import ttk
import sys, os, math

# ── ICON ──────────────────────────────────────────────────────────────────────
def set_icon(root):
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    ico = os.path.join(base, "icon.ico")
    if os.path.exists(ico):
        try: root.iconbitmap(ico)
        except: pass

# ── CHARSETS ──────────────────────────────────────────────────────────────────
SETS = {
    "digits":  "0123456789",
    "lower":   "abcdefghijklmnopqrstuvwxyz",
    "upper":   "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "special": "!@#$%^&*()_+-=[]{}|;':\",./<>?`~\\",
}

SPEEDS = [
    (100,       "Manual / slow script"),
    (1_000,     "Simple Python script"),
    (10_000,    "Optimized script"),
    (100_000,   "John the Ripper CPU"),
    (1_000_000, "Hashcat CPU (MD5)"),
    (10_000_000,"Hashcat GPU budget"),
    (100_000_000,"Hashcat GPU mid-range"),
    (1_000_000_000,"Hashcat GPU high-end"),
    (10_000_000_000,"GPU cluster / cloud"),
    (10_000_000_000_000,"Distributed / ASIC top"),
]

# ── THEME ─────────────────────────────────────────────────────────────────────
BG   = "#F5F7FA"
CARD = "#FFFFFF"
BORD = "#D0D7E2"
ACC  = "#1E50A0"
ACC2 = "#E8EEF8"
TX   = "#1A2540"
TX2  = "#5A6480"
OK   = "#1A8A4A"
WARN = "#C07000"
ERR  = "#C02020"
BTN  = "#FFFFFF"

def card_frame(parent, **kw):
    return tk.Frame(parent, bg=CARD, relief="flat", bd=0,
                    highlightbackground=BORD, highlightthickness=1, **kw)

def section_bar(parent, text):
    f = tk.Frame(parent, bg=ACC)
    tk.Label(f, text=text, font=("Segoe UI", 9, "bold"),
             bg=ACC, fg=BTN).pack(anchor="w", padx=8, pady=3)
    return f

# ── MATH ──────────────────────────────────────────────────────────────────────
def get_alphabet(states: dict) -> str:
    a = ""
    for k, v in states.items():
        if v:
            a += SETS[k]
    return a

def position_in_bruteforce(password: str, alphabet: str) -> int:
    """
    Returns the 1-based position of `password` in the brute-force sequence
    ordered: all length-1 strings, then length-2, etc., within each length
    lexicographically by alphabet order.
    """
    n = len(alphabet)
    length = len(password)
    # offset: all shorter strings
    offset = sum(n**l for l in range(1, length))
    # position within same-length strings (lex order by alphabet)
    pos = 0
    for i, ch in enumerate(password):
        idx = alphabet.index(ch)
        pos = pos * n + idx
    return offset + pos + 1  # 1-based

def total_space(n: int, length: int) -> int:
    """Total combinations for all lengths from 1 to `length`."""
    return sum(n**l for l in range(1, length + 1))

def format_big(n: float) -> str:
    if n < 1_000:
        return f"{int(n):,}"
    for suffix, div in [("T", 1e12), ("B", 1e9), ("M", 1e6), ("K", 1e3)]:
        if n >= div:
            return f"{n/div:.2f} {suffix}"
    return f"{n:.2e}"

def format_time(seconds: float) -> str:
    if seconds < 0.001:
        return "< 1 ms"
    if seconds < 1:
        return f"{seconds*1000:.1f} ms"
    if seconds < 60:
        return f"{seconds:.1f} s"
    if seconds < 3600:
        return f"{seconds/60:.1f} min"
    if seconds < 86400:
        return f"{seconds/3600:.1f} h"
    if seconds < 86400*365:
        return f"{seconds/86400:.1f} days"
    if seconds < 86400*365*1000:
        return f"{seconds/86400/365:.1f} years"
    if seconds < 86400*365*1e9:
        return f"{seconds/86400/365/1000:.2f} thousand years"
    if seconds < 86400*365*1e12:
        return f"{seconds/86400/365/1e6:.2f} million years"
    return f"{seconds/86400/365/1e9:.2f} billion years"

def strength_label(pct: float, pos: int, space: int) -> tuple:
    """Returns (text, color) strength assessment."""
    ratio = pos / space if space > 0 else 0
    if ratio < 0.01:
        return "Very Weak — found in first 1% of search", ERR
    if ratio < 0.10:
        return "Weak — found in first 10% of search", ERR
    if ratio < 0.40:
        return "Below Average", WARN
    if ratio < 0.70:
        return "Average", WARN
    if ratio < 0.90:
        return "Good", OK
    return "Excellent — in last 10% of search space", OK


# ── APP ───────────────────────────────────────────────────────────────────────
class PasswordPositionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Position Calculator v1.0  |  Laboratorium Elektroniki")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        self.root.geometry("660x780")
        set_icon(root)

        self.charset_states = {k: tk.BooleanVar(value=(k in ("digits","lower")))
                               for k in SETS}
        self.speed_idx = tk.IntVar(value=4)
        self.show_pw = tk.BooleanVar(value=False)

        style = ttk.Style()
        style.theme_use("clam")
        for w in ("TCheckbutton", "TRadiobutton"):
            style.configure(w, background=CARD, foreground=TX, font=("Segoe UI", 9))
            style.map(w, background=[("active", CARD)])
        style.configure("TScale", background=BG, troughcolor=BORD)

        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        hdr = tk.Frame(self.root, bg=ACC)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🔐  Password Position Calculator",
                 font=("Segoe UI", 13, "bold"), bg=ACC, fg=BTN).pack(side="left", padx=14, pady=8)
        tk.Label(hdr, text="v1.0", font=("Segoe UI", 9),
                 bg=ACC, fg="#A0C0E8").pack(side="left")

        tk.Label(self.root,
                 text="Enter a password to see its exact position in a brute-force sequence  |  Laboratorium Elektroniki",
                 font=("Segoe UI", 8), bg=BG, fg=TX2).pack(fill="x", padx=10, pady=(4, 2))

        P = self.root  # shorthand

        # ── Password Input ──
        c1 = card_frame(P); c1.pack(fill="x", padx=10, pady=(4, 2))
        section_bar(c1, "🔑  Password").pack(fill="x")
        row = tk.Frame(c1, bg=CARD); row.pack(fill="x", padx=8, pady=8)
        self._pw_var = tk.StringVar()
        self._pw_entry = tk.Entry(row, textvariable=self._pw_var,
                                  font=("Courier New", 14), bg=ACC2, fg=TX,
                                  relief="flat", bd=6, show="●", width=30)
        self._pw_entry.pack(side="left", fill="x", expand=True)
        self._pw_entry.bind("<Return>", lambda e: self.calculate())
        self._pw_entry.bind("<KeyRelease>", lambda e: self.calculate())

        show_cb = ttk.Checkbutton(row, text="Show", variable=self.show_pw,
                                   command=self._toggle_show)
        show_cb.pack(side="left", padx=(8, 0))

        tk.Button(row, text="Calculate", command=self.calculate,
                  bg=ACC, fg=BTN, font=("Segoe UI", 9, "bold"),
                  relief="flat", cursor="hand2", padx=12).pack(side="left", padx=(6, 0))

        # ── Charset ──
        c2 = card_frame(P); c2.pack(fill="x", padx=10, pady=2)
        section_bar(c2, "🔤  Character Set").pack(fill="x")
        cf = tk.Frame(c2, bg=CARD); cf.pack(fill="x", padx=8, pady=6)
        labels = {
            "digits":  "🔢  Digits (0-9)",
            "lower":   "🔡  Lowercase (a-z)",
            "upper":   "🔠  Uppercase (A-Z)",
            "special": "🔣  Special (!@#…)",
        }
        for k, lbl_text in labels.items():
            ttk.Checkbutton(cf, text=lbl_text, variable=self.charset_states[k],
                             command=self.calculate).pack(side="left", padx=8)

        self._alpha_info = tk.Label(c2, text="Alphabet: 36 chars",
                                    font=("Segoe UI", 8), bg=CARD, fg=TX2)
        self._alpha_info.pack(anchor="w", padx=8, pady=(0, 6))

        # ── Speed ──
        c3 = card_frame(P); c3.pack(fill="x", padx=10, pady=2)
        section_bar(c3, "⚡  Attack Speed").pack(fill="x")
        sf = tk.Frame(c3, bg=CARD); sf.pack(fill="x", padx=8, pady=6)
        ttk.Scale(sf, from_=0, to=len(SPEEDS)-1, variable=self.speed_idx,
                  orient="horizontal", command=lambda v: self.calculate()).pack(
                  fill="x", pady=(0, 4))
        self._speed_lbl = tk.Label(c3, text="", font=("Segoe UI", 9, "bold"),
                                    bg=CARD, fg=ACC)
        self._speed_lbl.pack(anchor="w", padx=8)
        self._speed_desc = tk.Label(c3, text="", font=("Segoe UI", 8),
                                     bg=CARD, fg=TX2)
        self._speed_desc.pack(anchor="w", padx=8, pady=(0, 6))

        # ── Results ──
        c4 = card_frame(P); c4.pack(fill="x", padx=10, pady=2)
        section_bar(c4, "📊  Results").pack(fill="x")
        grid = tk.Frame(c4, bg=CARD); grid.pack(fill="x", padx=8, pady=8)

        self._cards = {}
        card_defs = [
            ("position",    "Position in BF",     "—", "1-based sequence number"),
            ("alphabet",    "Alphabet size",       "—", "available characters"),
            ("length",      "Password length",     "—", "characters"),
            ("space",       "Total combinations",  "—", "all lengths up to this"),
        ]
        for i, (key, title, val, sub) in enumerate(card_defs):
            cf2 = tk.Frame(grid, bg=ACC2, relief="flat", bd=0,
                           highlightbackground=BORD, highlightthickness=1)
            cf2.grid(row=0, column=i, padx=4, pady=2, sticky="nsew")
            grid.columnconfigure(i, weight=1)
            tk.Label(cf2, text=title, font=("Segoe UI", 8),
                     bg=ACC2, fg=TX2).pack(anchor="w", padx=6, pady=(4, 0))
            v_lbl = tk.Label(cf2, text=val, font=("Segoe UI", 13, "bold"),
                             bg=ACC2, fg=ACC)
            v_lbl.pack(anchor="w", padx=6)
            tk.Label(cf2, text=sub, font=("Segoe UI", 7),
                     bg=ACC2, fg=TX2).pack(anchor="w", padx=6, pady=(0, 4))
            self._cards[key] = v_lbl

        # Progress bar
        bar_frame = tk.Frame(c4, bg=CARD); bar_frame.pack(fill="x", padx=8, pady=(4, 2))
        bar_top = tk.Frame(bar_frame, bg=CARD); bar_top.pack(fill="x")
        tk.Label(bar_top, text="Progress to password:", font=("Segoe UI", 8),
                 bg=CARD, fg=TX2).pack(side="left")
        self._pct_lbl = tk.Label(bar_top, text="—", font=("Segoe UI", 8, "bold"),
                                  bg=CARD, fg=ACC)
        self._pct_lbl.pack(side="right")
        bar_bg = tk.Frame(bar_frame, bg=BORD, height=10)
        bar_bg.pack(fill="x", pady=2)
        self._bar = tk.Frame(bar_bg, bg=ACC, height=10)
        self._bar.place(x=0, y=0, relheight=1, relwidth=0)

        # Strength
        self._strength_lbl = tk.Label(c4, text="", font=("Segoe UI", 9, "bold"),
                                       bg=CARD, fg=TX2)
        self._strength_lbl.pack(anchor="w", padx=8, pady=(4, 2))

        # ── Time estimates ──
        c5 = card_frame(P); c5.pack(fill="x", padx=10, pady=2)
        section_bar(c5, "⏱  Time Estimates").pack(fill="x")
        tgrid = tk.Frame(c5, bg=CARD); tgrid.pack(fill="x", padx=8, pady=8)

        self._time_cards = {}
        time_defs = [
            ("to_pos",  "To reach this password"),
            ("full",    "Exhaust full space"),
            ("half",    "50% of search space"),
        ]
        for i, (key, title) in enumerate(time_defs):
            tf = tk.Frame(tgrid, bg=ACC2, relief="flat", bd=0,
                          highlightbackground=BORD, highlightthickness=1)
            tf.grid(row=0, column=i, padx=4, sticky="nsew")
            tgrid.columnconfigure(i, weight=1)
            tk.Label(tf, text=title, font=("Segoe UI", 8),
                     bg=ACC2, fg=TX2).pack(anchor="w", padx=6, pady=(4, 0))
            v = tk.Label(tf, text="—", font=("Segoe UI", 11, "bold"),
                         bg=ACC2, fg=ACC)
            v.pack(anchor="w", padx=6, pady=(0, 4))
            self._time_cards[key] = v

        # ── Warning ──
        c6 = card_frame(P); c6.pack(fill="x", padx=10, pady=(2, 8))
        tk.Label(c6,
                 text="⚠  For authorized forensic and security research use only. "
                      "No data leaves this computer.",
                 font=("Segoe UI", 8), bg=CARD, fg=TX2, wraplength=600,
                 justify="left").pack(padx=8, pady=4)

        # Footer
        tk.Label(P,
                 text="Laboratorium Elektroniki  |  Password Position Calculator v1.0  |  laboratoriumelektroniki.pl",
                 font=("Segoe UI", 7), bg=BG, fg=TX2).pack(pady=4)

        self._update_speed_label()
        self._update_alpha_info()

    def _toggle_show(self):
        self._pw_entry.config(show="" if self.show_pw.get() else "●")

    def _update_speed_label(self):
        idx = int(self.speed_idx.get())
        speed, desc = SPEEDS[idx]
        self._speed_lbl.config(text=f"{speed:,} attempts/s")
        self._speed_desc.config(text=desc)

    def _update_alpha_info(self):
        alpha = get_alphabet({k: v.get() for k, v in self.charset_states.items()})
        preview = alpha[:60] + ("…" if len(alpha) > 60 else "")
        self._alpha_info.config(
            text=f"Alphabet: {len(alpha)} chars  |  {preview}")

    def calculate(self, *_):
        self._update_speed_label()
        self._update_alpha_info()

        pw = self._pw_var.get()
        if not pw:
            self._clear_results()
            return

        states = {k: v.get() for k, v in self.charset_states.items()}
        alpha = get_alphabet(states)

        if not alpha:
            self._set_error("Select at least one character set.")
            return

        missing = [c for c in pw if c not in alpha]
        if missing:
            self._set_error(f"Characters not in alphabet: {' '.join(set(missing))}")
            return

        try:
            pos   = position_in_bruteforce(pw, alpha)
            space = total_space(len(alpha), len(pw))
            pct   = (pos / space) * 100
            speed = SPEEDS[int(self.speed_idx.get())][0]

            self._cards["position"].config(text=format_big(pos), fg=ACC)
            self._cards["alphabet"].config(text=str(len(alpha)), fg=ACC)
            self._cards["length"].config(text=str(len(pw)), fg=ACC)
            self._cards["space"].config(text=format_big(space), fg=ACC)

            rel_w = max(0.005, min(1.0, pct / 100))
            self._bar.place(relwidth=rel_w)
            self._pct_lbl.config(text=f"{pct:.4f}%")

            s_text, s_color = strength_label(pct, pos, space)
            self._strength_lbl.config(text=f"Position assessment: {s_text}", fg=s_color)

            self._time_cards["to_pos"].config(text=format_time(pos / speed), fg=ACC)
            self._time_cards["full"].config(text=format_time(space / speed), fg=ACC)
            self._time_cards["half"].config(text=format_time(space / speed / 2), fg=ACC)

        except Exception as e:
            self._set_error(str(e))

    def _clear_results(self):
        for v in self._cards.values(): v.config(text="—", fg=ACC)
        for v in self._time_cards.values(): v.config(text="—", fg=ACC)
        self._bar.place(relwidth=0)
        self._pct_lbl.config(text="—")
        self._strength_lbl.config(text="")

    def _set_error(self, msg):
        self._cards["position"].config(text="⚠ Error", fg=ERR)
        self._strength_lbl.config(text=msg, fg=ERR)
        for k in ("alphabet","length","space"):
            self._cards[k].config(text="—", fg=ACC)
        for v in self._time_cards.values():
            v.config(text="—", fg=ACC)
        self._bar.place(relwidth=0)
        self._pct_lbl.config(text="—")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordPositionCalculator(root)
    root.mainloop()
