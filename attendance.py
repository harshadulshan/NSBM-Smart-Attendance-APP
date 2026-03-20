import customtkinter as ctk
from tkinter import messagebox
import database as db
import cv2
import numpy as np
import json
import os
from datetime import datetime
from PIL import Image

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

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────
LATE_HOUR       = 9
LATE_MINUTE     = 0
CONFIDENCE_THRESHOLD = 70

class AttendanceFrame(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color=NSBM_DARK, corner_radius=0)
        self.user       = user
        self.cap        = None
        self.running    = False
        self.recognizer = None
        self.label_map  = {}
        self.marked_today = set()
        self.current_session = "Morning Session"
        self.selected_course = None
        self.selected_batch  = None

        # Load model if exists
        self.load_model()

        # Build UI
        self.build_ui()

        # Load already marked today
        self.load_marked_today()

    def load_model(self):
        """Load face recognition model."""
        if os.path.exists('face_model.yml') and \
           os.path.exists('label_map.json'):
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read('face_model.yml')
            with open('label_map.json', 'r') as f:
                self.label_map = json.load(f)
            print("✅ Model loaded successfully!")
        else:
            print("⚠️ No model found!")

    def load_marked_today(self):
        """Load already marked students."""
        records = db.get_attendance_today()
        for r in records:
            key = f"{r['student_id']}_{r.get('session','')}"
            self.marked_today.add(key)

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
            text="🎯 Mark Attendance",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=WHITE
        ).pack(side="left", padx=25, pady=20)

        # Live clock
        self.clock_label = ctk.CTkLabel(
            header,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=GRAY
        )
        self.clock_label.pack(side="right", padx=25)
        self.update_clock()

        # ── MAIN CONTENT ─────────────────
        content = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # ── LEFT PANEL ───────────────────
        left = ctk.CTkFrame(
            content,
            fg_color=NSBM_CARD,
            corner_radius=15,
            width=300
        )
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left,
            text="⚙️ Session Setup",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(20, 15))

        # Course selection
        ctk.CTkLabel(
            left,
            text="Course",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NSBM_ACCENT,
            anchor="w"
        ).pack(fill="x", padx=20)

        courses         = db.get_all_courses()
        self.course_map = {c['name']: c['id'] for c in courses}
        course_names    = list(self.course_map.keys())

        self.course_var = ctk.StringVar(
            value=course_names[0] if course_names else ""
        )
        ctk.CTkOptionMenu(
            left,
            values=course_names,
            variable=self.course_var,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8,
            command=self.update_batches
        ).pack(fill="x", padx=20, pady=(5, 12))

        # Batch selection
        ctk.CTkLabel(
            left,
            text="Batch",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NSBM_ACCENT,
            anchor="w"
        ).pack(fill="x", padx=20)

        self.batch_var = ctk.StringVar()
        self.batch_dropdown = ctk.CTkOptionMenu(
            left,
            values=[],
            variable=self.batch_var,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8
        )
        self.batch_dropdown.pack(fill="x", padx=20, pady=(5, 12))
        self.update_batches(course_names[0] if course_names else "")

        # Session selection
        ctk.CTkLabel(
            left,
            text="Session",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NSBM_ACCENT,
            anchor="w"
        ).pack(fill="x", padx=20)

        self.session_var = ctk.StringVar(value="Morning Session")
        ctk.CTkOptionMenu(
            left,
            values=[
                "Morning Session",
                "Afternoon Session",
                "Evening Session",
                "Lab Session",
                "Tutorial Session"
            ],
            variable=self.session_var,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8
        ).pack(fill="x", padx=20, pady=(5, 12))

        # Current session info
        self.session_info = ctk.CTkLabel(
            left,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=NSBM_GOLD,
            wraplength=250
        )
        self.session_info.pack(padx=20, pady=5)
        self.check_timetable()

        # Divider
        ctk.CTkFrame(
            left, height=1, fg_color="#1e4a7a"
        ).pack(fill="x", padx=20, pady=15)

        # Camera controls
        ctk.CTkLabel(
            left,
            text="🎥 Camera Controls",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(0, 10))

        self.start_btn = ctk.CTkButton(
            left,
            text="▶️  Start Camera",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=NSBM_GREEN,
            hover_color="#1B5E20",
            corner_radius=10,
            command=self.start_camera
        )
        self.start_btn.pack(fill="x", padx=20, pady=(0, 8))

        self.stop_btn = ctk.CTkButton(
            left,
            text="⏹  Stop Camera",
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=RED,
            hover_color="#7F0000",
            corner_radius=10,
            command=self.stop_camera,
            state="disabled"
        )
        self.stop_btn.pack(fill="x", padx=20, pady=(0, 8))

        # Divider
        ctk.CTkFrame(
            left, height=1, fg_color="#1e4a7a"
        ).pack(fill="x", padx=20, pady=15)

        # Stats
        ctk.CTkLabel(
            left,
            text="📊 Session Stats",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(0, 10))

        self.stats_frame = ctk.CTkFrame(
            left, fg_color="transparent"
        )
        self.stats_frame.pack(fill="x", padx=20)
        self.update_stats()

        # ── RIGHT PANEL ──────────────────
        right = ctk.CTkFrame(
            content, fg_color="transparent"
        )
        right.pack(side="right", fill="both", expand=True)

        # Camera preview
        self.camera_frame = ctk.CTkFrame(
            right,
            fg_color=NSBM_CARD,
            corner_radius=15,
            width=640,
            height=440
        )
        self.camera_frame.pack(fill="both", expand=True, pady=(0, 10))

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="🎥\n\nCamera not started\n\nSelect course & batch\nthen click Start Camera",
            font=ctk.CTkFont(size=15),
            text_color=GRAY
        )
        self.camera_label.pack(expand=True)

        # Status bar
        self.status_bar = ctk.CTkFrame(
            right,
            fg_color=NSBM_CARD,
            corner_radius=10,
            height=50
        )
        self.status_bar.pack(fill="x")
        self.status_bar.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready — Start camera to begin marking attendance",
            font=ctk.CTkFont(size=13),
            text_color=GRAY
        )
        self.status_label.pack(expand=True)

    def update_clock(self):
        """Update live clock."""
        now = datetime.now().strftime('%A, %B %d %Y  |  %H:%M:%S')
        self.clock_label.configure(text=f"📅 {now}")
        self.after(1000, self.update_clock)

    def update_batches(self, course_name):
        """Update batch dropdown."""
        course_id      = self.course_map.get(course_name)
        self.selected_course = course_id
        if course_id:
            batches        = db.get_batches_by_course(course_id)
            self.batch_map = {b['name']: b['id'] for b in batches}
            batch_names    = list(self.batch_map.keys())
            self.batch_dropdown.configure(values=batch_names)
            if batch_names:
                self.batch_var.set(batch_names[0])
                self.selected_batch = self.batch_map[batch_names[0]]

    def check_timetable(self):
        """Check current timetable session."""
        if self.selected_course and self.selected_batch:
            session = db.get_current_session(
                self.selected_course,
                self.selected_batch
            )
            if session:
                self.session_info.configure(
                    text=f"📚 Current: {session['subject']}\n"
                         f"👨‍🏫 {session['lecturer_name']}\n"
                         f"⏰ {session['start_time']} - {session['end_time']}"
                )
            else:
                self.session_info.configure(
                    text="No scheduled class right now"
                )

    def is_late(self):
        """Check if current time is late."""
        now = datetime.now()
        return (now.hour > LATE_HOUR or
               (now.hour == LATE_HOUR and
                now.minute >= LATE_MINUTE))

    def update_stats(self):
        """Update session statistics."""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        records  = db.get_attendance_today()
        present  = len(records)
        late     = len([r for r in records
                       if 'Late' in r.get('arrival', '')])
        on_time  = present - late

        stats = [
            ("✅ Present", str(present), "#22C55E"),
            ("🔴 Late",    str(late),    NSBM_GOLD),
            ("🟢 On Time", str(on_time), NSBM_ACCENT),
        ]

        for label, value, color in stats:
            row = ctk.CTkFrame(
                self.stats_frame,
                fg_color="#050d1a",
                corner_radius=8
            )
            row.pack(fill="x", pady=3)

            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=12),
                text_color=GRAY
            ).pack(side="left", padx=12, pady=8)

            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=color
            ).pack(side="right", padx=12)

    def start_camera(self):
        """Start camera for attendance."""
        if not self.recognizer:
            messagebox.showerror(
                "Error",
                "❌ No trained model found!\n"
                "Please register students first!"
            )
            return

        self.running = True
        self.cap     = cv2.VideoCapture(0)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        self.current_session = self.session_var.get()
        self.selected_batch  = self.batch_map.get(
            self.batch_var.get()
        )

        self.update_camera()

    def update_camera(self):
        """Update camera feed."""
        if not self.running:
            return

        success, frame = self.cap.read()
        if not success:
            self.after(30, self.update_camera)
            return

        frame        = cv2.flip(frame, 1)
        gray         = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            'haarcascade_frontalface_default.xml'
        )
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )

        for (x, y, w, h) in faces:
            face_roi             = gray[y:y+h, x:x+w]
            label_id, confidence = self.recognizer.predict(face_roi)
            confidence_pct       = round(100 - confidence, 2)

            if confidence < CONFIDENCE_THRESHOLD:
                # Known student
                student_id = self.label_map.get(str(label_id), "")
                student    = db.get_student_by_id(student_id)

                if student:
                    name     = student['full_name']
                    color    = (0, 255, 0)
                    dup_key  = f"{student_id}_{self.current_session}"

                    if dup_key not in self.marked_today:
                        # Mark attendance
                        arrival = "Late 🔴" if self.is_late() else "On Time 🟢"
                        success, msg = db.mark_attendance(
                            student_id,
                            name,
                            self.selected_course,
                            self.selected_batch,
                            arrival,
                            self.user['username'],
                            self.current_session
                        )

                        if success:
                            self.marked_today.add(dup_key)
                            self.status_label.configure(
                                text=f"✅ {name} marked — {arrival}",
                                text_color="#22C55E"
                            )
                            self.update_stats()
                        color = (0, 255, 0)
                    else:
                        color = (0, 165, 255)
                        self.status_label.configure(
                            text=f"⚠️ {name} — Already marked this session!",
                            text_color=NSBM_GOLD
                        )
                else:
                    name  = student_id
                    color = (0, 255, 0)
            else:
                # Unknown
                name  = "Unknown"
                color = (0, 0, 255)
                self.status_label.configure(
                    text="❌ Unknown face detected!",
                    text_color=RED
                )

            # Draw box
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y-65), (x+w, y), color, -1)
            cv2.putText(
                frame, name,
                (x+5, y-40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255, 255, 255), 2
            )
            cv2.putText(
                frame, f"Conf: {confidence_pct}%",
                (x+5, y-15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 1
            )

        # Info overlay
        cv2.rectangle(frame, (0, 0), (350, 60), (22, 33, 62), -1)
        cv2.putText(
            frame,
            f"Session: {self.current_session}",
            (10, 22),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 217, 255), 2
        )
        cv2.putText(
            frame,
            f"Marked: {len(self.marked_today)} | "
            f"{datetime.now().strftime('%H:%M:%S')}",
            (10, 48),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55, (255, 255, 255), 1
        )

        # Display in UI
        try:
            frame_rgb = cv2.cvtColor(
                cv2.resize(frame, (620, 420)),
                cv2.COLOR_BGR2RGB
            )
            pil_img = Image.fromarray(frame_rgb)
            ctk_img = ctk.CTkImage(
                light_image=pil_img,
                dark_image=pil_img,
                size=(620, 420)
            )
            self.camera_label.configure(
                image=ctk_img,
                text=""
            )
            self.camera_label._image = ctk_img
        except Exception as e:
            print(f"Display error: {e}")

        if self.running:
            self.after(30, self.update_camera)

    def stop_camera(self):
        """Stop camera."""
        self.running = False
        if self.cap:
            self.cap.release()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.camera_label.configure(
            image=None,
            text="🎥\n\nCamera stopped\n\nClick Start Camera to resume"
        )
        self.status_label.configure(
            text="Camera stopped",
            text_color=GRAY
        )

    def destroy(self):
        """Clean up on destroy."""
        self.stop_camera()
        super().destroy()