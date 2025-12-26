from tkinter import ttk, scrolledtext
import os
import tempfile
import shutil
import ctypes
import psutil
import subprocess
import threading
import webbrowser
import time
import random
import sys
import requests
import json
from packaging import version
import zipfile

myappid = 'LightAssist.Cleaner.App'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# Make window DPI aware
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

import tkinter as tk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# ===== VERSION CONFIG =====
CURRENT_VERSION = "1.0.1"  # Update ini setiap release
GITHUB_REPO = "MiminCat/lightassist"  # username/repo
UPDATE_CHECK_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

# ===== CYBER CONFIG =====
BG = "#0D0D1E"
CARD = "#1A1A2E"
ACCENT = "#00FFF0"
ACCENT2 = "#FF00FF"
TEXT = "#E0E0E0"
SUBTEXT = "#808080"
SUCCESS = "#00FF88"
WARNING = "#FFD700"
ERROR = "#FF3366"
PINK = "#FF69B4"
PURPLE = "#DA70D6"
BLUE = "#00BFFF"

FONT_TITLE = ("Courier New", 11, "bold")
FONT_TEXT = ("Courier New", 8)
FONT_TINY = ("Courier New", 7)
FONT_CONSOLE = ("Consolas", 8)

# ===== ASCII ART =====
KAWAII_CATS = [
    """
    ／l、
  （ﾟ､ ｡ ７
    l  ~ヽ
    じしf_,)ノ
    """,
    """
    /\\_/\\
   ( o.o )
    > ^ <
    """,
    """
   ∧＿∧
  (｡･ω･｡)つ━☆
  ⊂　　 ノ
    しーＪ
    """
]

SPARKLES = ["✨", "⭐", "💫", "🌟", "✧", "◆", "◇", "★"]

# ===== APP =====
app = tk.Tk()
app.iconbitmap(resource_path("lightassist.ico"))
app.title("LightAssist")
app.geometry("420x580")
app.configure(bg=BG)
app.resizable(False, False)

# ===== STYLE =====
style = ttk.Style()
style.theme_use('clam')
style.configure("Cyber.Horizontal.TProgressbar",
                troughcolor=CARD,
                bordercolor=BG,
                background=ACCENT,
                lightcolor=ACCENT,
                darkcolor=ACCENT,
                thickness=6)

# ===== HEADER =====
header = tk.Frame(app, bg=BG)
header.pack(pady=(12, 8), fill="x")

title_frame = tk.Frame(header, bg=BG)
title_frame.pack()

title = tk.Label(title_frame, text="⚡ LIGHT_ASSIST", 
                font=FONT_TITLE, fg=ACCENT, bg=BG)
title.pack()

subtitle = tk.Label(header, text=f"[ mini kawaii cleaner v{CURRENT_VERSION} ]", 
                   font=FONT_TINY, fg=SUBTEXT, bg=BG)
subtitle.pack()

# ===== INFO CARDS =====
info_frame = tk.Frame(app, bg=BG)
info_frame.pack(padx=15, pady=8, fill="x")

def create_compact_card(parent, icon, label_text):
    card = tk.Frame(parent, bg=CARD, relief="flat")
    card.pack(side="left", expand=True, fill="both", padx=3)
    
    top = tk.Frame(card, bg=CARD)
    top.pack(pady=(6, 2))
    
    tk.Label(top, text=icon, font=("Courier New", 10), 
            fg=ACCENT, bg=CARD).pack(side="left", padx=(8, 4))
    tk.Label(top, text=label_text, font=FONT_TINY, 
            fg=SUBTEXT, bg=CARD).pack(side="left")
    
    value = tk.Label(card, text="--", font=("Courier New", 12, "bold"), 
                    fg=TEXT, bg=CARD)
    value.pack()
    
    progress = ttk.Progressbar(card, length=150, mode='determinate',
                              style="Cyber.Horizontal.TProgressbar")
    progress.pack(pady=(4, 6))
    
    return value, progress

