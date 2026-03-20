<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:050d1a,50:235895,100:60b94b&height=220&section=header&text=NSBM%20Smart%20Attendance&fontSize=48&fontColor=cfff5a&animation=twinkling&fontAlignY=38&desc=AI-Powered%20Desktop%20Attendance%20System%20for%20NSBM%20Green%20University&descAlignY=58&descSize=15&descColor=aabbcc"/>

---

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=22&duration=3000&pause=800&color=60b94b&center=true&vCenter=true&width=800&height=60&lines=🎓+Built+for+NSBM+Green+University;🤖+Real-time+AI+Face+Recognition;📊+Live+Analytics+%26+Dashboard;🔒+Secure+Multi-Role+Access+System;📦+Packaged+as+Windows+.exe+App;🎨+Glassmorphism+UI+with+NSBM+Colors)](https://git.io/typing-svg)

<br/>

<img src="https://img.shields.io/badge/Python-3.14-050d1a?style=for-the-badge&logo=python&logoColor=cfff5a"/>
<img src="https://img.shields.io/badge/OpenCV-LBPH-050d1a?style=for-the-badge&logo=opencv&logoColor=60b94b"/>
<img src="https://img.shields.io/badge/CustomTkinter-GUI-050d1a?style=for-the-badge&logo=python&logoColor=cfff5a"/>
<img src="https://img.shields.io/badge/SQLite-Database-050d1a?style=for-the-badge&logo=sqlite&logoColor=60b94b"/>
<img src="https://img.shields.io/badge/PyInstaller-Packaged-050d1a?style=for-the-badge&logo=python&logoColor=cfff5a"/>

<br/><br/>

<img src="https://img.shields.io/github/stars/harshadulshan/NSBM-Smart-Attendance?style=for-the-badge&color=cfff5a&labelColor=050d1a"/>
<img src="https://img.shields.io/github/forks/harshadulshan/NSBM-Smart-Attendance?style=for-the-badge&color=60b94b&labelColor=050d1a"/>
<img src="https://img.shields.io/github/last-commit/harshadulshan/NSBM-Smart-Attendance?style=for-the-badge&color=235895&labelColor=050d1a"/>
<img src="https://img.shields.io/github/license/harshadulshan/NSBM-Smart-Attendance?style=for-the-badge&color=60b94b&labelColor=050d1a"/>
<img src="https://img.shields.io/badge/Platform-Windows-050d1a?style=for-the-badge&logo=windows&logoColor=cfff5a"/>

</div>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🎯 What is This?

<table>
<tr>
<td width="60%" valign="top">

A **fully functional AI-powered Desktop Application** built exclusively for **NSBM Green University**. The system uses **OpenCV LBPH Face Recognition** to automatically detect, identify and mark student attendance in real-time through a webcam — eliminating manual roll calls and proxy attendance forever.

The application is packaged as a **Windows .exe** file — no Python installation required on target machines!

> 🎓 *"From registration to report generation — fully automated with AI!"*

</td>
<td width="40%" align="center" valign="top">

<img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="260"/>

</td>
</tr>
</table>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   NSBM Smart Attendance                     │
│                      main.py (Launcher)                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────▼──────────────┐
            │        login.py             │
            │   🔒 Authentication Layer   │
            │   Admin | Lecturer | Student│
            └──────────────┬──────────────┘
                           │
            ┌──────────────▼──────────────┐
            │         home.py             │
            │    🏠 Dashboard & Router    │
            └──┬────────┬────────┬────────┘
               │        │        │
    ┌──────────▼──┐  ┌──▼─────┐  ┌▼──────────┐
    │register.py  │  │attend. │  │reports.py │
    │📸 Face Reg  │  │🎯 Mark │  │📊 Reports │
    └──────┬──────┘  └──┬─────┘  └───────────┘
           │            │
    ┌──────▼─────────────▼──────┐
    │        database.py        │
    │   🗄️ SQLite Data Layer    │
    │  Users|Students|Attend.   │
    └───────────────────────────┘
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Security & Access
- 🔒 **Secure Login** — Multi-role authentication
- 👨‍💼 **Admin Panel** — Full system control
- 👨‍🏫 **Lecturer Access** — Mark & view class attendance
- 👨‍🎓 **Student Portal** — View own records
- 🔑 **Password Protection** — Encrypted credentials

### 🤖 AI & Recognition
- 📸 **Face Registration** — Capture 50 face samples
- 🧠 **LBPH Algorithm** — Accurate face recognition
- ⚡ **Real-time Detection** — Live webcam processing
- 🔍 **Confidence Score** — Recognition accuracy display
- ⚠️ **Unknown Detection** — Flag unregistered faces

### 📅 Attendance Management
- ✅ **Auto Marking** — Instant attendance on recognition
- 🔴 **Late Detection** — Configurable late arrival time
- 🔁 **Duplicate Check** — Prevent double marking
- 📚 **Session Tracking** — Morning/Afternoon/Lab sessions
- 🕒 **Timetable Integration** — Auto-detect current class

</td>
<td width="50%">

### 📊 Reports & Analytics
- 📋 **Attendance Log** — Full detailed records
- 👤 **Student Summary** — Individual attendance stats
- ⚠️ **Below 80% Alert** — Automatic warning list
- 📆 **Date Range Filter** — Custom period reports
- 🎓 **Course/Batch Filter** — Targeted reports
- 📥 **Excel Export** — Professional formatted reports

### 🎨 UI & Experience
- 🌙 **Glassmorphism Design** — Modern dark theme
- 🎨 **NSBM Color Scheme** — Official university colors
- 💫 **Smooth Animations** — Professional transitions
- 🔢 **Animated Counters** — Live stat updates
- 💡 **Glow Effects** — Interactive hover animations
- 📱 **Responsive Layout** — Adapts to window size

### 📧 Communication
- 📧 **Email Reports** — Auto daily summary
- 📊 **Excel Attachment** — Report in email
- 🎨 **HTML Email** — Beautiful formatted email

</td>
</tr>
</table>

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 📊 System Stats at a Glance

```
╔══════════════════════════════════════════════════════════════╗
║              📊 NSBM Smart Attendance — Stats                ║
╠══════════════╦═══════════════╦══════════════╦════════════════╣
║  👥 Students ║ 📋 Attendance ║  🎓 Courses  ║  👤 User Roles ║
║   Unlimited  ║   Auto-saved  ║      5+      ║      3         ║
╠══════════════╬═══════════════╬══════════════╬════════════════╣
║  📸 Samples  ║  🎯 Accuracy  ║  📦 App Size ║  🖥️ Platform  ║
║  50 per face ║    90 pct+    ║   ~250 MB    ║  Windows 10/11 ║
╚══════════════╩═══════════════╩══════════════╩════════════════╝
```

---

## 🗄️ Database Schema

```
📦 attendance.db (SQLite)
│
├── 👥 users
│   ├── id, username, password
│   ├── role (admin/lecturer/student)
│   └── full_name, email
│
├── 🎓 students
│   ├── student_id, full_name, email
│   ├── course_id  courses.id
│   ├── batch_id   batches.id
│   └── face_registered (0/1)
│
├── 📚 courses
│   ├── id, name, code
│   └── department_id  departments.id
│
├── 📅 timetable
│   ├── course_id, batch_id
│   ├── subject, day_of_week
│   ├── start_time, end_time
│   └── lecturer_id  users.id
│
└── ✅ attendance
    ├── student_id, student_name
    ├── course_id, batch_id
    ├── date, time, status
    ├── arrival (On Time / Late)
    ├── session, marked_by
    └── created_at
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🖥️ App Screenshots

### 🔒 Login Screen
> Glassmorphism design with particle animation

![Login](login.png)

---

### 🏠 Home Dashboard
> Animated stat counters and quick actions

![Home](home.png)

---

### 📸 Student Registration
> Face capture with live camera preview

![Register](register.png)

---

### 🎯 Mark Attendance
> Real-time face recognition with confidence display

![Attendance](attendance.png)

---

### 📊 Reports & Analytics
> Tabbed reports with filters and Excel export

![Reports](reports.png)

---

### ⚙️ Settings Panel
> User management and timetable setup

![Settings](settings.png)
```

---

## STEP 4 — Commit Changes

Commit message:
```
📸 Add app screenshots to README

---

## 🎓 NSBM Departments & Courses

```
🏛️ Faculty of Computing (FOC)
    ├── BSc Management Information Systems (MIS)
    ├── BSc Computer Science (CS)
    ├── BSc Information Technology (IT)
    └── BSc Software Engineering (SE)

🏛️ Faculty of Business (FOB)
    └── BSc Business Management (BM)

🏛️ Faculty of Engineering (FOE)
🏛️ Faculty of Science (FOS)
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install customtkinter opencv-python pillow pandas openpyxl
```

### Run the App
```bash
python main.py
```

### OR — Run the .exe
```
1. Download NSBM_SmartAttendance.zip from Releases
2. Extract the zip file
3. Double click NSBM_SmartAttendance.exe
4. No Python installation needed!
```

### Default Admin Login
```
Username : admin
Password : admin123
```

---

## 📁 Project Structure

```
NSBM-Smart-Attendance/
│
├── main.py           ← App entry point
├── database.py       ← SQLite models & queries
├── login.py          ← Authentication screen
├── home.py           ← Dashboard & navigation
├── register.py       ← Student & face registration
├── attendance.py     ← Real-time attendance marking
├── reports.py        ← Analytics & reports
├── settings.py       ← Admin settings panel
├── icon.png          ← Application icon
│
├── database/         ← SQLite database files
├── dataset/          ← Registered face images
├── snapshots/        ← Attendance snapshots
├── reports/          ← Generated Excel reports
└── dist/             ← Packaged .exe output
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 🛠️ Tech Stack

<div align="center">

| Category | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.14 | Core development |
| **GUI Framework** | CustomTkinter | Modern desktop UI |
| **Face Recognition** | OpenCV LBPH | AI detection engine |
| **Computer Vision** | OpenCV | Camera & image processing |
| **Database** | SQLite | Local data storage |
| **Data Processing** | Pandas | Report analytics |
| **Excel Export** | OpenPyXL | Report generation |
| **Email** | SMTP + MIMEText | Auto email reports |
| **Packaging** | PyInstaller | Windows .exe creation |
| **Image Processing** | Pillow | UI image handling |

</div>

---

## 🗺️ Development Roadmap

```
Phase 1 — Core System
   SQLite database design
   Multi-role authentication
   Student registration

Phase 2 — AI Engine
   Face capture & training
   Real-time recognition
   Late arrival detection

Phase 3 — Analytics
   Reports & filters
   Excel export
   Email automation

Phase 4 — Polish
   Glassmorphism UI redesign
   NSBM color scheme
   Animations & effects
   Packaged as .exe

Phase 5 — Future (Coming Soon)
   QR Code scanning
   Mobile companion app
   Cloud sync
   SMS notifications
```

---

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%">

---

## 👨‍💻 Author

<div align="center">

### Harsha Dulshan Kaldera
**MIS Undergraduate | AI Researcher | Entrepreneur**
*NSBM Green University — Expected 2026*

[![GitHub](https://img.shields.io/badge/GitHub-harshadulshan-050d1a?style=for-the-badge&logo=github&logoColor=cfff5a)](https://github.com/harshadulshan)
[![Email](https://img.shields.io/badge/Email-hphdkaldera%40gmail.com-050d1a?style=for-the-badge&logo=gmail&logoColor=60b94b)](mailto:hphdkaldera@gmail.com)

</div>

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs via Issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star the repository

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:60b94b,50:235895,100:050d1a&height=130&section=footer&animation=fadeIn"/>

<div align="center">

**⭐ If this project helped you, please give it a star! ⭐**

[![GitHub stars](https://img.shields.io/github/stars/harshadulshan/NSBM-Smart-Attendance?style=social)](https://github.com/harshadulshan/NSBM-Smart-Attendance)
[![GitHub watchers](https://img.shields.io/github/watchers/harshadulshan/NSBM-Smart-Attendance?style=social)](https://github.com/harshadulshan/NSBM-Smart-Attendance)

*Built with love for NSBM Green University*

</div>
