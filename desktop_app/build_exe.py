"""
Build HeartsConnect.exe
Run from inside desktop_app/:  python build_exe.py
Requires: pip install pywebview pyinstaller pillow
"""
import os
import sys
import subprocess

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICO_SRC = os.path.join(ROOT, "icon.png")
ICO_DST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
HERE    = os.path.dirname(os.path.abspath(__file__))


def convert_icon():
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Pillow not installed — run: pip install pillow")
    if not os.path.exists(ICO_SRC):
        sys.exit(f"icon.png not found at: {ICO_SRC}")
    img = Image.open(ICO_SRC).convert("RGBA")
    img.save(ICO_DST, format="ICO", sizes=[
        (256, 256), (128, 128), (64, 64),
        (48,  48),  (32,  32),  (16, 16),
    ])
    print(f"Icon converted  ->  {ICO_DST}")


def build():
    subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        f"--icon={ICO_DST}",
        "--name=HeartsConnect",
        "main.py",
    ], check=True, cwd=HERE)
    print(f"\nBuild complete  ->  {os.path.join(HERE, 'dist', 'HeartsConnect.exe')}")


if __name__ == "__main__":
    convert_icon()
    build()