storage_val, storage_prog = create_compact_card(info_frame, "💾", "DISK")
ram_val, ram_prog = create_compact_card(info_frame, "🔋", "RAM")

def update_info():
    try:
        disk = psutil.disk_usage('C:/')
        free_gb = round(disk.free / (1024**3), 1)
        storage_val.config(text=f"{free_gb}GB")
        storage_prog['value'] = disk.percent
        
        if disk.percent > 80:
            storage_val.config(fg=ERROR)
        elif disk.percent > 60:
            storage_val.config(fg=WARNING)
        else:
            storage_val.config(fg=SUCCESS)
        
        mem = psutil.virtual_memory()
        free_gb = round(mem.available / (1024**3), 1)
        ram_val.config(text=f"{free_gb}GB")
        ram_prog['value'] = mem.percent
        
        if mem.percent > 80:
            ram_val.config(fg=ERROR)
        elif mem.percent > 60:
            ram_val.config(fg=WARNING)
        else:
            ram_val.config(fg=SUCCESS)
            
    except Exception as e:
        print(f"Error: {e}")

# ===== MAIN BUTTON =====
btn_frame = tk.Frame(app, bg=BG)
btn_frame.pack(pady=12)

main_btn = tk.Button(
    btn_frame,
    text="▶ CLEAN NOW",
    font=("Courier New", 10, "bold"),
    bg=CARD,
    fg=ACCENT,
    activebackground=ACCENT,
    activeforeground=BG,
    relief="flat",
    bd=0,
    padx=50,
    pady=15,
    cursor="hand2"
)
main_btn.pack()

def btn_enter(e):
    main_btn.config(bg=ACCENT, fg=BG)
def btn_leave(e):
    main_btn.config(bg=CARD, fg=ACCENT)

main_btn.bind("<Enter>", btn_enter)
main_btn.bind("<Leave>", btn_leave)

# ===== COLORFUL CONSOLE =====
console_frame = tk.Frame(app, bg=CARD)
console_frame.pack(padx=15, pady=8, fill="both", expand=True)

tk.Label(console_frame, text="[ CONSOLE ]", font=FONT_TINY, 
        fg=ACCENT, bg=CARD).pack(pady=(6, 3))

console = scrolledtext.ScrolledText(
    console_frame,
    height=12,
    font=FONT_CONSOLE,
    bg="#0A0A15",
    fg=TEXT,
    insertbackground=ACCENT,
    relief="flat",
    bd=0,
    padx=10,
    pady=8,
    wrap="word"
)
console.pack(padx=8, pady=(0, 8), fill="both", expand=True)

# Input field for update response (hidden by default)
input_frame = tk.Frame(console_frame, bg="#0A0A15")

input_label = tk.Label(input_frame, text="Your choice:", 
                      font=FONT_TINY, fg=ACCENT, bg="#0A0A15")
input_label.pack(side="left", padx=(8, 5))

input_entry = tk.Entry(input_frame, font=FONT_CONSOLE, bg="#1a1a2e", 
                      fg=TEXT, insertbackground=ACCENT, relief="flat",
                      bd=0, width=3)
input_entry.pack(side="left", padx=(0, 5))

input_btn = tk.Button(input_frame, text="OK", font=FONT_TINY,
                     bg=CARD, fg=ACCENT, activebackground=ACCENT,
                     activeforeground=BG, relief="flat", bd=0,
                     padx=15, pady=5, cursor="hand2")
input_btn.pack(side="left")

# Configure text tags for colors
console.tag_config("cyan", foreground=ACCENT)
console.tag_config("pink", foreground=PINK)
console.tag_config("purple", foreground=PURPLE)
console.tag_config("green", foreground=SUCCESS)
console.tag_config("yellow", foreground=WARNING)
console.tag_config("red", foreground=ERROR)
console.tag_config("blue", foreground=BLUE)
console.tag_config("white", foreground=TEXT)
console.tag_config("gray", foreground=SUBTEXT)

