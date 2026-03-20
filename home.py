import customtkinter as ctk
from tkinter import Canvas, messagebox
import database as db
from datetime import datetime
import math
import random

# ─────────────────────────────────────────
# NSBM COLOR PALETTE
# ─────────────────────────────────────────
C_BG1       = "#050d1a"
C_BG2       = "#0a1628"
C_NAVY      = "#235895"
C_GREEN     = "#60b94b"
C_LIME      = "#cfff5a"
C_WHITE     = "#ffffff"
C_CARD1     = "#0d1f35"
C_CARD2     = "#102540"
C_BORDER    = "#1e4a7a"
C_GLOW      = "#60b94b"
C_GRAY      = "#aabbcc"
C_SIDEBAR   = "#060e1c"
C_TOPBAR    = "#080f1f"
RED         = "#ef4444"
GOLD        = "#f59e0b"
PURPLE      = "#a855f7"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─────────────────────────────────────────
# GLASS CARD CANVAS
# ─────────────────────────────────────────
class GlassCard(Canvas):
    """Simulates glassmorphism using Canvas."""
    def __init__(self, parent, width, height,
                 color=C_CARD1, border=C_BORDER,
                 radius=16, **kwargs):
        super().__init__(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bg=C_BG2,
            **kwargs
        )
        self.card_w  = width
        self.card_h  = height
        self.color   = color
        self.border  = border
        self.radius  = radius
        self._draw()
        self._glow_step = 0
        self._animate_glow()

    def _draw(self):
        self.delete("card")
        r = self.radius
        w = self.card_w
        h = self.card_h

        # Draw layered glass effect
        for i, (c, inset) in enumerate([
            (self._lighten(self.color, 20), 0),
            (self._lighten(self.color, 10), 1),
            (self.color,                    2),
        ]):
            self._rounded_rect(
                inset, inset,
                w-inset, h-inset,
                r-inset, c, "", "card"
            )

        # Border glow
        self._rounded_rect(
            0, 0, w, h, r,
            "", self.border, "card"
        )

        # Top shine line
        self._rounded_rect(
            2, 2, w-2, 8, 3,
            self._lighten(self.color, 40),
            "", "card"
        )

    def _rounded_rect(self, x1, y1, x2, y2,
                      r, fill, outline, tag):
        self.create_polygon(
            x1+r, y1,
            x2-r, y1,
            x2,   y1+r,
            x2,   y2-r,
            x2-r, y2,
            x1+r, y2,
            x1,   y2-r,
            x1,   y1+r,
            smooth=True,
            fill=fill,
            outline=outline,
            tags=tag
        )

    def _lighten(self, color, amount):
        r = min(255, int(color[1:3], 16) + amount)
        g = min(255, int(color[3:5], 16) + amount)
        b = min(255, int(color[5:7], 16) + amount)
        return f'#{r:02x}{g:02x}{b:02x}'

    def _animate_glow(self):
        self._glow_step += 0.05
        pulse  = abs(math.sin(self._glow_step))
        amount = int(pulse * 15)
        border = self._lighten(self.border, amount)
        self.delete("border_glow")
        self._rounded_rect(
            0, 0,
            self.card_w, self.card_h,
            self.radius,
            "", border, "border_glow"
        )
        self.after(50, self._animate_glow)

    def place_widget(self, widget, x, y):
        """Place a widget inside the canvas."""
        self.create_window(x, y, window=widget, anchor="nw")

# ─────────────────────────────────────────
# ANIMATED BACKGROUND
# ─────────────────────────────────────────

