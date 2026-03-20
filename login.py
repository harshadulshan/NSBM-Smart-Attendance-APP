import customtkinter as ctk
import database as db
import math
import random
from tkinter import Canvas

# ─────────────────────────────────────────
# NSBM COLOR PALETTE
# ─────────────────────────────────────────
C_BG        = "#050d1a"
C_NAVY      = "#235895"
C_GREEN     = "#60b94b"
C_LIME      = "#cfff5a"
C_WHITE     = "#ffffff"
C_CARD      = "#0d1f35"
C_CARD2     = "#102540"
C_BORDER    = "#1e4a7a"
C_GRAY      = "#aabbcc"
RED         = "#ef4444"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ─────────────────────────────────────────
# ANIMATED PARTICLE BACKGROUND
# ─────────────────────────────────────────
class ParticleBG(Canvas):
    def __init__(self, parent, w, h):
        super().__init__(
            parent, width=w, height=h,
            highlightthickness=0, bg=C_BG
        )
        self.W = w
        self.H = h
        self.particles = [
            {
                'x'    : random.randint(0, w),
                'y'    : random.randint(0, h),
                'r'    : random.uniform(1, 2.5),
                'dx'   : random.uniform(-0.3, 0.3),
                'dy'   : random.uniform(-0.3, 0.3),
                'color': random.choice([
                    C_GREEN, C_NAVY,
                    C_LIME, "#ffffff"
                ])
            }
            for _ in range(40)
        ]
        self._animate()

    def _animate(self):
        self.delete("p")
        for p in self.particles:
            self.create_oval(
                p['x']-p['r'], p['y']-p['r'],
                p['x']+p['r'], p['y']+p['r'],
                fill=p['color'], outline="", tags="p"
            )
            p['x'] += p['dx']
            p['y'] += p['dy']
            if p['x'] < 0 or p['x'] > self.W:
                p['dx'] *= -1
            if p['y'] < 0 or p['y'] > self.H:
                p['dy'] *= -1
        self.after(40, self._animate)

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
        self.configure(
            border_color=C_BORDER,
            border_width=1
        )

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
# LOGIN APP
# ─────────────────────────────────────────
class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        db.initialize_database()

        self.title("NSBM Smart Attendance System")
        self.geometry("900x600")
        self.resizable(False, False)
        self.configure(fg_color=C_BG)
        self._center(900, 600)
        self._build()
        self._animate_entrance()

    def _center(self, w, h):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def _build(self):

        # ── ANIMATED BACKGROUND ───────────
        self.bg = ParticleBG(self, 900, 600)
        self.bg.place(x=0, y=0)

        # ── LEFT PANEL ───────────────────
        left = ctk.CTkFrame(
            self,
            width=420,
            height=600,
            fg_color=C_CARD,
            corner_radius=0
        )
        left.place(x=0, y=0)
        left.pack_propagate(False)

        # Top green bar
        ctk.CTkFrame(
            left,
            height=4,
            fg_color=C_GREEN,
            corner_radius=0
        ).pack(fill="x")

        # Logo area
        logo_frame = ctk.CTkFrame(
            left,
            fg_color=C_CARD2,
            corner_radius=0,
            height=200
        )
        logo_frame.pack(fill="x")
        logo_frame.pack_propagate(False)

        ctk.CTkLabel(
            logo_frame,
            text="🎓",
            font=ctk.CTkFont(size=70)
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            logo_frame,
            text="NSBM",
            font=ctk.CTkFont(size=38, weight="bold"),
            text_color=C_LIME
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="GREEN UNIVERSITY",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=C_GREEN
        ).pack(pady=(2, 0))

        ctk.CTkFrame(
            logo_frame,
            height=2,
            width=180,
            fg_color=C_GREEN,
            corner_radius=2
        ).pack(pady=8)

        ctk.CTkLabel(
            logo_frame,
            text="Smart Attendance System",
            font=ctk.CTkFont(size=13),
            text_color=C_GRAY
        ).pack()

        # Feature badges
        badges = ctk.CTkFrame(left, fg_color="transparent")
        badges.pack(fill="x", padx=30, pady=20)

        for icon, text in [
            ("🤖", "AI Face Recognition"),
            ("📊", "Live Analytics Dashboard"),
            ("🔒", "Secure Multi-Role Access"),
        ]:
            row = ctk.CTkFrame(
                badges,
                fg_color=C_CARD2,
                corner_radius=20,
                border_color=C_BORDER,
                border_width=1
            )
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(
                row,
                text=f"{icon}   {text}",
                font=ctk.CTkFont(size=12),
                text_color=C_GRAY
            ).pack(padx=20, pady=8)

        # Footer
        ctk.CTkLabel(
            left,
            text="© 2026 NSBM Green University",
            font=ctk.CTkFont(size=10),
            text_color=C_GRAY
        ).pack(side="bottom", pady=12)

        # ── RIGHT PANEL — LOGIN CARD ──────
        self.card = ctk.CTkFrame(
            self,
            width=380,
            height=460,
            fg_color=C_CARD2,
            corner_radius=24,
            border_color=C_BORDER,
            border_width=1
        )
        self.card.place(x=510, y=70)
        self.card.pack_propagate(False)

        # Top lime bar
        ctk.CTkFrame(
            self.card,
            height=3,
            fg_color=C_LIME,
            corner_radius=0
        ).pack(fill="x")

        # Title
        ctk.CTkLabel(
            self.card,
            text="Welcome Back 👋",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=C_WHITE
        ).pack(pady=(25, 3))

        ctk.CTkLabel(
            self.card,
            text="Sign in to your account",
            font=ctk.CTkFont(size=12),
            text_color=C_GRAY
        ).pack(pady=(0, 20))

        # Divider
        ctk.CTkFrame(
            self.card,
            height=1,
            fg_color=C_BORDER
        ).pack(fill="x", padx=30, pady=(0, 15))

        # Username
        ctk.CTkLabel(
            self.card,
            text="USERNAME",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=C_GREEN,
            anchor="w"
        ).pack(fill="x", padx=30)

        self.username = ctk.CTkEntry(
            self.card,
            placeholder_text="Enter your username",
            height=45,
            font=ctk.CTkFont(size=13),
            fg_color=C_CARD,
            border_color=C_NAVY,
            border_width=1,
            corner_radius=10,
            text_color=C_WHITE,
            placeholder_text_color=C_GRAY
        )
        self.username.pack(fill="x", padx=30, pady=(5, 12))
        self.username.bind(
            "<FocusIn>",
            lambda e: self.username.configure(border_color=C_LIME)
        )
        self.username.bind(
            "<FocusOut>",
            lambda e: self.username.configure(border_color=C_NAVY)
        )

        # Password
        ctk.CTkLabel(
            self.card,
            text="PASSWORD",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=C_GREEN,
            anchor="w"
        ).pack(fill="x", padx=30)

        self.password = ctk.CTkEntry(
            self.card,
            placeholder_text="Enter your password",
            show="*",
            height=45,
            font=ctk.CTkFont(size=13),
            fg_color=C_CARD,
            border_color=C_NAVY,
            border_width=1,
            corner_radius=10,
            text_color=C_WHITE,
            placeholder_text_color=C_GRAY
        )
        self.password.pack(fill="x", padx=30, pady=(5, 8))
        self.password.bind(
            "<FocusIn>",
            lambda e: self.password.configure(border_color=C_LIME)
        )
        self.password.bind(
            "<FocusOut>",
            lambda e: self.password.configure(border_color=C_NAVY)
        )

        # Show password
        self.show_pwd = ctk.CTkCheckBox(
            self.card,
            text="Show password",
            font=ctk.CTkFont(size=11),
            text_color=C_GRAY,
            fg_color=C_GREEN,
            hover_color=C_LIME,
            corner_radius=4,
            command=self._toggle_pwd
        )
        self.show_pwd.pack(anchor="w", padx=30, pady=(0, 15))

        # Login button
        self.login_btn = GlowButton(
            self.card,
            text="🔐   SIGN IN",
            height=48,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=C_GREEN,
            hover_color="#4a9a3a",
            text_color=C_BG,
            corner_radius=12,
            border_color=C_BORDER,
            border_width=1,
            glow_color=C_LIME,
            command=self._login
        )
        self.login_btn.pack(fill="x", padx=30, pady=(0, 10))

        # Status
        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=C_GRAY
        )
        self.status.pack()

        # Bind enter key
        self.bind("<Return>", lambda e: self._login())
        self.username.focus()

    def _toggle_pwd(self):
        """Toggle password visibility."""
        self.password.configure(
            show="" if self.show_pwd.get() else "*"
        )

    def _animate_entrance(self):
        """Slide card in from right."""
        self._step = 0
        self._slide()

    def _slide(self):
        self._step += 1
        progress  = min(self._step / 25, 1.0)
        ease      = 1 - (1 - progress) ** 3
        start_x   = 900
        end_x     = 510
        current_x = int(start_x + (end_x - start_x) * ease)
        self.card.place(x=current_x, y=70)
        if progress < 1.0:
            self.after(16, self._slide)

    def _login(self):
        """Handle login click."""
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            self.status.configure(
                text="⚠️ Please fill in all fields!",
                text_color="#F59E0B"
            )
            self._shake()
            return

        # Show loading
        self.login_btn.configure(
            text="⏳   Authenticating...",
            state="disabled",
            fg_color=C_NAVY
        )
        self.status.configure(
            text="Verifying credentials...",
            text_color=C_GRAY
        )
        self.update()
        self.after(300, lambda: self._verify(username, password))

    def _verify(self, username, password):
        """Verify credentials."""
        try:
            user = db.verify_user(username, password)
            if user:
                self.login_btn.configure(
                    text="✅   Welcome!",
                    fg_color=C_GREEN,
                    state="normal"
                )
                self.status.configure(
                    text=f"Welcome, {user['full_name']}!",
                    text_color=C_LIME
                )
                self.update()
                self.after(400, lambda: self._go_home(user))
            else:
                self.login_btn.configure(
                    text="🔐   SIGN IN",
                    state="normal",
                    fg_color=C_GREEN
                )
                self.status.configure(
                    text="❌ Invalid username or password!",
                    text_color=RED
                )
                self.password.delete(0, "end")
                self.password.focus()
                self._shake()
        except Exception as e:
            print(f"Login error: {e}")
            self.login_btn.configure(
                text="🔐   SIGN IN",
                state="normal",
                fg_color=C_GREEN
            )
            self.status.configure(
                text=f"❌ Error: {str(e)}",
                text_color=RED
            )

    def _go_home(self, user):
        """Navigate to home."""
        try:
            self.destroy()
            from home import HomeApp
            HomeApp(user).mainloop()
        except Exception as e:
            print(f"Home error: {e}")

    def _shake(self):
        """Shake card on error."""
        offsets = [10, -10, 8, -8, 5, -5, 2, -2, 0]
        self._do_shake(offsets, 0)

    def _do_shake(self, offsets, idx):
        if idx >= len(offsets):
            self.card.place(x=510, y=70)
            return
        self.card.place(x=510 + offsets[idx], y=70)
        self.after(35, lambda: self._do_shake(offsets, idx+1))

# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────
if __name__ == '__main__':
    LoginApp().mainloop()