import customtkinter
import google.generativeai as genai
import os
import threading
import subprocess
import wmi
from tkinter import messagebox
import ctypes
import sys
import tkinter as tk
from PIL import Image
from dotenv import load_dotenv
from dns_changer import change_dns, get_active_adapter

from sidebar import Sidebar
from convercation import Conversation, TopBar
from user_input import User_input

# مسیر فعلی فایل main.py
current_dir = os.path.dirname(os.path.abspath(__file__))
# مسیر فایل .env
env_path = os.path.join(current_dir, '.env')

# بارگذاری فایل .env از مسیر مشخص شده
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("خطا: کلید API یافت نشد!")
    sys.exit(1)

try:
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"خطا در تنظیم API: {str(e)}")
    sys.exit(1)

class AnimatedLabel(customtkinter.CTkLabel):
    def __init__(self, master, text, font, fixed_width=300, **kwargs):
        super().__init__(
            master,
            text="",
            font=font,
            width=fixed_width,
            wraplength=fixed_width - 20,
            justify='right',
            anchor='e',
            corner_radius=10,
            fg_color='#1A1A1A',
            padx=10,
            pady=10,
            **kwargs
        )
        self.full_text = text
        self.displayed_text = ""
        self.update_text()

    def update_text(self):
        if len(self.displayed_text) < len(self.full_text):
            self.displayed_text += self.full_text[len(self.displayed_text)]
            self.configure(text=self.displayed_text)
            self.after(25, self.update_text)


class LoadingAnimation(customtkinter.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="", **kwargs)
        self.size = 20
        self.max_size = 30
        self.min_size = 20
        self.is_growing = True
        self.animate()

    def animate(self):
        if self.is_growing:
            self.size += 1
            if self.size >= self.max_size:
                self.is_growing = False
        else:
            self.size -= 1
            if self.size <= self.min_size:
                self.is_growing = True

        self.configure(text="●", font=("Arial", self.size))
        self.after(100, self.animate)


class Window(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x1200')

        try:
            if ctypes.windll.shell32.IsUserAnAdmin():
                adapter = get_active_adapter()
                if adapter:
                    change_dns(adapter)
            else:
                if sys.platform.startswith('win'):
                    ctypes.windll.shell32.ShellExecuteW(
                        None,
                        "runas",
                        sys.executable,
                        " ".join(sys.argv),
                        None,
                        1
                    )
        except Exception as e:
            print(f"خطا در تنظیم DNS: {str(e)}")
            pass  # ادامه اجرای برنامه حتی در صورت خطا در DNS

        self.model = genai.GenerativeModel('gemini-2.0-flash')

        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 2048,
        }

        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

        self.chat = self.model.start_chat(history=[])

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=8)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, rowspan=3, sticky='news')
        self.sidebar.close_sidebar_btn.configure(command=self.closeSidebar)

        self.topbar = TopBar(self)
        self.topbar.grid(row=0, column=1, sticky='nsew', padx=0)
        self.topbar.grid_remove()
        self.topbar.openSidebar.configure(command=self.openSidebar)

        self.convercation_side = Conversation(self)
        self.convercation_side.grid(row=1, column=1, sticky='news')

        self.user_input = User_input(self)
        self.user_input.grid(row=2, column=1, sticky='we')
        self.user_input.send_message_btn.configure(command=self.send_message)

        self.sidebar.newchat_btn.configure(command=self.new_chat)
        self.sidebar.newchatSmall_btn.configure(command=self.new_chat)

        self.active_adapter = self.get_active_adapter()
        self.bind("<Button-1>", self.on_window_click)

    def get_active_adapter(self):
        c = wmi.WMI()
        ethernet_active = None
        wifi_active = None
        for nic in c.Win32_NetworkAdapter():
            if nic.NetConnectionID and nic.NetConnectionStatus == 2:
                if nic.NetConnectionID.lower() == "ethernet":
                    ethernet_active = nic.NetConnectionID
                elif nic.NetConnectionID.lower() in ("wi-fi", "wifi"):
                    wifi_active = nic.NetConnectionID
        return ethernet_active if ethernet_active else wifi_active

    def enable_dns(self):
        try:
            script_path = os.path.join(os.path.dirname(__file__), 'dns_changer.py')
            subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در اجرای اسکریپت تغییر DNS:\n{str(e)}")

    def closeSidebar(self):
        self.sidebar.grid_remove()
        self.topbar.grid()
        self.convercation_side.grid(row=1, column=0, columnspan=2, sticky='news')
        self.user_input.grid(row=2, column=0, columnspan=2, sticky='news')

    def openSidebar(self):
        self.sidebar.grid()
        self.topbar.grid_remove()
        self.convercation_side.grid(row=1, column=1, sticky='news')
        self.user_input.grid(row=2, column=1, sticky='we')

    def get_ai_response(self, user_message):
        try:
            response = self.chat.send_message(
                user_message,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"متاسفانه خطایی رخ داد: {str(e)}"

    def send_message(self):
        text = self.user_input.user_text_input.get("1.0", "end-1c").strip()
        if text:
            self.convercation_side.add_message(text, is_user=True)
            self.user_input.user_text_input.delete("1.0", "end")

            self.loading_animation = LoadingAnimation(self.convercation_side)
            self.loading_animation.grid(row=self.convercation_side.current_row, column=0, pady=15, padx=75, sticky='nw')
            self.convercation_side.current_row += 1
            threading.Thread(target=self.process_response, args=(text,), daemon=True).start()

    def process_response(self, user_message):
        response = self.get_ai_response(user_message)
        self.after(0, self.display_response, response)

    def display_response(self, response):
        if hasattr(self, 'loading_animation'):
            self.loading_animation.destroy()
            self.convercation_side.current_row -= 1
        self.convercation_side.add_message(response, is_user=False)

    def on_window_click(self, event):
        if event.widget != self.user_input.user_text_input:
            self.user_input.on_frame_click(event)

    def new_chat(self):
        self.chat = self.model.start_chat(history=[])
        self.user_input.user_text_input.delete("1.0", "end")
        self.convercation_side.clear_messages()


if __name__ == '__main__':
    window = Window()

    #  مسیر آیکون برای حالت اجرا + حالت exe با PyInstaller
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, 'teksan.ico')
    else:
        icon_path = os.path.join(os.path.dirname(__file__), 'teksan.ico')

    window.iconbitmap(icon_path)
    window.title("تِک سان")
    window.mainloop()