# ─────────────────────────────────────────
# ANIMATED COUNTER
# ─────────────────────────────────────────
class AnimatedCounter(ctk.CTkLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target  = 0
        self._current = 0

    def count_to(self, target):
        self._target  = int(target)
        self._current = 0
        self._run()

    def _run(self):
        if self._current < self._target:
            step = max(1, int((self._target-self._current)/6))
            self._current = min(self._current+step, self._target)
            self.configure(text=str(self._current))
            self.after(25, self._run)
        else:
            self.configure(text=str(self._target))

# ─────────────────────────────────────────
# GLOW BUTTON
# ─────────────────────────────────────────
class GlowButton(ctk.CTkButton):
    def __init__(self, *args, glow_color=C_GREEN, **kwargs):
        super().__init__(*args, **kwargs)
        self.glow_color = glow_color
        self._glowing   = False
        self._step      = 0
        self.bind("<Enter>", self._glow_on)
        self.bind("<Leave>", self._glow_off)

    def _glow_on(self, e=None):
        self._glowing = True
        self._step    = 0
        self._animate()

    def _glow_off(self, e=None):
        self._glowing = False
        self.configure(border_color=C_BORDER, border_width=1)

    def _animate(self):
        if not self._glowing:
            return
        self._step += 0.25
        pulse = abs(math.sin(self._step))
        self.configure(
            border_color=self.glow_color,
            border_width=int(1 + pulse * 3)
        )
        self.after(40, self._animate)

# ─────────────────────────────────────────
# SIDEBAR BUTTON
# ─────────────────────────────────────────
class SidebarBtn(ctk.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = False
        self.bind("<Enter>", self._hover_on)
        self.bind("<Leave>", self._hover_off)

    def set_active(self, val):
        self._active = val
        if val:
            self.configure(
                fg_color=C_NAVY,
                text_color=C_LIME,
                border_color=C_GREEN,
                border_width=1
            )
        else:
            self.configure(
                fg_color=C_SIDEBAR,
                text_color=C_GRAY,
                border_color=C_SIDEBAR,
                border_width=0
            )

    def _hover_on(self, e=None):
        if not self._active:
            self.configure(fg_color=C_CARD1, text_color=C_WHITE)

    def _hover_off(self, e=None):
        if not self._active:
            self.configure(fg_color=C_SIDEBAR, text_color=C_GRAY)

# ─────────────────────────────────────────
# HOME APP
# ─────────────────────────────────────────
class HomeApp(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.user          = user
        self.nav_btn_list  = []

        self.title("NSBM Smart Attendance System")
        self.geometry("1200x750")
        self.configure(fg_color=C_BG1)
        self._center(1200, 750)
        self._build()

    def _center(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):

        # ── SIDEBAR ──────────────────────
        self.sidebar = ctk.CTkFrame(
            self, fg_color=C_SIDEBAR,
            width=245, corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Green accent line
        ctk.CTkFrame(
            self.sidebar,
            width=3, fg_color=C_GREEN,
            corner_radius=0
        ).place(x=0, y=0, relheight=1)

        # Logo
        logo = ctk.CTkFrame(
            self.sidebar,
            fg_color=C_CARD1,
            corner_radius=0, height=110
        )
        logo.pack(fill="x")
        logo.pack_propagate(False)

        ctk.CTkLabel(
            logo, text="🎓",
            font=ctk.CTkFont(size=38)
        ).pack(pady=(12, 0))

        ctk.CTkLabel(
            logo,
            text="NSBM",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=C_LIME
        ).pack()

        ctk.CTkLabel(
            logo,
            text="Smart Attendance",
            font=ctk.CTkFont(size=10),
            text_color=C_GRAY
        ).pack(pady=(0, 8))

        # User card
        uc = ctk.CTkFrame(
            self.sidebar,
            fg_color=C_CARD2,
            corner_radius=12,
            border_color=C_BORDER,
            border_width=1
        )
        uc.pack(fill="x", padx=12, pady=12)

        ctk.CTkLabel(
            uc,
            text=f"👤  {self.user['full_name']}",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=C_WHITE,
            wraplength=195,
            anchor="w"
        ).pack(fill="x", padx=12, pady=(10, 2))

        role_c = {
            'admin': C_LIME,
            'lecturer': C_GREEN,
            'student': C_GRAY
        }.get(self.user['role'], C_WHITE)

        ctk.CTkLabel(
            uc,
            text=f"🔑  {self.user['role'].capitalize()}",
            font=ctk.CTkFont(size=11),
            text_color=role_c
        ).pack(anchor="w", padx=12, pady=(0, 10))

        # Divider
        ctk.CTkFrame(
            self.sidebar,
            height=1, fg_color=C_BORDER
        ).pack(fill="x", padx=15)

        ctk.CTkLabel(
            self.sidebar,
            text="MENU",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=C_GRAY
        ).pack(anchor="w", padx=22, pady=(10, 5))

        # Nav items
        nav_items = [
            ("🏠", "Home",             self.show_home),
            ("📸", "Register Student", self.open_register),
            ("🎯", "Mark Attendance",  self.open_attendance),
            ("📊", "Reports",          self.open_reports),
        ]
        if self.user['role'] == 'admin':
            nav_items.append(("⚙️", "Settings", self.open_settings))

        for icon, label, cmd in nav_items:
            btn = SidebarBtn(
                self.sidebar,
                text=f"   {icon}   {label}",
                height=44,
                font=ctk.CTkFont(size=13),
                fg_color=C_SIDEBAR,
                text_color=C_GRAY,
                anchor="w",
                corner_radius=10,
                border_color=C_SIDEBAR,
                border_width=0,
                command=lambda c=cmd: self._nav(c)
            )
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_btn_list.append((btn, cmd))

        # Bottom divider + logout
        ctk.CTkFrame(
            self.sidebar,
            height=1, fg_color=C_BORDER
        ).pack(side="bottom", fill="x", padx=15, pady=5)

        GlowButton(
            self.sidebar,
            text="   🚪   Logout",
            height=44,
            font=ctk.CTkFont(size=13),
            fg_color=C_SIDEBAR,
            hover_color="#1a0000",
            text_color=RED,
            anchor="w",
            corner_radius=10,
            border_color=C_SIDEBAR,
            border_width=0,
            glow_color=RED,
            command=self._logout
        ).pack(side="bottom", fill="x", padx=10, pady=(0, 5))

        # ── MAIN FRAME ───────────────────
        self.main = ctk.CTkFrame(
            self, fg_color=C_BG2,
            corner_radius=0
        )
        self.main.pack(side="right", fill="both", expand=True)

        # Set first button active
        self._set_active(0)
        self.show_home()

    def _nav(self, cmd):
        for i, (btn, c) in enumerate(self.nav_btn_list):
            self._set_active(i) if c == cmd else None
        cmd()

    def _set_active(self, idx):
        for i, (btn, _) in enumerate(self.nav_btn_list):
            btn.set_active(i == idx)

    def _clear(self):
        for w in self.main.winfo_children():
            w.destroy()

    # ─────────────────────────────────────
    # HOME SCREEN
    # ─────────────────────────────────────
    def show_home(self):
        self._clear()

        # Animated background

        # Top bar
        topbar = ctk.CTkFrame(
            self.main,
            fg_color=C_TOPBAR,
            corner_radius=0, height=60
        )
        topbar.place(x=0, y=0, relwidth=1)
        topbar.pack_propagate(False)

        ctk.CTkLabel(
            topbar,
            text="🏠  Dashboard",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=C_WHITE
        ).pack(side="left", padx=25, pady=16)

        self.clock_lbl = ctk.CTkLabel(
            topbar, text="",
            font=ctk.CTkFont(size=11),
            text_color=C_GRAY
        )
        self.clock_lbl.pack(side="right", padx=25)
        self._tick()

        # Scrollable content
        scroll = ctk.CTkScrollableFrame(
            self.main,
            fg_color=C_BG2,
            corner_radius=0,
            scrollbar_button_color=C_NAVY,
            scrollbar_button_hover_color=C_GREEN
        )
        scroll.place(x=0, y=60, relwidth=1, relheight=1)
        scroll.configure(fg_color=C_BG2)


## Why This Works


        # Welcome banner
        banner = ctk.CTkFrame(
            scroll,
            fg_color=C_CARD2,
            corner_radius=18,
            border_color=C_GREEN,
            border_width=1
        )
        banner.pack(fill="x", padx=20, pady=(15, 15))

        # Animated lime bar
        bar = ctk.CTkFrame(
            banner, fg_color=C_LIME,
            height=4, corner_radius=2
        )
        bar.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            banner,
            text=f"Welcome back, {self.user['full_name']}! 👋",
            font=ctk.CTkFont(size=19, weight="bold"),
            text_color=C_LIME
        ).pack(anchor="w", padx=25, pady=(15, 3))

        ctk.CTkLabel(
            banner,
            text=f"📅 {datetime.now().strftime('%A, %B %d %Y')}"
                 f"   🎓 NSBM Green University"
                 f"   🔑 {self.user['role'].capitalize()}",
            font=ctk.CTkFont(size=12),
            text_color=C_GRAY
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # ── STAT CARDS ───────────────────
        ctk.CTkLabel(
            scroll,
            text="  📊 Today's Overview",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=C_WHITE
        ).pack(anchor="w", padx=20, pady=(5, 8))

        sf = ctk.CTkFrame(scroll, fg_color=C_BG1)
        sf.pack(fill="x", padx=20, pady=(0, 15))

        students   = db.get_all_students()
        attendance = db.get_attendance_today()
        total_s    = len(students)
        present    = len(attendance)
        late       = len([a for a in attendance
                         if 'Late' in a.get('arrival', '')])
        rate       = int((present/total_s)*100) if total_s > 0 else 0

        cards_data = [
            ("👥", "Students",       total_s, C_CARD2,  C_LIME,   C_BORDER),
            ("✅", "Present Today",  present, "#0a2a10", C_GREEN,  "#1a5a2a"),
            ("🔴", "Late Today",     late,    "#1a1200", GOLD,     "#3a2800"),
            ("📊", "Attendance %",   rate,    "#12082a", PURPLE,   "#2a1260"),
        ]

        self.counters = []
        for i, (icon, lbl, val, bg, color, border) in enumerate(cards_data):
            card = ctk.CTkFrame(
                sf,
                fg_color=bg,
                corner_radius=18,
                border_color=border,
                border_width=1
            )
            card.grid(row=0, column=i, padx=8, sticky="ew")
            sf.grid_columnconfigure(i, weight=1)

            # Top color bar
            ctk.CTkFrame(
                card, fg_color=color,
                height=3, corner_radius=0
            ).pack(fill="x")

            ctk.CTkLabel(
                card, text=icon,
                font=ctk.CTkFont(size=26)
            ).pack(pady=(15, 3))

            ctr = AnimatedCounter(
                card, text="0",
                font=ctk.CTkFont(size=34, weight="bold"),
                text_color=color
            )
            ctr.pack()
            self.counters.append((ctr, val))

            suffix = "%" if lbl == "Attendance %" else ""
            ctk.CTkLabel(
                card,
                text=lbl + suffix,
                font=ctk.CTkFont(size=11),
                text_color=C_GRAY
            ).pack(pady=(3, 18))

        self.after(400, self._run_counters)

        # ── QUICK ACTIONS ─────────────────
        ctk.CTkLabel(
            scroll,
            text="  ⚡ Quick Actions",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=C_WHITE
        ).pack(anchor="w", padx=20, pady=(5, 8))

        af = ctk.CTkFrame(scroll, fg_color=C_BG1)
        af.pack(fill="x", padx=20, pady=(0, 15))

        actions = [
            ("📸", "Register\nStudent",  C_GREEN,  "#0a2a10", self.open_register),
            ("🎯", "Mark\nAttendance",   C_NAVY,   "#0a1a3a", self.open_attendance),
            ("📊", "View\nReports",      PURPLE,   "#12082a", self.open_reports),
            ("📧", "Email\nReport",      GOLD,     "#1a1200", self._email),
        ]

        for i, (icon, text, color, bg, cmd) in enumerate(actions):
            btn = GlowButton(
                af,
                text=f"{icon}\n{text}",
                height=90,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color=bg,
                hover_color=C_BG1,
                text_color=color,
                corner_radius=18,
                border_color=color,
                border_width=1,
                glow_color=color,
                command=cmd
            )
            btn.grid(row=0, column=i, padx=8, sticky="ew")
            af.grid_columnconfigure(i, weight=1)

        # ── RECENT ATTENDANCE ─────────────
        ctk.CTkLabel(
            scroll,
            text="  📋 Recent Attendance",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=C_WHITE
        ).pack(anchor="w", padx=20, pady=(5, 8))

        tbl = ctk.CTkFrame(
            scroll,
            fg_color=C_CARD1,
            corner_radius=18,
            border_color=C_BORDER,
            border_width=1
        )
        tbl.pack(fill="x", padx=20, pady=(0, 20))

        # Header row
        hrow = ctk.CTkFrame(
            tbl,
            fg_color=C_NAVY,
            corner_radius=12
        )
        hrow.pack(fill="x", padx=10, pady=(10, 5))

        headers = ["Student ID", "Name", "Course", "Time", "Arrival"]
        widths  = [120, 190, 180, 90, 130]

        for h, w in zip(headers, widths):
            ctk.CTkLabel(
                hrow, text=h,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=C_LIME,
                width=w, anchor="w"
            ).pack(side="left", padx=10, pady=10)

        if attendance:
            for i, rec in enumerate(attendance[:8]):
                bg  = C_CARD1 if i % 2 == 0 else C_CARD2
                row = ctk.CTkFrame(
                    tbl, fg_color=bg, corner_radius=8
                )
                row.pack(fill="x", padx=10, pady=2)

                ac = GOLD if "Late" in rec.get('arrival', '') else C_GREEN
                vals = [
                    (rec.get('student_id',   ''), C_WHITE),
                    (rec.get('student_name', ''), C_WHITE),
                    (rec.get('course_name',  ''), C_GRAY),
                    (rec.get('time',         ''), C_WHITE),
                    (rec.get('arrival',      ''), ac),
                ]
                for (v, c), w in zip(vals, widths):
                    ctk.CTkLabel(
                        row, text=str(v)[:20],
                        font=ctk.CTkFont(size=11),
                        text_color=c,
                        width=w, anchor="w"
                    ).pack(side="left", padx=10, pady=8)
        else:
            ctk.CTkLabel(
                tbl,
                text="No attendance marked today",
                font=ctk.CTkFont(size=13),
                text_color=C_GRAY
            ).pack(pady=20)

        ctk.CTkFrame(scroll, fg_color=C_BG1,
                     height=20).pack()

    def _run_counters(self):
        for ctr, val in self.counters:
            ctr.count_to(val)

    def _tick(self):
        try:
            self.clock_lbl.configure(
                text=f"📅 {datetime.now().strftime('%A, %b %d  |  %H:%M:%S')}"
            )
            self.after(1000, self._tick)
        except:
            pass

    def open_register(self):
        self._set_active(1)
        self._clear()
        from register import RegisterFrame
        RegisterFrame(self.main, self.user).pack(fill="both", expand=True)

    def open_attendance(self):
        self._set_active(2)
        self._clear()
        from attendance import AttendanceFrame
        AttendanceFrame(self.main, self.user).pack(fill="both", expand=True)

    def open_reports(self):
        self._set_active(3)
        self._clear()
        from reports import ReportsFrame
        ReportsFrame(self.main, self.user).pack(fill="both", expand=True)

    def open_settings(self):
        self._set_active(4)
        self._clear()
        from settings import SettingsFrame
        SettingsFrame(self.main, self.user).pack(fill="both", expand=True)

    def _email(self):
        try:
            from email_report import send_report
            send_report()
            messagebox.showinfo("Success", "✅ Email sent!")
        except Exception as e:
            messagebox.showerror("Error", f"❌ {e}")

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.destroy()
            from login import LoginApp
            LoginApp().mainloop()

# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────
if __name__ == '__main__':
    db.initialize_database()
    HomeApp({
        'id': 1, 'username': 'admin',
        'role': 'admin',
        'full_name': 'System Administrator',
        'email': 'admin@nsbm.ac.lk'
    }).mainloop()