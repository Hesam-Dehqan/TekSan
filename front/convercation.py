import customtkinter
from customtkinter import CTk
from PIL import Image
import os
import sys

from option_files import Options_files
import tkinter as tk

# تابع ایمن برای پیدا کردن مسیر فایل در حالت فشرده‌شده (PyInstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AnimatedMessage(customtkinter.CTkLabel):
    def __init__(self, master, text, font, fixed_width=400, speed=25, **kwargs):
        super().__init__(
            master,
            text="",
            font=font,
            width=fixed_width,
            wraplength=fixed_width - 20,
            corner_radius=10,
            fg_color='#1A1A1A',
            text_color='white',
            padx=10,
            pady=10,
            **kwargs
        )
        self.fixed_width = fixed_width
        self.full_text = text
        self.displayed_text = ""
        self.speed = speed
        self.after(self.speed, self.update_text)

    def update_text(self):
        if len(self.displayed_text) < len(self.full_text):
            self.displayed_text += self.full_text[len(self.displayed_text)]
            display_text = self.displayed_text.replace('\n', '\n ')
            self.configure(text=display_text)
            self.after(self.speed, self.update_text)

class WelcomeMessage(customtkinter.CTkLabel):
    def __init__(self, master, text, font, fixed_width=500, **kwargs):
        super().__init__(
            master,
            text="",
            font=font,
            width=fixed_width,
            wraplength=fixed_width - 20,
            corner_radius=10,
            fg_color='transparent',
            text_color='#FFD700',
            padx=10,
            pady=10,
            **kwargs
        )
        self.fixed_width = fixed_width
        self.full_text = text
        self.displayed_text = ""
        self.cursor_visible = False
        self.after(75, self.update_text)

    def update_text(self):
        if len(self.displayed_text) < len(self.full_text):
            self.displayed_text += self.full_text[len(self.displayed_text)]
            display_text = self.displayed_text.replace('\n', '\n ')
            self.configure(text=display_text)
            self.after(75, self.update_text)
        else:
            self.blink_cursor()

    def blink_cursor(self):
        if self.cursor_visible:
            new_text = self.full_text + " "
            self.cursor_visible = False
        else:
            new_text = self.full_text + "_"
            self.cursor_visible = True
        display_text = new_text.replace('\n', '\n ')
        self.configure(text=display_text)
        self.after(500, self.blink_cursor)

class MessageContainer(customtkinter.CTkFrame):
    def __init__(self, master, message, is_user=False, is_welcome=False, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color='transparent')

        self.grid_columnconfigure(0, weight=1)

        if is_welcome:
            self.message = WelcomeMessage(
                self,
                text=message,
                font=customtkinter.CTkFont(family="Vazir", size=32),
                justify='center',
                anchor='center'
            )
            self.message.grid(row=0, column=0, pady=150, padx=75, sticky='nsew')
        else:
            if is_user:
                self.message = customtkinter.CTkLabel(
                    self,
                    text=message,
                    font=customtkinter.CTkFont(family="Vazir", size=20),
                    width=400,
                    wraplength=380,
                    justify='right',
                    anchor='e',
                    corner_radius=10,
                    fg_color='#2F4F4F',
                    text_color='white',
                    padx=10,
                    pady=10
                )
                self.message.grid(row=0, column=0, pady=5, padx=(400, 75), sticky='e')
            else:
                self.message = AnimatedMessage(
                    self,
                    text=message,
                    font=customtkinter.CTkFont(family="Vazir", size=20),
                    justify='left',
                    anchor='w',
                    speed=15
                )
                self.message.grid(row=0, column=0, pady=5, padx=(75, 400), sticky='w')

class TopBar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        kwargs["fg_color"] = 'transparent'
        kwargs["height"] = 50
        super().__init__(master, **kwargs)

        # مسیر آیکون‌ها با resource_path
        icons_dir = resource_path('icons')

        self.grid_columnconfigure(0, weight=0, minsize=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        self.openSidebar_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'arrow (1).png')),
            size=(20, 20)
        )

        self.userSidebar_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'profile.png')),
            size=(35, 35)
        )

        self.openSidebar = customtkinter.CTkButton(
            self,
            image=self.openSidebar_image,
            text='',
            fg_color='transparent',
            width=35,
            height=50,
            hover_color='',
            corner_radius=0
        )
        self.openSidebar.grid(row=0, column=0, sticky='nsw')

        self.user_btn = customtkinter.CTkButton(
            self,
            image=self.userSidebar_image,
            text='',
            font=customtkinter.CTkFont('Vazir', size=20, weight='bold'),
            fg_color='transparent',
            hover_color='#0F0F0F',
            compound='left',
            anchor="e",
            width=35,
            height=35
        )
        self.user_btn.grid(row=0, column=2, padx=15, pady=10, sticky='e')

class Conversation(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(width=self.winfo_screenwidth() - 180)

        self.messages = []
        self.current_row = 0

        self.grid_columnconfigure(0, weight=1)

        self.show_welcome_message()

    def show_welcome_message(self):
        try:
            self.add_message(f"{u'\U0001F916'} \n !سلام  \n چه کاری از دستم برمیاد؟؟", is_welcome=True)
        except Exception as e:
            print(f"خطا در نمایش پیام خوش‌آمدگویی: {str(e)}")
            self.add_message("سلام! چه کاری از دستم برمیاد؟", is_welcome=True)

    def add_message(self, message, is_user=False, is_welcome=False):
        try:
            message_container = MessageContainer(self, message, is_user, is_welcome)
            message_container.grid(row=self.current_row, column=0, sticky='ew')
            self.messages.append(message_container)
            self.current_row += 1
            self.after(100, self._scroll_to_bottom)
        except Exception as e:
            print(f"خطا در افزودن پیام: {str(e)}")

    def clear_messages(self):
        for message in self.messages:
            message.destroy()

        self.messages.clear()
        self.current_row = 0
        self.show_welcome_message()

    def _scroll_to_bottom(self):
        self._parent_canvas.yview_moveto(1.0)