def log(msg, tag="white", animate=False):
    console.config(state="normal")
    if animate:
        for char in msg:
            console.insert("end", char, tag)
            console.see("end")
            app.update()
            time.sleep(0.005)
        console.insert("end", "\n")
    else:
        console.insert("end", f"{msg}\n", tag)
    console.see("end")
    console.config(state="disabled")
    app.update_idletasks()

def log_colored(parts):
    """Log multiple colored parts in one line"""
    console.config(state="normal")
    for text, tag in parts:
        console.insert("end", text, tag)
    console.insert("end", "\n")
    console.see("end")
    console.config(state="disabled")
    app.update_idletasks()

def clear_console():
    console.config(state="normal")
    console.delete("1.0", "end")
    console.config(state="disabled")

def show_kawaii_welcome():
    clear_console()
    cat = random.choice(KAWAII_CATS)
    for line in cat.split('\n'):
        log(line, "pink")
    log("", "white")
    log_colored([
        ("  Welcome to ", "white"),
        ("Light", "cyan"),
        ("Assist ", "pink"),
        ("~(｡♥‿♥｡)", "purple")
    ])
    log("", "white")

def show_credits():
    clear_console()
    
    # ASCII header
    log("╔═══════════════════════════════╗", "cyan")
    log("║                               ║", "cyan")
    log_colored([
        ("║     ", "cyan"),
        ("⚡ LIGHT ASSIST ", "pink"),
        (f"v{CURRENT_VERSION}      ║", "cyan")
    ])
    log("║                               ║", "cyan")
    log("╠═══════════════════════════════╣", "cyan")
    
    # Kawaii divider
    sparkle = " ".join(random.sample(SPARKLES, 5))
    log(f"  {sparkle}", "yellow")
    log("", "white")
    
    # Credits
    log_colored([("  ", "white"), ("Powered by:", "purple")])
    log("", "white")
    log_colored([("    ", "white"), ("✨ ChatGPT", "cyan")])
    log_colored([("    ", "white"), ("💜 Claude AI", "purple")])
    log("", "white")
    
    # Cute message
    log_colored([
        ("  Made with ", "white"),
        ("♥", "pink"),
        (" & ", "white"),
        ("✨", "yellow"),
        (" for you!", "white")
    ])
    log("", "white")
    
    # ASCII cat
    log("     /\\_/\\  ", "pink")
    log("    ( ^.^ ) ~nyaa", "pink")
    log("     > ^ <", "pink")
    log("", "white")
    
    log("╚═══════════════════════════════╝", "cyan")

# ===== UPDATE SYSTEM =====
update_data = {}
update_mode_active = False  # Flag untuk cek apakah sedang dalam mode update

