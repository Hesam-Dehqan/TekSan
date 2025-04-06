import customtkinter
from PIL import Image
import os
import sys
from option_files import Options_files
from convercation import Conversation

# تابع امن برای مدیریت مسیرها در حالت exe و اجرا عادی
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class User_input(customtkinter.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.var = 1
        self.convercation = Conversation(self)
        self.is_focused = False

        # مسیر پوشه آیکون‌ها
        icons_dir = resource_path('icons')

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.off_searchThe_web_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'web_black.png')), 
            size=(35, 35)
        )
        self.on_searchThe_web_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'web.png')), 
            size=(35, 35)
        )
        self.send_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'send.png')), 
            size=(35, 35)
        )
        self.moreOption_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'option.png'))
        )

        self.optionbar = Options_files(self)
        self.optionbar.grid(row=0, column=0, columnspan=4, sticky='we', pady=0, padx=0)

        self.user_text_input = customtkinter.CTkTextbox(
            self,
            height=100,
            width=300,
            scrollbar_button_color='yellow',
            scrollbar_button_hover_color='#FF7F00',
            font=customtkinter.CTkFont('Vazir', size=18)
        )
        self.user_text_input.grid(row=1, column=1, rowspan=2, sticky='news', padx=5, pady=5)

        self.search_theWeb = customtkinter.CTkButton(
            self,
            text='',
            image=self.off_searchThe_web_image,
            fg_color='transparent',
            hover_color='#708090',
            width=35,
            command=self.On_search_the_web
        )
        self.search_theWeb.grid(row=2, column=0, sticky='news', padx=5, pady=5)

        self.more_option = customtkinter.CTkButton(
            self,
            text='',
            image=self.moreOption_image,
            fg_color='transparent',
            hover_color='#708090',
            width=35
        )
        self.more_option.grid(row=1, column=0, sticky='news', padx=5, pady=5)

        self.send_message_btn = customtkinter.CTkButton(
            self,
            text='',
            image=self.send_image,
            fg_color='transparent',
            hover_color='#708090',
            width=35
        )
        self.send_message_btn.grid(row=1, column=2, sticky='ns', padx=5, pady=0)

        self.user_text_input.bind("<Button-1>", self.on_textbox_click)
        self.bind("<Button-1>", self.on_frame_click)

    def On_search_the_web(self):
        self.var += 1
        if self.var % 2 == 0:
            self.search_theWeb.configure(image=self.on_searchThe_web_image)
        else:
            self.search_theWeb.configure(image=self.off_searchThe_web_image)

    def on_textbox_click(self, event):
        if not self.is_focused:
            self.is_focused = True
            self.user_text_input.configure(border_width=2, border_color='yellow')
        event.widget.focus_set()
        return "break"

    def on_frame_click(self, event):
        if event.widget != self.user_text_input and self.is_focused:
            self.is_focused = False
            self.user_text_input.configure(border_width=0)
