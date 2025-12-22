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


myappid = 'LightAssist.Cleaner.App'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

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

subtitle = tk.Label(header, text="[ mini kawaii cleaner ]", 
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

def typing_effect(text, tag="cyan"):
    console.config(state="normal")
    for char in text:
        console.insert("end", char, tag)
        console.see("end")
        app.update()
        time.sleep(0.02)
    console.insert("end", "\n")
    console.config(state="disabled")

def show_credits():
    clear_console()
    
    # ASCII header
    log("╔═══════════════════════════════╗", "cyan")
    log("║                               ║", "cyan")
    log_colored([
        ("║     ", "cyan"),
        ("⚡ LIGHT ASSIST ", "pink"),
        ("v1.0      ║", "cyan")
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
                    if size > 100 * 1024:  # Only show files > 100KB
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
        
        # Scanning animation
        log_colored([
            ("  ⟳ ", "cyan"),
            ("Scanning ", "cyan"),
            (name, "yellow"),
            ("...", "white")
        ])
        time.sleep(0.3)
        
        # Get file details
        files_info, folder_size = get_folder_details(folder)
        
        if not files_info:
            log_colored([
                ("    ✓ ", "green"),
                ("Already clean!", "green")
            ])
            log("", "white")
            continue
        
        # Show top files
        log_colored([
            ("    📂 Found ", "white"),
            (str(len(files_info)), "yellow"),
            (" items (", "white"),
            (format_size(folder_size), "cyan"),
            (")", "white")
        ])
        
        # Show sample files
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
        
        # Cleaning
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
        
        # Success message
        log_colored([
            ("    ✓ ", "green"),
            ("Removed ", "green"),
            (str(deleted), "cyan"),
            (" items, freed ", "green"),
            (format_size(freed), "yellow")
        ])
        
        # Sparkles
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
            main_btn.config(state="disabled", text="⧗ CLEANING...")
            
            clear_console()
            
            # Header with animation
            log("╔═══════════════════════════════╗", "cyan")
            log("║   🧹 CLEANING IN PROGRESS    ║", "cyan")
            log("╚═══════════════════════════════╝", "cyan")
            log("", "white")
            
            # Cute cat watching
            log("   /\\_/\\  ", "pink")
            log("  ( •.• ) watching...", "pink")
            log("   > ^ <", "pink")
            log("", "white")
            
            deleted, freed = clean_temp()
            empty_bin()
            optimize_ram()
            
            # Success header
            log("", "white")
            sparkle_line = "".join([random.choice(SPARKLES) + " " for _ in range(8)])
            log(sparkle_line, "yellow")
            log("╔═══════════════════════════════╗", "green")
            log("║      ✨ CLEANUP DONE! ✨     ║", "green")
            log("╚═══════════════════════════════╝", "green")
            log("", "white")
            
            # Summary
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
            
            # Happy cat
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
    try:
        subprocess.Popen("cleanmgr.exe")
        log_colored([
            ("▸ ", "cyan"),
            ("Disk Cleanup opened ", "white"),
            ("💿", "yellow")
        ])
    except:
        pass

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

tk.Label(footer_frame, text="| v1.0", font=FONT_TINY,
        fg=SUBTEXT, bg=BG).pack(side="left")

# ===== INIT =====
show_kawaii_welcome()
update_info()

def auto_update():
    update_info()
    app.after(3000, auto_update)

auto_update()

# ===== RUN =====
app.mainloop()