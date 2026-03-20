import customtkinter as ctk
from tkinter import messagebox
import database as db
import cv2
import os
import numpy as np
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

class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent, user):
        super().__init__(parent, fg_color="#050d1a", corner_radius=0)
        self.user            = user
        self.cap             = None
        self.capturing       = False
        self.count           = 0
        self.total           = 50
        self.current_student = None
        self.face_cascade    = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.build_ui()

    def build_ui(self):

        # ── HEADER ───────────────────────
        header = ctk.CTkFrame(
            self, fg_color="#0d1f35",
            corner_radius=0, height=70
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="📸 Student Registration",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=WHITE
        ).pack(side="left", padx=25, pady=20)

        # ── MAIN CONTENT ─────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Left — Form
        left = ctk.CTkScrollableFrame(
            content,
            fg_color="#0d1f35",
            corner_radius=15,
            width=380
        )
        left.pack(side="left", fill="both", padx=(0, 10))

        ctk.CTkLabel(
            left,
            text="Student Details",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(20, 15))

        # Form fields
        fields = [
            ("Student ID *", "e.g. MIS/21/001"),
            ("Full Name *",  "Enter full name"),
            ("Email",        "student@nsbm.ac.lk"),
        ]

        self.entries = {}
        for label, placeholder in fields:
            ctk.CTkLabel(
                left,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=NSBM_ACCENT,
                anchor="w"
            ).pack(fill="x", padx=20)

            entry = ctk.CTkEntry(
                left,
                placeholder_text=placeholder,
                height=40,
                font=ctk.CTkFont(size=12),
                fg_color="#050d1a",
                border_color=NSBM_ACCENT,
                border_width=1,
                corner_radius=8
            )
            entry.pack(fill="x", padx=20, pady=(5, 12))
            self.entries[label] = entry

        # Course dropdown
        ctk.CTkLabel(
            left,
            text="Course *",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NSBM_ACCENT,
            anchor="w"
        ).pack(fill="x", padx=20)

        courses         = db.get_all_courses()
        self.course_map = {c['name']: c['id'] for c in courses}
        course_names    = list(self.course_map.keys())

        self.course_var = ctk.StringVar(value=course_names[0] if course_names else "")
        self.course_dropdown = ctk.CTkOptionMenu(
            left,
            values=course_names,
            variable=self.course_var,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8,
            command=self.update_batches
        )
        self.course_dropdown.pack(fill="x", padx=20, pady=(5, 12))

        # Batch dropdown
        ctk.CTkLabel(
            left,
            text="Batch *",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=NSBM_ACCENT,
            anchor="w"
        ).pack(fill="x", padx=20)

        self.batch_var      = ctk.StringVar()
        self.batch_dropdown = ctk.CTkOptionMenu(
            left,
            values=[],
            variable=self.batch_var,
            height=40,
            font=ctk.CTkFont(size=12),
            fg_color="#050d1a",
            button_color=NSBM_GREEN,
            corner_radius=8
        )
        self.batch_dropdown.pack(fill="x", padx=20, pady=(5, 12))

        # Load initial batches
        self.update_batches(course_names[0] if course_names else "")

        # Register button
        ctk.CTkButton(
            left,
            text="📝  Save Student Details",
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=NSBM_GREEN,
            hover_color="#1B5E20",
            corner_radius=10,
            command=self.save_student
        ).pack(fill="x", padx=20, pady=(10, 5))

        # Status label
        self.status_label = ctk.CTkLabel(
            left,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#22C55E",
            wraplength=320
        )
        self.status_label.pack(padx=20, pady=5)

        # Divider
        ctk.CTkFrame(left, height=1, fg_color="#1e4a7a").pack(
            fill="x", padx=20, pady=15
        )

        # Face capture section
        ctk.CTkLabel(
            left,
            text="Face Registration",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=NSBM_ACCENT
        ).pack(anchor="w", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            left,
            text="Capture Progress:",
            font=ctk.CTkFont(size=12),
            text_color=GRAY,
            anchor="w"
        ).pack(fill="x", padx=20)

        self.progress_bar = ctk.CTkProgressBar(
            left, height=15, corner_radius=8,
            progress_color=NSBM_GREEN
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(5, 5))
        self.progress_bar.set(0)

        self.progress_label = ctk.CTkLabel(
            left,
            text="0 / 50 samples captured",
            font=ctk.CTkFont(size=11),
            text_color=GRAY
        )
        self.progress_label.pack(padx=20, pady=(0, 10))

        # Camera buttons
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=5)

        self.capture_btn = ctk.CTkButton(
            btn_frame,
            text="📷 Start Capture",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=NSBM_ACCENT,
            hover_color="#0099BB",
            text_color="#000000",
            corner_radius=8,
            command=self.start_capture
        )
        self.capture_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹ Stop",
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=RED,
            hover_color="#7F0000",
            corner_radius=8,
            command=self.stop_capture,
            state="disabled"
        )
        self.stop_btn.pack(side="right", fill="x", expand=True)

        # Right — Camera preview + student list
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        self.camera_frame = ctk.CTkFrame(
            right, fg_color="#0d1f35",
            corner_radius=15, height=320
        )
        self.camera_frame.pack(fill="x", pady=(0, 10))
        self.camera_frame.pack_propagate(False)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text="📷\nCamera Preview\nClick 'Start Capture' to begin",
            font=ctk.CTkFont(size=14),
            text_color=GRAY
        )
        self.camera_label.pack(expand=True)

        # Registered students list
        ctk.CTkLabel(
            right,
            text="👥 Registered Students",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=WHITE
        ).pack(anchor="w", pady=(5, 8))

        self.students_frame = ctk.CTkScrollableFrame(
            right, fg_color="#0d1f35", corner_radius=15
        )
        self.students_frame.pack(fill="both", expand=True)

        self.load_students()

    # ─────────────────────────────────────────
    def update_batches(self, course_name):
        """Update batch dropdown based on selected course."""
        course_id = self.course_map.get(course_name)
        if course_id:
            batches        = db.get_batches_by_course(course_id)
            self.batch_map = {b['name']: b['id'] for b in batches}
            batch_names    = list(self.batch_map.keys())
            self.batch_dropdown.configure(values=batch_names)
            if batch_names:
                self.batch_var.set(batch_names[0])

    def save_student(self):
        """Save student to database."""
        student_id = self.entries["Student ID *"].get().strip()
        full_name  = self.entries["Full Name *"].get().strip()
        email      = self.entries["Email"].get().strip()
        course     = self.course_var.get()
        batch      = self.batch_var.get()

        if not student_id or not full_name:
            self.status_label.configure(
                text="⚠️ Student ID and Name are required!",
                text_color=RED
            )
            return

        course_id = self.course_map.get(course)
        batch_id  = self.batch_map.get(batch)

        success = db.add_student(
            student_id, full_name, email,
            course_id, batch_id
        )

        if success:
            self.current_student = {
                'student_id': student_id,
                'full_name' : full_name,
                'course_id' : course_id,
                'batch_id'  : batch_id
            }
            self.status_label.configure(
                text=f"✅ {full_name} saved! Now capture face.",
                text_color="#22C55E"
            )
            self.load_students()
        else:
            self.status_label.configure(
                text="⚠️ Student ID already exists!",
                text_color=RED
            )

    def start_capture(self):
        """Start face capture."""
        if not self.current_student:
            self.status_label.configure(
                text="⚠️ Please save student details first!",
                text_color=RED
            )
            return

        self.capturing = True
        self.count     = 0
        self.cap       = cv2.VideoCapture(0)

        self.capture_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")

        folder = f"dataset/{self.current_student['student_id']}"
        os.makedirs(folder, exist_ok=True)

        self.update_camera()

    def update_camera(self):
        """Update camera preview and capture face samples."""
        if not self.capturing:
            return

        success, frame = self.cap.read()
        if not success:
            return

        frame = cv2.flip(frame, 1)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # FIX: use self.face_cascade (not undefined local face_cascade)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5
        )

        for (x, y, w, h) in faces:
            if self.count < self.total:
                self.count   += 1
                face_img      = gray[y:y+h, x:x+w]
                folder        = f"dataset/{self.current_student['student_id']}"
                face_resized  = cv2.resize(face_img, (200, 200))
                cv2.imwrite(f"{folder}/{self.count}.jpg", face_resized)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{self.count}/{self.total}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2
            )

        # Update progress bar (only once, not duplicated)
        progress = self.count / self.total
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"{self.count} / {self.total} samples captured"
        )

        # Show frame in UI
        frame_rgb = cv2.cvtColor(
            cv2.resize(frame, (500, 300)),
            cv2.COLOR_BGR2RGB
        )
        from PIL import Image
        img = ctk.CTkImage(Image.fromarray(frame_rgb), size=(500, 300))
        self.camera_label.configure(image=img, text="")
        self.camera_label.image = img

        # Stop automatically when done
        if self.count >= self.total:
            self.stop_capture()
            self.train_model()
            return

        if self.capturing:
            self.after(50, self.update_camera)

    def stop_capture(self):
        """Stop face capture."""
        self.capturing = False
        if self.cap:
            self.cap.release()
        self.capture_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.camera_label.configure(
            image=None,
            text="📷\nCamera stopped"
        )

    def train_model(self):
        """Train face recognition model."""
        self.status_label.configure(
            text="🔄 Training model...",
            text_color=NSBM_GOLD
        )
        self.update()

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        faces      = []
        labels     = []
        label_map  = {}
        label_id   = 0

        for person_id in os.listdir('dataset'):
            folder = f'dataset/{person_id}'
            if not os.path.isdir(folder):
                continue
            label_map[label_id] = person_id
            for img_file in os.listdir(folder):
                img = cv2.imread(
                    f'{folder}/{img_file}',
                    cv2.IMREAD_GRAYSCALE
                )
                if img is not None:
                    faces.append(img)
                    labels.append(label_id)
            label_id += 1

        if faces:
            recognizer.train(faces, np.array(labels))
            recognizer.write('face_model.yml')
            import json
            with open('label_map.json', 'w') as f:
                json.dump(label_map, f)

            db.update_face_registered(self.current_student['student_id'])

            self.status_label.configure(
                text="✅ Face registered successfully!",
                text_color="#22C55E"
            )
            self.progress_bar.set(1)
            self.load_students()
        else:
            self.status_label.configure(
                text="❌ No faces found!",
                text_color=RED
            )

    def load_students(self):
        """Load and display registered students."""
        for widget in self.students_frame.winfo_children():
            widget.destroy()

        students = db.get_all_students()

        if not students:
            ctk.CTkLabel(
                self.students_frame,
                text="No students registered yet",
                font=ctk.CTkFont(size=13),
                text_color=GRAY
            ).pack(pady=20)
            return

        for student in students:
            row = ctk.CTkFrame(
                self.students_frame,
                fg_color="#050d1a",
                corner_radius=10
            )
            row.pack(fill="x", padx=10, pady=4)

            face_icon = "✅" if student['face_registered'] else "❌"

            ctk.CTkLabel(
                row,
                text=f"{face_icon}  {student['student_id']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=NSBM_ACCENT
            ).pack(side="left", padx=12, pady=10)

            ctk.CTkLabel(
                row,
                text=student['full_name'],
                font=ctk.CTkFont(size=12),
                text_color=WHITE
            ).pack(side="left", padx=5)

            ctk.CTkLabel(
                row,
                text=student.get('course_name', ''),
                font=ctk.CTkFont(size=11),
                text_color=GRAY
            ).pack(side="right", padx=12)