import customtkinter
from customtkinter import CTkButton
from PIL import Image
import os
import sys

# تابع ایمن برای دسترسی به مسیر فایل‌ها در حالت exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Sidebar(customtkinter.CTkFrame):
    _images = {}

    def __init__(self, master, width=250, **kwargs):
        super().__init__(master, **kwargs)

        self.width = width
        self.configure(width=self.width,
                       border_color='yellow',
                       fg_color='#0F0F0F',
                       corner_radius=0)

        icons_dir = resource_path('icons')

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0)
        self.grid_propagate(False)

        if not Sidebar._images:
            try:
                Sidebar._images = {
                    'close': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'arrow_left.png')),
                        size=(20, 20)),
                    'search': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'interface.png')),
                        size=(20, 20)),
                    'newchat_small': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'chat (2).png')),
                        size=(20, 20)),
                    'newchat': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'chat (1).png')),
                        size=(20, 20)),
                    'models': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'list (1).png')),
                        size=(20, 20)),
                    'settings': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'settings (1).png')),
                        size=(35, 35)),
                    'user': customtkinter.CTkImage(
                        Image.open(os.path.join(icons_dir, 'profile.png')),
                        size=(35, 35))
                }
            except Exception as e:
                print(f"خطا در بارگذاری تصاویر: {str(e)}")
                Sidebar._images = {}  # تنظیم یک دیکشنری خالی در صورت خطا

        self.close_sidebar_btn = CTkButton(self,
                                           image=Sidebar._images['close'],
                                           text='',
                                           fg_color='transparent',
                                           width=20,
                                           height=20,
                                           hover_color='#708090')
        self.close_sidebar_btn.grid(row=0, column=0, padx=(25, 5), pady=10, sticky="w")

        self.search_btn = customtkinter.CTkButton(self,
                                                  image=Sidebar._images['search'],
                                                  text='',
                                                  fg_color='transparent',
                                                  width=20,
                                                  height=20,
                                                  hover_color='#708090')
        self.search_btn.grid(row=0, column=1, padx=5, pady=10)

        self.newchatSmall_btn = customtkinter.CTkButton(self,
                                                       image=Sidebar._images['newchat_small'],
                                                       text='',
                                                       fg_color='transparent',
                                                       width=20,
                                                       height=20,
                                                       hover_color='#708090')
        self.newchatSmall_btn.grid(row=0, column=2, padx=(5, 25), pady=10, sticky="e")

        self.newchat_btn = customtkinter.CTkButton(self,
                                                   image=Sidebar._images['newchat'],
                                                   text='گفت و گوی جدید',
                                                   font=customtkinter.CTkFont('Vazir', size=20, weight='bold'),
                                                   fg_color='transparent',
                                                   hover_color='#708090',
                                                   compound='left',
                                                   anchor="e")
        self.newchat_btn.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        self.models_btn = customtkinter.CTkButton(self,
                                                  image=Sidebar._images['models'],
                                                  text='مدل ها',
                                                  font=customtkinter.CTkFont('Vazir', size=20, weight='bold'),
                                                  fg_color='transparent',
                                                  hover_color='#708090',
                                                  compound='left',
                                                  anchor="e")
        self.models_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        self.setting_btn = customtkinter.CTkButton(self,
                                                   image=Sidebar._images['settings'],
                                                   text='',
                                                   font=customtkinter.CTkFont('Vazir', size=20, weight='bold'),
                                                   fg_color='transparent',
                                                   hover_color='#0F0F0F',
                                                   compound='left',
                                                   anchor="w")
        self.setting_btn.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        self.user_btn = customtkinter.CTkButton(self,
                                                image=Sidebar._images['user'],
                                                text='',
                                                font=customtkinter.CTkFont('Vazir', size=20, weight='bold'),
                                                fg_color='transparent',
                                                hover_color='#0F0F0F',
                                                compound='left',
                                                anchor="e")
        self.user_btn.grid(row=4, column=2, padx=10, pady=10, sticky='e')
