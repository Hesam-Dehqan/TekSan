import customtkinter
from PIL import Image
import os
import sys

def resource_path(relative_path):
    try:
        # وقتی برنامه به صورت .exe اجرا میشه توسط PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # وقتی به صورت عادی اجرا میشه
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Options_files(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.configure(fg_color='#545454')

        # مسیر پوشه icons
        icons_dir = resource_path(os.path.join('icons'))

        self.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.grid_rowconfigure(0, weight=2)

        # Images
        self.pdf_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'pdf.png')), 
            size=(25, 25)
        )
        self.imageFile_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'picture.png')), 
            size=(25, 25)
        )
        self.audioFile_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'audio.png')), 
            size=(25, 25)
        )
        self.voice_chat_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'audio (2).png')), 
            size=(25, 25)
        )
        self.video_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'video-message.png')), 
            size=(25, 25)
        )
        self.textFile_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_dir, 'text.png')), 
            size=(25, 25)
        )

        # دکمه‌ها
        self.pdf_translate = customtkinter.CTkButton(self,
                                                     height=50,
                                                     corner_radius=10,
                                                     border_width=0,
                                                     border_color='gray',
                                                     hover_color='#708090',
                                                     text="PDF ترجمه ی",
                                                     font=customtkinter.CTkFont("Vazir", size=15),
                                                     anchor="e",
                                                     fg_color='transparent',
                                                     compound='right',
                                                     image=self.pdf_image,
                                                     command=lambda: self.set_border_color(self.pdf_translate)
                                                     )

        self.Text_file_analysis = customtkinter.CTkButton(self,
                                                          height=50,
                                                          corner_radius=10,
                                                          border_width=0,
                                                          border_color='gray',
                                                          hover_color='#708090',
                                                          text='فایل های متنی',
                                                          font=customtkinter.CTkFont("Vazir", size=18),
                                                          anchor="e",
                                                          compound='right',
                                                          image=self.textFile_image,
                                                          fg_color='transparent',
                                                          command=lambda: self.set_border_color(self.Text_file_analysis)
                                                          )

        self.imageAndVideo_file_analysis = customtkinter.CTkButton(self,
                                                                   height=50,
                                                                   corner_radius=10,
                                                                   border_width=0,
                                                                   border_color='gray',
                                                                   hover_color='#708090',
                                                                   text='عکس',
                                                                   compound='right',
                                                                   image=self.imageFile_image,
                                                                   font=customtkinter.CTkFont("Vazir", size=18),
                                                                   anchor="e",
                                                                   fg_color='transparent',
                                                                   command=lambda: self.set_border_color(self.imageAndVideo_file_analysis)
                                                                   )

        self.audio_file_analysis = customtkinter.CTkButton(self,
                                                           height=50,
                                                           corner_radius=10,
                                                           border_width=0,
                                                           border_color='gray',
                                                           hover_color='#708090',
                                                           text='آنالیز فایل‌های صوتی',
                                                           font=customtkinter.CTkFont("Vazir", size=18),
                                                           anchor="e",
                                                           compound='right',
                                                           image=self.audioFile_image,
                                                           fg_color='transparent',
                                                           command=lambda: self.set_border_color(self.audio_file_analysis)
                                                           )

        self.voice_chat = customtkinter.CTkButton(self,
                                                  height=50,
                                                  corner_radius=10,
                                                  border_width=0,
                                                  border_color='gray',
                                                  hover_color='#708090',
                                                  text='گفت‌وگوی صوتی',
                                                  font=customtkinter.CTkFont("Vazir", size=18),
                                                  anchor="e",
                                                  compound='right',
                                                  image=self.voice_chat_image,
                                                  fg_color='transparent',
                                                  command=lambda: self.set_border_color(self.voice_chat)
                                                  )
        self.videoChat = customtkinter.CTkButton(self,
                                                 height=50,
                                                 corner_radius=10,
                                                 border_width=0,
                                                 border_color='gray',
                                                 hover_color='#708090',
                                                 text='ویدئو',
                                                 font=customtkinter.CTkFont("Vazir", size=18),
                                                 anchor="e",
                                                 compound='right',
                                                 image=self.video_image,
                                                 fg_color='transparent',
                                                 command=lambda: self.set_border_color(self.videoChat)
                                                 )

        # قرار دادن دکمه‌ها در گرید
        self.voice_chat.grid(row=0, column=0, padx=0, pady=0, sticky='we')
        self.Text_file_analysis.grid(row=0, column=1, padx=0, pady=0, sticky='we')
        self.imageAndVideo_file_analysis.grid(row=0, column=2, padx=0, pady=0, sticky='we')
        self.audio_file_analysis.grid(row=0, column=3, padx=0, pady=0, sticky='we')
        self.pdf_translate.grid(row=0, column=4, padx=0, pady=0, sticky='we')
        self.videoChat.grid(row=0, column=5, padx=0, pady=0, sticky='we')

    def set_border_color(self, clicked_button):
        # بازنشانی حاشیهٔ همهٔ دکمه‌ها
        for button in [self.pdf_translate, self.Text_file_analysis, self.imageAndVideo_file_analysis,
                       self.audio_file_analysis, self.voice_chat, self.videoChat]:
            button.configure(border_width=0)

        # تنظیم حاشیهٔ دکمهٔ کلیک‌شده
        clicked_button.configure(border_width=2, border_color='blue')