def check_for_updates():
    """Check GitHub for new version"""
    try:
        response = requests.get(UPDATE_CHECK_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest = data['tag_name'].replace('v', '')
            
            if version.parse(latest) > version.parse(CURRENT_VERSION):
                return {
                    'available': True,
                    'version': latest,
                    'url': data['assets'][0]['browser_download_url'] if data['assets'] else None,
                    'notes': data['body']
                }
    except:
        pass
    
    return {'available': False}

def show_update_notification(update_info):
    """Show cute update notification in console - NON-BLOCKING"""
    global update_data
    update_data = update_info
    
    clear_console()
    
    # Excited cat
    log("     /\\_/\\  ", "pink")
    log("    ( *o* )!! ", "pink")
    log("     > ^ <", "pink")
    log("", "white")
    
    # Update header
    log("╔═══════════════════════════════╗", "yellow")
    log("║   🎉 UPDATE AVAILABLE! 🎉    ║", "yellow")
    log("╚═══════════════════════════════╝", "yellow")
    log("", "white")
    
    # Version info
    log_colored([
        ("  Current: ", "white"),
        (f"v{CURRENT_VERSION}", "gray"),
        (" → New: ", "white"),
        (f"v{update_info['version']}", "cyan"),
        (" ✨", "yellow")
    ])
    log("", "white")
    
    # What's new (first 3 lines)
    if update_info.get('notes'):
        log("  📝 What's New:", "purple")
        notes_lines = update_info['notes'].split('\n')[:3]
        for line in notes_lines:
            if line.strip():
                log(f"    • {line.strip()[:40]}", "white")
    
    log("", "white")
    
    # Sparkles
    sparkles = "".join([random.choice(SPARKLES) + " " for _ in range(8)])
    log(f"  {sparkles}", "yellow")
    log("", "white")
    
    # Non-blocking prompt
    log_colored([
        ("  💾 ", "cyan"),
        ("Want to update? Type Y below ⬇", "yellow")
    ])
    log_colored([
        ("  ℹ️  ", "gray"),
        ("Or just use the app normally - I won't bug you!", "gray")
    ])
    log("", "white")
    
    # Show input field (but don't disable buttons!)
    input_frame.pack(padx=8, pady=(0, 8), fill="x")
    input_entry.delete(0, tk.END)
    input_entry.focus_set()

def download_with_progress(url, dest_path):
    """Download file with animated progress"""
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    
    log("", "white")
    log("  ╔════════════════════════════╗", "cyan")
    log("  ║   📥 DOWNLOADING UPDATE    ║", "cyan")
    log("  ╚════════════════════════════╝", "cyan")
    log("", "white")
    
    downloaded = 0
    block_size = 8192
    
    # Create initial progress line
    log("  [░░░░░░░░░░░░░░░░░░░░] 0% ✨", "cyan")
    
    with open(dest_path, 'wb') as f:
        for chunk in response.iter_content(block_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                percent = int((downloaded / total) * 100)
                
                # Animated progress bar
                filled = int(percent / 5)
                bar = "█" * filled + "░" * (20 - filled)
                sparkle = random.choice(SPARKLES)
                
                # Update last line instead of deleting
                console.config(state="normal")
                # Get current line position
                last_line_start = console.index("end-2l linestart")
                last_line_end = console.index("end-2l lineend")
                # Delete last line
                console.delete(last_line_start, last_line_end)
                # Insert new progress
                console.insert(last_line_start, f"  [{bar}] {percent}% {sparkle}", "cyan")
                console.see("end")
                console.config(state="disabled")
                
                app.update_idletasks()
                time.sleep(0.02)
    
    log("", "white")
    log_colored([
        ("  ✓ ", "green"),
        ("Download complete! ", "green"),
        ("🎉", "yellow")
    ])

def install_update(zip_path):
    """Install the update"""
    log("", "white")
    log("  ╔════════════════════════════╗", "purple")
    log("  ║   ⚡ INSTALLING UPDATE     ║", "purple")
    log("  ╚════════════════════════════╝", "purple")
    log("", "white")
    
    # Cute loading animation
    log("  Installing... (｡♥‿♥｡)", "cyan")
    
    for i in range(3):
        time.sleep(0.5)
        log(f"  {'.' * (i + 1)}", "cyan")
    
    try:
        # Extract update to temp folder
        extract_path = os.path.join(tempfile.gettempdir(), "lightassist_update")
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path, ignore_errors=True)
        os.makedirs(extract_path, exist_ok=True)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # Get current exe path
        if getattr(sys, 'frozen', False):
            current_exe = sys.executable
            current_dir = os.path.dirname(current_exe)
        else:
            current_exe = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_exe)
        
        # Create batch file for update
        batch_script = os.path.join(tempfile.gettempdir(), "lightassist_update.bat")
        
        with open(batch_script, 'w') as f:
            f.write(f"""@echo off
echo Updating LightAssist...
timeout /t 2 /nobreak > nul

REM Kill current process
taskkill /F /IM LightAssist.exe > nul 2>&1

REM Copy new files
xcopy /s /y /q "{extract_path}\\*.*" "{current_dir}\\" > nul

REM Restart application
start "" "{current_exe}"

REM Cleanup
timeout /t 1 /nobreak > nul
rmdir /s /q "{extract_path}" > nul 2>&1
del "%~f0"
""")
        
        log("", "white")
        log_colored([
            ("  ✓ ", "green"),
            ("Update ready! Restarting... ", "green"),
            ("✨", "yellow")
        ])
        log("", "white")
        
        # Happy cat
        log("     /\\_/\\  ", "pink")
        log("    ( ^ω^ ) Bye~!", "pink")
        log("     > ^ <", "pink")
        
        time.sleep(2)
        
        # Run update script
        subprocess.Popen(batch_script, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        app.quit()
        
    except Exception as e:
        log("", "white")
        log_colored([
            ("  ✗ ", "red"),
            (f"Update failed: {str(e)}", "red")
        ])
        log("", "white")
        log("  You can download manually from GitHub", "gray")
        enable_all_buttons()

def enable_all_buttons():
    """Re-enable all buttons after update prompt closed"""
    global update_mode_active
    update_mode_active = False
    # Buttons never disabled now, so this just resets the flag

def handle_update_response(response):
    """Handle Y/N response"""
    response = response.lower().strip()
    
    # Hide input field
    input_frame.pack_forget()
    
    if response == 'y':
        # Excited response
        log_colored([
            ("  ", "white"),
            ("Yay! ", "pink"),
            ("(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "yellow")
        ])
        
        if update_data.get('url'):
            def update_thread():
                try:
                    zip_path = os.path.join(tempfile.gettempdir(), "lightassist_update.zip")
                    download_with_progress(update_data['url'], zip_path)
                    install_update(zip_path)
                except Exception as e:
                    log("", "white")
                    log_colored([
                        ("  ✗ ", "red"),
                        (f"Error: {str(e)}", "red")
                    ])
                    log("", "white")
                    log("  (｡•́︿•̀｡) Update failed, but app still works!", "pink")
            
            threading.Thread(target=update_thread, daemon=True).start()
        else:
            log_colored([
                ("  ✗ ", "red"),
                ("No download URL available", "red")
            ])
    
    elif response == 'n' or response == '':
        log_colored([
            ("  ", "white"),
            ("No problem! ", "white"),
            ("(｡♥‿♥｡)", "pink")
        ])
        log("", "white")
        log("  You can update anytime from 🔄 Update button", "gray")
        log("", "white")
    
    else:
        log_colored([
            ("  ", "white"),
            ("❌ Invalid! Type ", "red"),
            ("Y", "cyan"),
            (" to update or just close this", "white")
        ])
        log("", "white")
        # Show input again
        input_frame.pack(padx=8, pady=(0, 8), fill="x")
        input_entry.delete(0, tk.END)
        input_entry.focus_set()

def on_input_submit():
    """Handle input submission"""
    response = input_entry.get()
    handle_update_response(response)

def on_key_press(event):
    """Handle keyboard input for update prompt"""
    if event.keysym == "Return":
        on_input_submit()

# Bind input events
input_entry.bind("<Return>", on_key_press)
input_btn.config(command=on_input_submit)

console.bind("<KeyPress>", on_key_press)

# ===== MINI TOOLS =====
tools = tk.Frame(app, bg=BG)
tools.pack(padx=15, pady=6, fill="x")

def create_mini_btn(parent, txt, cmd):
    btn = tk.Button(parent, text=txt, font=FONT_TINY,
                   bg=CARD, fg=TEXT, activebackground="#252538",
                   activeforeground=ACCENT, relief="flat", bd=0,
                   padx=6, pady=6, cursor="hand2", command=cmd)
    btn.pack(side="left", expand=True, fill="x", padx=2)
    
    def enter(e): btn.config(bg="#252538", fg=ACCENT)
    def leave(e): btn.config(bg=CARD, fg=TEXT)
    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn

# ===== CLEANING FUNCTIONS =====
def get_folder_details(path):
    """Get detailed file list"""
    files_info = []
    total_size = 0
    
    if not os.path.exists(path):
        return files_info, total_size
    
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    total_size += size
                    if size > 100 * 1024:
                        files_info.append((item, size, "file"))
                elif os.path.isdir(item_path):
                    folder_size = 0
                    for root, dirs, files in os.walk(item_path):
                        for f in files:
                            try:
                                folder_size += os.path.getsize(os.path.join(root, f))
                            except:
                                pass
                    total_size += folder_size
                    if folder_size > 100 * 1024:
                        files_info.append((item, folder_size, "folder"))
            except:
                pass
    except:
        pass
    
    return files_info, total_size

def format_size(bytes_size):
    """Format bytes to human readable"""
    if bytes_size < 1024:
        return f"{bytes_size}B"
    elif bytes_size < 1024**2:
        return f"{round(bytes_size/1024, 1)}KB"
    elif bytes_size < 1024**3:
        return f"{round(bytes_size/(1024**2), 1)}MB"
    else:
        return f"{round(bytes_size/(1024**3), 2)}GB"

def clean_temp():
    folders = {
        "User Temp (%TEMP%)": tempfile.gettempdir(),
        "Windows Temp": "C:\\Windows\\Temp"
    }
    
    total_del = 0
    total_size = 0
    
    for name, folder in folders.items():
        if not os.path.exists(folder):
            log_colored([
                ("  ✗ ", "red"),
                (name, "white"),
                (" not found", "gray")
            ])
            continue
        
        log_colored([
            ("  ⟳ ", "cyan"),
            ("Scanning ", "cyan"),
            (name, "yellow"),
            ("...", "white")
        ])
        time.sleep(0.3)
        
        files_info, folder_size = get_folder_details(folder)
        
        if not files_info:
            log_colored([
                ("    ✓ ", "green"),
                ("Already clean!", "green")
            ])
            log("", "white")
            continue
        
        log_colored([
            ("    📂 Found ", "white"),
            (str(len(files_info)), "yellow"),
            (" items (", "white"),
            (format_size(folder_size), "cyan"),
            (")", "white")
        ])
        
        for item_name, item_size, item_type in sorted(files_info, key=lambda x: x[1], reverse=True)[:3]:
            icon = "📄" if item_type == "file" else "📁"
            log_colored([
                (f"      {icon} ", "white"),
                (item_name[:30], "gray"),
                (" - ", "white"),
                (format_size(item_size), "yellow")
            ])
        
        if len(files_info) > 3:
            log(f"      ... and {len(files_info) - 3} more", "gray")
        
        log_colored([
            ("    ⚡ ", "purple"),
            ("Cleaning...", "purple")
        ])
        
        deleted = 0
        freed = 0
        
        try:
            for item in os.listdir(folder):
                path = os.path.join(folder, item)
                try:
                    if os.path.isfile(path):
                        size = os.path.getsize(path)
                        os.unlink(path)
                        deleted += 1
                        freed += size
                    elif os.path.isdir(path):
                        for root, dirs, files_in_dir in os.walk(path):
                            for f in files_in_dir:
                                try:
                                    freed += os.path.getsize(os.path.join(root, f))
                                except:
                                    pass
                        shutil.rmtree(path, ignore_errors=True)
                        deleted += 1
                except:
                    pass
        except:
            pass
        
        total_del += deleted
        total_size += freed
        
        log_colored([
            ("    ✓ ", "green"),
            ("Removed ", "green"),
            (str(deleted), "cyan"),
            (" items, freed ", "green"),
            (format_size(freed), "yellow")
        ])
        
        sparkles = "".join(random.sample(SPARKLES, 3))
        log(f"      {sparkles}", "pink")
        log("", "white")
    
    return total_del, total_size

def empty_bin():
    try:
        log_colored([
            ("  ⟳ ", "cyan"),
            ("Emptying Recycle Bin...", "cyan")
        ])
        time.sleep(0.3)
        ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0)
        log_colored([
            ("    ✓ ", "green"),
            ("Recycle Bin emptied! ", "green"),
            ("🗑️✨", "yellow")
        ])
        return True
    except:
        log_colored([
            ("    ✗ ", "red"),
            ("Failed to empty bin", "red")
        ])
        return False

def optimize_ram():
    try:
        log_colored([
            ("  ⟳ ", "cyan"),
            ("Optimizing RAM...", "cyan")
        ])
        time.sleep(0.3)
        before = psutil.virtual_memory().percent
        ctypes.windll.psapi.EmptyWorkingSet(-1)
        after = psutil.virtual_memory().percent
        saved = round(before - after, 1)
        log_colored([
            ("    ✓ ", "green"),
            ("RAM optimized! Freed ~", "green"),
            (f"{saved}%", "cyan"),
            (" 💾✨", "yellow")
        ])
        return True
    except:
        log_colored([
            ("    ✗ ", "red"),
            ("Failed to optimize RAM", "red")
        ])
        return False

def main_clean():
    def thread():
        try:
            # If user clicks while update notification is showing, just hide it
            if input_frame.winfo_ismapped():
                input_frame.pack_forget()
            
            main_btn.config(state="disabled", text="⧗ CLEANING...")
            
            clear_console()
            
            log("╔═══════════════════════════════╗", "cyan")
            log("║   🧹 CLEANING IN PROGRESS    ║", "cyan")
            log("╚═══════════════════════════════╝", "cyan")
            log("", "white")
            
            log("   /\\_/\\  ", "pink")
            log("  ( •.• ) watching...", "pink")
            log("   > ^ <", "pink")
            log("", "white")
            
            deleted, freed = clean_temp()
            empty_bin()
            optimize_ram()
            
            log("", "white")
            sparkle_line = "".join([random.choice(SPARKLES) + " " for _ in range(8)])
            log(sparkle_line, "yellow")
            log("╔═══════════════════════════════╗", "green")
            log("║      ✨ CLEANUP DONE! ✨     ║", "green")
            log("╚═══════════════════════════════╝", "green")
            log("", "white")
            
            mb = round(freed / (1024**2), 1)
            log_colored([
                ("  📊 ", "white"),
                ("Summary:", "purple")
            ])
            log_colored([
                ("    • Files removed: ", "white"),
                (str(deleted), "cyan")
            ])
            log_colored([
                ("    • Space freed: ", "white"),
                (f"{mb} MB", "yellow")
            ])
            log_colored([
                ("    • RAM optimized: ", "white"),
                ("✓", "green")
            ])
            log("", "white")
            
            log("     /\\_/\\  ", "pink")
            log("    ( ^ω^ ) Done~!", "pink")
            log("     > ^ <", "pink")
            
            update_info()
            main_btn.config(state="normal", text="▶ CLEAN NOW")
            
        except Exception as e:
            log_colored([
                ("  ✗ Error: ", "red"),
                (str(e), "white")
            ])
            main_btn.config(state="normal", text="▶ CLEAN NOW")
    
    threading.Thread(target=thread, daemon=True).start()

def ram_only():
    def thread():
        # Hide update prompt if showing
        if input_frame.winfo_ismapped():
            input_frame.pack_forget()
        
        clear_console()
        log("╔═══════════════════════════════╗", "cyan")
        log("║     💾 RAM OPTIMIZATION      ║", "cyan")
        log("╚═══════════════════════════════╝", "cyan")
        log("", "white")
        optimize_ram()
        update_info()
        log("", "white")
        log("  (｡♥‿♥｡) All done!", "pink")
    threading.Thread(target=thread, daemon=True).start()

def troubleshoot():
    # Hide update prompt if showing
    if input_frame.winfo_ismapped():
        input_frame.pack_forget()
    
    try:
        subprocess.Popen("msdt.exe -id DeviceDiagnostic")
        log_colored([
            ("▸ ", "cyan"),
            ("Troubleshooter opened ", "white"),
            ("🔧", "yellow")
        ])
    except:
        pass

def disk_clean():
    # Hide update prompt if showing
    if input_frame.winfo_ismapped():
        input_frame.pack_forget()
    
    try:
        subprocess.Popen("cleanmgr.exe")
        log_colored([
            ("▸ ", "cyan"),
            ("Disk Cleanup opened ", "white"),
            ("💿", "yellow")
        ])
    except:
        pass

def manual_update_check():
    """Manual update check button"""
    def thread():
        # If already in update mode, ignore
        if update_mode_active:
            return
        
        clear_console()
        log("╔═══════════════════════════════╗", "cyan")
        log("║   🔍 CHECKING FOR UPDATES    ║", "cyan")
        log("╚═══════════════════════════════╝", "cyan")
        log("", "white")
        
        # Cute searching animation
        search_frames = ["(•‿•)", "(◕‿◕)", "(✿◠‿◠)", "(｡♥‿♥｡)"]
        for i in range(4):
            console.config(state="normal")
            console.delete("end-2l", "end-1l")
            console.config(state="disabled")
            log_colored([
                ("  Searching... ", "cyan"),
                (search_frames[i % len(search_frames)], "pink")
            ])
            time.sleep(0.3)
        
        log("", "white")
        
        update_info = check_for_updates()
        
        if update_info['available']:
            show_update_notification(update_info)
        else:
            log_colored([
                ("  ✓ ", "green"),
                ("You're using the latest version! ", "green"),
                ("🎉", "yellow")
            ])
            log("", "white")
            log("     /\\_/\\  ", "pink")
            log("    ( ^‿^ ) Perfect!", "pink")
            log("     > ^ <", "pink")
    
    threading.Thread(target=thread, daemon=True).start()

# ===== COMMANDS =====
main_btn.config(command=main_clean)
create_mini_btn(tools, "[RAM]", ram_only)
create_mini_btn(tools, "[FIX]", troubleshoot)
create_mini_btn(tools, "[DISK]", disk_clean)

# ===== FOOTER =====
footer_frame = tk.Frame(app, bg=BG)
footer_frame.pack(side="bottom", pady=8)

github_btn = tk.Label(
    footer_frame,
    text="⚡ GitHub",
    font=FONT_TINY,
    fg=ACCENT,
    bg=BG,
    cursor="hand2"
)
github_btn.pack(side="left", padx=4)

def open_github(e):
    webbrowser.open("https://github.com/MiminCat/lightassist")

github_btn.bind("<Button-1>", open_github)

def github_enter(e):
    github_btn.config(fg=ACCENT2)
def github_leave(e):
    github_btn.config(fg=ACCENT)

github_btn.bind("<Enter>", github_enter)
github_btn.bind("<Leave>", github_leave)

# Update check button
update_btn = tk.Label(
    footer_frame,
    text="🔄 Update",
    font=FONT_TINY,
    fg=SUBTEXT,
    bg=BG,
    cursor="hand2"
)
update_btn.pack(side="left", padx=4)

update_btn.bind("<Button-1>", lambda e: manual_update_check())

def update_enter(e):
    update_btn.config(fg=ACCENT)
def update_leave(e):
    update_btn.config(fg=SUBTEXT)

update_btn.bind("<Enter>", update_enter)
update_btn.bind("<Leave>", update_leave)

credits_btn = tk.Label(
    footer_frame,
    text="ⓘ Credits",
    font=FONT_TINY,
    fg=SUBTEXT,
    bg=BG,
    cursor="hand2"
)
credits_btn.pack(side="left", padx=4)

credits_btn.bind("<Button-1>", lambda e: show_credits())

def credits_enter(e):
    credits_btn.config(fg=ACCENT)
def credits_leave(e):
    credits_btn.config(fg=SUBTEXT)

credits_btn.bind("<Enter>", credits_enter)
credits_btn.bind("<Leave>", credits_leave)

tk.Label(footer_frame, text=f"| v{CURRENT_VERSION}", font=FONT_TINY,
        fg=SUBTEXT, bg=BG).pack(side="left")

# ===== AUTO UPDATE CHECK ON STARTUP =====
def startup_update_check():
    """Check for updates on startup (silent)"""
    try:
        update_info = check_for_updates()
        if update_info['available']:
            # Wait a bit before showing notification
            time.sleep(2)
            show_update_notification(update_info)
    except:
        pass

# ===== INIT =====
show_kawaii_welcome()
update_info()

def auto_update():
    update_info()
    app.after(3000, auto_update)

auto_update()

# Start update check in background
threading.Thread(target=startup_update_check, daemon=True).start()

# ===== RUN =====
app.mainloop()