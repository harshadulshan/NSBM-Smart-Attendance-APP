import customtkinter as ctk
import database as db
from login import LoginApp

# ─────────────────────────────────────────
# APP CONFIGURATION
# ─────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def main():
    """Main entry point."""
    print("=" * 50)
    print("  🎓 NSBM Smart Attendance System")
    print("=" * 50)
    print("\n🔄 Initializing database...")

    # Initialize database
    db.initialize_database()

    print("✅ Database ready!")
    print("🚀 Launching application...\n")

    # Launch login screen
    app = LoginApp()
    app.mainloop()


if __name__ == '__main__':
    main()