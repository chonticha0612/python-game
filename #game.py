from tkinter import *
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Tk, Button, Label, Toplevel, Frame, Entry
from PIL import ImageFont
import random
import time

class Game:
    def __init__(self):
        # Initialize game state
        self.window = tk.Tk()
        bgimg = tk.PhotoImage(file = "/Users/jelly/Downloads/new_bg.png")
        limg= Label(self.window, i=bgimg)
        limg.pack()
        self.window.title("Game Tai Si Ja Nong Sao")
        self.window.geometry("1440x990")
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.words_dict = {
            "prayut": {"category": "นายกในดวงใจ", "hints": ["สุดหล่อปี 57", "รักนะเลขาตู่", "ตัวตึงองค์มนตรี"]},
            "pravit": {"category": "คุณลุงในดวงใจ", "hints": ["นาฬิกาเพื่อน", "ลองนายก", "เรื่องปฏิวัติผมไม่เกี่ยวข้อง"]},
            "anutin": {"category": "คุณหมอในดวงใจ", "hints": ["โควิดกระจอก", "ภูมิใจดูด", "สารหนู"]},
            "newyear": {"category": "วันสำคัญ", "hints": ["วันปีใหม่"]}
        }
        self.custom_font_path = "/Users/jelly/Downloads/Joti_One/JotiOne-Regular.ttf"
        self.custom_font_title_path = "/Users/jelly/Downloads/Luckiest_Guy/LuckiestGuy-Regular.ttf"
        custom_font_size = 16 
        
        
        
        
        try:
            self.custom_font_title = ImageFont.truetype(self.custom_font_title_path, custom_font_size)
            self.custom_font = ImageFont.truetype(self.custom_font_path, custom_font_size)
            print("22")
        except IOError:
            print("11")
            print(f"Error: Unable to load font from {self.custom_font_path} or {self.custom_font_title_path}")
            self.custom_font_title = font.Font(size=custom_font_size, family="TkDefaultFont")
            self.custom_font = font.Font(size=custom_font_size, family="TkTitleFont")
            
        self.words = list(self.words_dict.keys())
        self.secret_word, self.clue = self.get_new_secret_word()

        # Create frames for different pages
        self.start_frame = Frame(self.window)   
        self.start_frame.pack()
        

        self.game_frame = Frame(self.window,bg="red")
        self.game_frame.pack_forget()
        
        self.name_frame = Frame(self.window)  
        self.name_frame.pack_forget()

        self.how_to_play_game_frame = Frame(self.window)
        self.how_to_play_game_frame.pack_forget()
        
        self.finish_game_frame = Frame(self.window)
        self.finish_game_frame.pack_forget()
        
        image = Image.open("/Users/jelly/Downloads/new_bg.png")
        self.bg = ImageTk.PhotoImage(image)
        canvas = Canvas(self.window)
        canvas.create_image(0, 0, anchor="nw", image=self.bg)
        canvas.pack()
        
        
        

        start_title = Label(canvas, text="WHAT\nWORLD", font=(self.custom_font_title, 100), fg="#F4C908", bg="#0D68EF", bd=10, relief="solid")
        start_label = Label(canvas, text="เกมส์ทายคำศัพท์", font=(self.custom_font_title, 50), fg="#FFFFFF", bg="#4dcbfe", )
        start_title.pack(side=TOP,pady=100,padx=300)
        start_label.pack(padx=24,pady=(24,0))
        start_button = Button(canvas, text="Start Game", font=(self.custom_font_title, 50), command=self.show_name_page)
        start_button.pack(padx=24,pady=(150,0))
       
        


        # Initialize GUI components for start frame
        
        
        #start frame
        start_title = Label(self.start_frame, text="WHAT\nWORLD", font=(self.custom_font_title, 100), fg="#F4C908", bg="#0D68EF", bd=10, relief="solid")
        start_label = Label(self.start_frame, text="เกมส์ทายคำศัพท์", font=(self.custom_font_title, 50), fg="#FFFFFF", bg="#4dcbfe", )
        start_title.pack(side=TOP,pady=100,padx=300)
        start_label.pack(padx=24,pady=(24,0))
        start_button = Button(self.start_frame, text="Start Game", font=(self.custom_font_title, 50), command=self.show_name_page)
        start_button.pack(padx=24,pady=(150,0))
        
        #nameframe
        name = Label(self.name_frame, text="ชื่อของคุณ", font=(self.custom_font_title, 50), fg="#F4C908", bg="#0D68EF", bd=10, relief="solid",border=1,justify='center')
        name.pack(side="top",pady=36,padx=24)
        self.textentry = Entry(self.name_frame, width=5, borderwidth=1, font=("Arial", 50), justify="center")
        self.textentry.pack()
        save_button = Button(self.name_frame, text="Save", command=self.show_how_to_play_game_page)
        save_button.pack(pady=(0,12))
       
        #how_to_play_frame
        how_to_play_label = Label(self.how_to_play_game_frame, text="- ทายภาพเป็นประโยคให้ถูกต้อง\n- 5 คำถาม\n-กด Play เพื่อเริ่มตอบคำถาม", font=(self.custom_font_title, 27), fg="#F4C908", bg="#0D68EF",justify='center')
        how_to_play_label.pack(side="top")
        
        play_button = Button(self.how_to_play_game_frame, text="Play", command=self.show_game_page)
        play_button.pack(padx=24,pady=(0.24))

        restart_button = Button(self.finish_game_frame, text="เริ่มใหม่", command=self.show_start_page)
        restart_button.pack()
        # Initialize GUI components for game frame
        
        self.game_finished = False
        self.score = 0
        self.lives = 5
        # Comes from Tkinter
        self.status_str = StringVar() 
        self.status_str.set("Score : " + str(self.score) + " | " + "Lives : " + "❤" * self.lives)
        show_status = Label(self.game_frame, textvariable=self.status_str)
        show_status.pack(pady=20)
        
        self.category_str = StringVar()
        self.category_str.set(self.words_dict[self.secret_word]["category"])
        show_category = Label(self.game_frame, textvariable=self.category_str, font=("Arial", 28))
        show_category.pack(pady=10)

        self.clue_str = StringVar()
        self.clue_str.set(" | ".join(self.clue))
        show_clue = Label(self.game_frame, textvariable=self.clue_str, font=("Arial", 50))
        show_clue.pack(padx=10, pady=30)

        # Display hints
        hints = self.words_dict[self.secret_word]["hints"]
        hint_text = StringVar()
        hint_text.set("Hints")
        self.hints_str = StringVar()
        self.hints_str.set("\n".join(hints))
        show_hint_text = Label(self.game_frame, textvariable=hint_text, font=("Arial Bold", 28))
        show_hint_text.pack()
        show_hints = Label(self.game_frame, textvariable=self.hints_str, font=("Arial", 28))
        show_hints.pack(pady=10)

        # Text entry widget
        self.textentry = Entry(self.game_frame, width=5, borderwidth=1, font=("Arial", 50), justify="center")
        self.textentry.pack()

        # Submit button
        submit_btn = Button(self.game_frame, text="Submit", command=self.update_screen)
        submit_btn.pack()

        self.run()

    def get_new_secret_word(self):
        random.shuffle(self.words)
        secret_word = self.words.pop()
        clue = list("?" * len(secret_word))
        return secret_word, clue

    def update_score_display(self):
        self.status_str.set("Score : " + str(self.score) + " | " + "Lives : " + "❤" * self.lives)
        
    def open_modal(self,result):
        modal = Toplevel(self.game_frame)
        modal.title("Modal Dialog")
        if(result == "win"): 
            modal_label = Label(modal, text="I want More")
            modal_label.pack(padx=10, pady=10)
            close_button = Button(modal, text="Next", command=lambda: [self.show_finish_game_page(), modal.destroy()])
            close_button.pack(pady=10)
        else:
            modal_label_lose = Label(modal, text="you lose")
            modal_label_lose.pack(padx=10, pady=10)
            close_button = Button(modal, text="restart", command=lambda: [self.show_game_page(), modal.destroy()])
            close_button.pack(pady=10)
            
        game_frame_x = self.game_frame.winfo_rootx()
        game_frame_y = self.game_frame.winfo_rooty()
        game_frame_width = self.game_frame.winfo_width()
        game_frame_height = self.game_frame.winfo_height()

        modal_width = 200  # Adjust this value based on the desired width of the modal
        modal_height = 100  # Adjust this value based on the desired height of the modal

        x_position = game_frame_x + (game_frame_width - modal_width) // 2
        y_position = game_frame_y + (game_frame_height - modal_height) // 2

        # Set the geometry of the modal window
        modal.geometry(f"{modal_width}x{modal_height}+{x_position}+{y_position}")

    def update_screen(self):
        guess = self.textentry.get().strip().lower()
        if guess == self.secret_word:
            if len(self.words) >= 1:
                self.score += 1
                self.update_score_display()
                print("เย้ คำนั้นก็คือ : " + self.secret_word)
                self.clue_str.set("ทายถูกแล้ว : " + self.secret_word)
                self.game_frame.update()
                time.sleep(0.3)

            if len(self.words) < 1:
                self.game_finished = True
                self.clue_str.set("Congrats!")
                self.result = "win"
                self.open_modal(self.result)
            else:
                self.secret_word, self.clue = self.get_new_secret_word()
                self.category_str.set(self.words_dict[self.secret_word]["category"])
                self.clue_str.set(" | ".join(self.clue))
                self.hints = self.words_dict[self.secret_word]["hints"]
                self.hints_str.set("\n".join(self.hints))
        else:
            print("ผิด! เลือดลด")
            self.lives -= 1
            self.update_score_display()
            self.game_frame.update()
            if self.lives < 1:
                self.clue_str.set("ควายแพ้ โง่")
                self.result = "lose"
                self.open_modal(self.result)
                self.game_finished = True

        self.textentry.delete(0, "end")

    def main(self):
        if not self.game_finished:
            self.window.after(10, self.main)
        else:
            print("Quitting...")

    def run(self):
        self.window.mainloop()

    def show_start_page(self):
        self.game_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.start_frame.pack()

    def show_game_page(self):
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.game_frame.pack()
        
    def show_name_page(self):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.name_frame.pack()
    
    def show_how_to_play_game_page(self):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.how_to_play_game_frame.pack()
    
    def show_finish_game_page(self):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack()

if __name__ == "__main__":
    game = Game()
