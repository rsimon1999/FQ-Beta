"""Application launcher."""
import os
import sys

# Guarantee the project root directory is at the head of sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Handle both MainApp and MainApplication imports cleanly
try:
    from src.ui.app import MainApp as MainApplication
except ImportError:
    from src.ui.app import MainApplication

def main():
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
