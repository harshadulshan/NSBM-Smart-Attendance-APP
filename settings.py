import customtkinter as ctk
from tkinter import messagebox
import database as db
from datetime import datetime

# ─────────────────────────────────────────
# THEME
# ─────────────────────────────────────────
NSBM_GREEN  = "#60b94b"
NSBM_DARK   = "#050d1a"
NSBM_CARD   = "#0d1f35"
NSBM_ACCENT = "#cfff5a"
NSBM_GOLD   = "#F59E0B"
WHITE       = "#FFFFFF"
GRAY        = "#AAAAAA"
RED         = "#EF4444"
PURPLE      = "#A855F7"

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color=NSBM_DARK, corner_radius=0)
        self.user = user
        self.build_ui()

    def build_ui(self):

        # ── HEADER ───────────────────────
        header = ctk.CTkFrame(
            self, fg_color=NSBM_CARD,
            corner_radius=0, height=70
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=WHITE
        ).pack(side="left", padx=25, pady=20)

        # ── MAIN CONTENT ─────────────────
        scroll = ctk.CTkScrollableFrame(
            self, fg_color=NSBM_DARK
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=20)

        # ── USER MANAGEMENT ──────────────
        self.build_section(
            scroll,
            "👥 User Management",
            self.build_user_section
        )

        # ── TIMETABLE ────────────────────
        self.build_section(
            scroll,
            "📅 Timetable Management",
            self.build_timetable_section
        )

        # ── SYSTEM SETTINGS ──────────────
        self.build_section(
            scroll,
            "🔧 System Settings",
            self.build_system_section
        )

        # ── DATABASE ─────────────────────
        self.build_section(
            scroll,
            "🗄️ Database",
            self.build_database_section
        )

    def build_section(self, parent, title, builder):
        """Build a settings section."""
        section = ctk.CTkFrame(
            parent,
            fg_color=NSBM_CARD,
            corner_radius=15
        )
        section.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(
            section,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(15, 10))

        ctk.CTkFrame(
            section, height=1, fg_color="#1e4a7a"
        ).pack(fill="x", padx=20, pady=(0, 15))

        builder(section)

    def build_user_section(self, parent):
        """Build user management section."""

        # Add new user
        ctk.CTkLabel(
            parent,
            text="Add New User",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=20, pady=(0, 10))

        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", padx=20, pady=(0, 15))

        # Row 1
        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))

        self.new_username = ctk.CTkEntry(
            row1,
            placeholder_text="Username",
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.new_username.pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )

        self.new_password = ctk.CTkEntry(
            row1,
            placeholder_text="Password",
            show="*",
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.new_password.pack(
            side="left", fill="x", expand=True
        )

        # Row 2
        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))

        self.new_fullname = ctk.CTkEntry(
            row2,
            placeholder_text="Full Name",
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.new_fullname.pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )

        self.new_email = ctk.CTkEntry(
            row2,
            placeholder_text="Email",
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.new_email.pack(
            side="left", fill="x", expand=True
        )

        # Row 3
        row3 = ctk.CTkFrame(form, fg_color="transparent")
        row3.pack(fill="x")

        self.new_role = ctk.StringVar(value="lecturer")
        ctk.CTkOptionMenu(
            row3,
            values=["admin", "lecturer", "student"],
            variable=self.new_role,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8,
            width=150
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            row3,
            text="➕ Add User",
            height=38,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NSBM_GREEN,
            hover_color="#1B5E20",
            corner_radius=8,
            command=self.add_user
        ).pack(side="left")

        self.user_status = ctk.CTkLabel(
            row3,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#22C55E"
        )
        self.user_status.pack(side="left", padx=10)

        # Users list
        ctk.CTkLabel(
            parent,
            text="Current Users",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=20, pady=(5, 8))

        self.users_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        self.users_frame.pack(fill="x", padx=20, pady=(0, 15))
        self.load_users()

    def add_user(self):
        """Add new user."""
        username  = self.new_username.get().strip()
        password  = self.new_password.get().strip()
        full_name = self.new_fullname.get().strip()
        email     = self.new_email.get().strip()
        role      = self.new_role.get()

        if not username or not password or not full_name:
            self.user_status.configure(
                text="⚠️ Fill all required fields!",
                text_color=RED
            )
            return

        success = db.add_user(
            username, password, role, full_name, email
        )

        if success:
            self.user_status.configure(
                text=f"✅ {full_name} added!",
                text_color="#22C55E"
            )
            self.new_username.delete(0, "end")
            self.new_password.delete(0, "end")
            self.new_fullname.delete(0, "end")
            self.new_email.delete(0, "end")
            self.load_users()
        else:
            self.user_status.configure(
                text="⚠️ Username already exists!",
                text_color=RED
            )

    def load_users(self):
        """Load users list."""
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        users = db.get_all_users()
        for user in users:
            row = ctk.CTkFrame(
                self.users_frame,
                fg_color="#050d1a",
                corner_radius=8
            )
            row.pack(fill="x", pady=3)

            role_color = {
                'admin'    : NSBM_ACCENT,
                'lecturer' : NSBM_GOLD,
                'student'  : "#22C55E"
            }.get(user['role'], WHITE)

            ctk.CTkLabel(
                row,
                text=f"👤 {user['username']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=WHITE
            ).pack(side="left", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=user['full_name'],
                font=ctk.CTkFont(size=12),
                text_color=GRAY
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text=f"🔑 {user['role'].capitalize()}",
                font=ctk.CTkFont(size=11),
                text_color=role_color
            ).pack(side="right", padx=12)

    def build_timetable_section(self, parent):
        """Build timetable management."""

        form = ctk.CTkFrame(parent, fg_color="transparent")
        form.pack(fill="x", padx=20, pady=(0, 15))

        # Row 1
        row1 = ctk.CTkFrame(form, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))

        # Course
        courses         = db.get_all_courses()
        self.tt_course_map = {c['name']: c['id'] for c in courses}
        course_names    = list(self.tt_course_map.keys())

        self.tt_course = ctk.StringVar(
            value=course_names[0] if course_names else ""
        )
        ctk.CTkOptionMenu(
            row1,
            values=course_names,
            variable=self.tt_course,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8,
            command=self.update_tt_batches
        ).pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Batch
        self.tt_batch_map = {}
        self.tt_batch     = ctk.StringVar()
        self.tt_batch_dd  = ctk.CTkOptionMenu(
            row1,
            values=[],
            variable=self.tt_batch,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8
        )
        self.tt_batch_dd.pack(
            side="left", fill="x", expand=True
        )
        self.update_tt_batches(
            course_names[0] if course_names else ""
        )

        # Row 2
        row2 = ctk.CTkFrame(form, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 8))

        self.tt_subject = ctk.CTkEntry(
            row2,
            placeholder_text="Subject Name",
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.tt_subject.pack(
            side="left", fill="x", expand=True, padx=(0, 8)
        )

        self.tt_day = ctk.StringVar(value="Monday")
        ctk.CTkOptionMenu(
            row2,
            values=["Monday", "Tuesday", "Wednesday",
                   "Thursday", "Friday", "Saturday"],
            variable=self.tt_day,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8,
            width=130
        ).pack(side="left", padx=(0, 8))

        # Row 3
        row3 = ctk.CTkFrame(form, fg_color="transparent")
        row3.pack(fill="x", pady=(0, 8))

        self.tt_start = ctk.CTkEntry(
            row3,
            placeholder_text="Start (08:00)",
            height=38,
            width=120,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.tt_start.pack(side="left", padx=(0, 8))

        self.tt_end = ctk.CTkEntry(
            row3,
            placeholder_text="End (10:00)",
            height=38,
            width=120,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1,
            corner_radius=8
        )
        self.tt_end.pack(side="left", padx=(0, 8))

        # Lecturer
        users           = db.get_all_users()
        lecturers       = [u for u in users
                          if u['role'] in ['lecturer', 'admin']]
        self.lect_map   = {u['full_name']: u['id'] for u in lecturers}
        lect_names      = list(self.lect_map.keys())

        self.tt_lecturer = ctk.StringVar(
            value=lect_names[0] if lect_names else ""
        )
        ctk.CTkOptionMenu(
            row3,
            values=lect_names,
            variable=self.tt_lecturer,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            row3,
            text="➕ Add",
            height=38,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NSBM_GREEN,
            hover_color="#1B5E20",
            corner_radius=8,
            command=self.add_timetable
        ).pack(side="left")

        self.tt_status = ctk.CTkLabel(
            form,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#22C55E"
        )
        self.tt_status.pack(anchor="w", pady=5)

        # Timetable list
        self.tt_list_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        self.tt_list_frame.pack(
            fill="x", padx=20, pady=(0, 15)
        )
        self.load_timetable()

    def update_tt_batches(self, course_name):
        """Update timetable batch dropdown."""
        course_id = self.tt_course_map.get(course_name)
        if course_id:
            batches          = db.get_batches_by_course(course_id)
            self.tt_batch_map = {b['name']: b['id'] for b in batches}
            batch_names      = list(self.tt_batch_map.keys())
            self.tt_batch_dd.configure(values=batch_names)
            if batch_names:
                self.tt_batch.set(batch_names[0])

    def add_timetable(self):
        """Add timetable entry."""
        course_id   = self.tt_course_map.get(self.tt_course.get())
        batch_id    = self.tt_batch_map.get(self.tt_batch.get())
        subject     = self.tt_subject.get().strip()
        day         = self.tt_day.get()
        start_time  = self.tt_start.get().strip()
        end_time    = self.tt_end.get().strip()
        lecturer_id = self.lect_map.get(self.tt_lecturer.get())

        if not subject or not start_time or not end_time:
            self.tt_status.configure(
                text="⚠️ Fill all fields!",
                text_color=RED
            )
            return

        db.add_timetable(
            course_id, batch_id, subject,
            day, start_time, end_time, lecturer_id
        )

        self.tt_status.configure(
            text=f"✅ {subject} added to timetable!",
            text_color="#22C55E"
        )
        self.tt_subject.delete(0, "end")
        self.tt_start.delete(0, "end")
        self.tt_end.delete(0, "end")
        self.load_timetable()

    def load_timetable(self):
        """Load timetable list."""
        for widget in self.tt_list_frame.winfo_children():
            widget.destroy()

        entries = db.get_timetable()
        if not entries:
            ctk.CTkLabel(
                self.tt_list_frame,
                text="No timetable entries yet",
                font=ctk.CTkFont(size=12),
                text_color=GRAY
            ).pack(pady=10)
            return

        for entry in entries:
            row = ctk.CTkFrame(
                self.tt_list_frame,
                fg_color="#050d1a",
                corner_radius=8
            )
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row,
                text=f"📚 {entry['subject']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=NSBM_ACCENT
            ).pack(side="left", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=f"{entry['day_of_week']} "
                     f"{entry['start_time']}-{entry['end_time']}",
                font=ctk.CTkFont(size=11),
                text_color=GRAY
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text=f"👨‍🏫 {entry.get('lecturer_name', '')}",
                font=ctk.CTkFont(size=11),
                text_color=NSBM_GOLD
            ).pack(side="right", padx=12)

    def build_system_section(self, parent):
        """Build system settings."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 15))

        # Late arrival time
        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(
            row,
            text="⏰ Late Arrival Time:",
            font=ctk.CTkFont(size=13),
            text_color=WHITE
        ).pack(side="left")

        self.late_hour = ctk.CTkEntry(
            row,
            placeholder_text="Hour (9)",
            width=80,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1
        )
        self.late_hour.pack(side="left", padx=(15, 5))
        self.late_hour.insert(0, "9")

        ctk.CTkLabel(
            row,
            text=":",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=WHITE
        ).pack(side="left")

        self.late_min = ctk.CTkEntry(
            row,
            placeholder_text="Min (00)",
            width=80,
            height=35,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            border_color=NSBM_ACCENT,
            border_width=1
        )
        self.late_min.pack(side="left", padx=(5, 15))
        self.late_min.insert(0, "00")

        ctk.CTkButton(
            row,
            text="💾 Save",
            height=35,
            width=80,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NSBM_GREEN,
            corner_radius=8,
            command=self.save_late_time
        ).pack(side="left")

        self.late_status = ctk.CTkLabel(
            frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#22C55E"
        )
        self.late_status.pack(anchor="w", pady=5)

    def save_late_time(self):
        """Save late arrival time."""
        self.late_status.configure(
            text=f"✅ Late time set to "
                 f"{self.late_hour.get()}:{self.late_min.get()}",
            text_color="#22C55E"
        )

    def build_database_section(self, parent):
        """Build database management."""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=20, pady=(0, 15))

        # Stats
        students   = db.get_all_students()
        attendance = db.get_attendance_by_date_range(
            "2020-01-01",
            datetime.now().strftime('%Y-%m-%d')
        )

        stats = [
            (f"👥 {len(students)} Students registered"),
            (f"📋 {len(attendance)} Attendance records"),
        ]

        for stat in stats:
            ctk.CTkLabel(
                frame,
                text=stat,
                font=ctk.CTkFont(size=13),
                text_color=WHITE
            ).pack(anchor="w", pady=3)

        ctk.CTkFrame(
            frame, height=1, fg_color="#1e4a7a"
        ).pack(fill="x", pady=15)

        ctk.CTkButton(
            frame,
            text="🔄 Reinitialize Database",
            height=38,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#1E3A5F",
            hover_color="#050d1a",
            corner_radius=8,
            command=self.reinit_db
        ).pack(anchor="w")

    def reinit_db(self):
        """Reinitialize database."""
        if messagebox.askyesno(
            "Confirm",
            "This will reset all data!\nAre you sure?"
        ):
            db.initialize_database()
            messagebox.showinfo(
                "Success",
                "✅ Database reinitialized!"
            )