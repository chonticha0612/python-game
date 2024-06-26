from tkinter import *
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Tk, Button, Label, Toplevel, Frame, Entry
from PIL import ImageFont
from database import get_database_row
import random
import time


class Game:
    def __init__(self,database_dict):
        # Initialize game state
        self.window = tk.Tk()
        self.window.title("Game Tai Si Ja Nong Sao")
        self.window.geometry("1440x1024")
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.game_finished = False
        self.score = 0
        self.lives = 5
        self.database_dict = database_dict
        self.words_dict = {}
        for key, value in database_dict.items():
            self.words_dict[value['Ans_Num']] = {"category": value["Question"],"Ans_TH":value["Ans_TH"]}
        
        self.words = list(self.words_dict.items())
        self.secret_word,self.Question,self.Ans_TH = self.get_new_secret_word()
       
        # Create frames for different pages
        self.start_frame = Frame(self.window)   
        self.start_frame.pack()
        
        self.game_frame = Frame(self.window)
        self.game_frame.pack_forget()
        
        self.name_frame = Frame(self.window)  
        self.name_frame.pack_forget()

        self.how_to_play_game_frame = Frame(self.window)
        self.how_to_play_game_frame.pack_forget()
        
        self.finish_game_frame = Frame(self.window)
        self.finish_game_frame.pack_forget()
        
        self.lose_game_frame = Frame(self.window)
        self.lose_game_frame.pack_forget()
        
        
        # Create a canvas for the start frame
        self.canvas_start_frame = Canvas(self.start_frame, width=1440, height=1024)
        self.canvas_start_frame.pack()
        ##BG 
        image_bg = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg = image_bg.resize((width, height))
        # Convert image to PhotoImage object
        self.tk_image_bg = ImageTk.PhotoImage(image_bg)
        self.canvas_start_frame.create_image(0,0,image=self.tk_image_bg,anchor=NW)
        
        
         # Load the second image and resize it
        image1 = Image.open("/Users/jelly/Downloads/The math2.png")
        # Resize the image to desired width and height
        width = 800
        height = 400
        image1 = image1.resize((width, height))
        self.tk_image1 = ImageTk.PhotoImage(image1)
        self.canvas_start_frame.create_image(300, 100, image=self.tk_image1, anchor=NW)
    
        # Load the second image and resize it
        button_play = Image.open("/Users/jelly/Downloads/play2.png")
        width = 400
        height = 100
        button_play = button_play.resize((width, height))
        self.tk_button_play = ImageTk.PhotoImage(button_play)
        self.button_play_id= self.canvas_start_frame.create_image(500, 600, image=self.tk_button_play, anchor=NW)
        self.canvas_start_frame.tag_bind(self.button_play_id, "<Button-1>", self.show_name_page)
        
        
        
        # Create a canvas for the name frame
        self.canvas_name_frame = Canvas(self.name_frame, width=1440, height=1024)
        self.canvas_name_frame.pack()
        ##BG 
        image_bg2 = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg2 = image_bg.resize((width, height))
        # Convert image to PhotoImage object
        self.tk_image_bg2 = ImageTk.PhotoImage(image_bg2)
        self.canvas_name_frame.create_image(0,0,image=self.tk_image_bg2,anchor=NW)
        
        # Create the Entry widget directly on self.canvas_bg
        name = Image.open("/Users/jelly/Downloads/name.png")
        # Resize the image to desired width and height
        width = 800
        height = 400
        name = name.resize((width, height))
        self.tk_name = ImageTk.PhotoImage(name)
        self.canvas_name_frame.create_image(300, 100, image=self.tk_name, anchor=NW)
        
        self.textentry = Entry(self.canvas_name_frame,width=15,  font=("Arial", 50), justify="center", highlightbackground="#ff944d")
        self.canvas_name_frame.create_window(700, 350, anchor=CENTER, window=self.textentry)
    
        
    
        save_button = Image.open("/Users/jelly/Downloads/save_button.png")
        width = 400
        height = 100
        save_button = save_button.resize((width, height))
        self.tk_save_button = ImageTk.PhotoImage(save_button)
        self.save_button_id= self.canvas_name_frame.create_image(700, 700, image=self.tk_save_button, anchor=CENTER,state="hidden")
        self.canvas_name_frame.tag_bind(self.save_button_id, "<Button-1>", self.show_how_to_play_game_page)
        
        def validate_entry(event=None):
            if len(self.textentry.get()) > 0:
                 self.canvas_name_frame.itemconfig(self.save_button_id, state="normal")
            else:
                 self.canvas_name_frame.itemconfig(self.save_button_id, state="hidden")
        self.textentry.bind("<KeyRelease>", validate_entry)
        
        # Create a canvas for the how to play frame
        self.canvas_how_to_play_frame = Canvas(self.how_to_play_game_frame, width=1440, height=1024)
        self.canvas_how_to_play_frame.pack()
        ##BG 
        image_bg3 = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg3 = image_bg.resize((width, height))
        # Convert image to PhotoImage object
        self.tk_image_bg3 = ImageTk.PhotoImage(image_bg3)
        self.canvas_how_to_play_frame.create_image(0,0,image=self.tk_image_bg3,anchor=NW)
        
        how_to_play = Image.open("/Users/jelly/Downloads/how_to_play2.png")
        # Resize the image to desired width and height
        width = 100
        height = 100
        image1 = image1.resize((width, height))
        self.tk_how_to_play = ImageTk.PhotoImage(how_to_play)
        self.canvas_how_to_play_frame.create_image(140, 50, image=self.tk_how_to_play, anchor=NW)

        save_button1= Image.open("/Users/jelly/Downloads/start.png")
        width = 400
        height = 100
        save_button1 = save_button1.resize((width, height))
        self.tk_save_button1 = ImageTk.PhotoImage(save_button1)
        self.save_button1_id= self.canvas_how_to_play_frame.create_image(700, 700, image=self.tk_save_button1, anchor=CENTER)
        self.canvas_how_to_play_frame.tag_bind(self.save_button1_id, "<Button-1>", self.show_game_page)
       
         # Create a canvas for the game frame
        self.canvas_game_frame = Canvas(self.game_frame, width=1440, height=1024)
        self.canvas_game_frame.pack()
        ##BG 
        image_bg4 = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg4 = image_bg.resize((width, height))
        # Convert image to PhotoImage object
        self.tk_image_bg4 = ImageTk.PhotoImage(image_bg4)
        self.canvas_game_frame.create_image(0,0,image=self.tk_image_bg4,anchor=NW)
        
        text_score = Image.open("/Users/jelly/Downloads/Score3.png")
        # Resize the image to desired width and height
        width = 100
        height = 50
        text_score = text_score.resize((width, height))
        self.tk_text_score = ImageTk.PhotoImage(text_score)
        self.canvas_game_frame.create_image(450, 20, image=self.tk_text_score, anchor=NW)
        
        score = Image.open("/Users/jelly/Downloads/box_empty.png")
        # Resize the image to desired width and height
        width = 100
        height = 50
        score = score.resize((width, height))
        self.tk_score = ImageTk.PhotoImage(score)
        self.canvas_game_frame.create_image(570, 20, image=self.tk_score, anchor=NW)
        
        heart = Image.open("/Users/jelly/Downloads/heart.png")
        # Resize the image to desired width and height
        width = 100
        height = 50
        heart = heart.resize((width, height))
        self.tk_heart = ImageTk.PhotoImage(heart)
        self.canvas_game_frame.create_image(750, 20, image=self.tk_heart, anchor=NW)
        
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_lives = self.canvas_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_score1 = self.canvas_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)
        frame = Image.open("/Users/jelly/Downloads/Frame 6525.png")
        # Resize the image to desired width and height
        width = 1200
        height = 500
        frame = frame.resize((width, height))
        self.tk_frame = ImageTk.PhotoImage(frame)
        self.canvas_game_frame.create_image(110, 100, image=self.tk_frame, anchor=NW)
        self.Question_str = StringVar()
        self.Question_str.set(self.Question)
        
        self.text_input = Entry(self.canvas_game_frame, width=15, font=("Arial", 50), justify="center", highlightbackground="#ff944d")
        self.canvas_game_frame.create_window(700, 350, anchor=CENTER, window=self.text_input)

        submit_button = Image.open("/Users/jelly/Downloads/submit.png")
        width = 400
        height = 100
        submit_button = submit_button.resize((width, height))
        self.tk_submit_button = ImageTk.PhotoImage(submit_button)
        self.submit_button_id = self.canvas_game_frame.create_image(700, 700, image=self.tk_submit_button, anchor=CENTER, state="hidden")
        self.canvas_game_frame.tag_bind(self.submit_button_id, "<Button-1>", self.update_screen)

        def validate_entry2(event=None):
            if len(self.text_input.get()) > 0:
                self.canvas_game_frame.itemconfig(self.submit_button_id, state="normal")
            else:
                self.canvas_game_frame.itemconfig(self.submit_button_id, state="hidden")

        self.text_input.bind("<KeyRelease>", validate_entry2)
        self.len_Question = len(self.Question)
        text_x = 700
        text_y = 200
        text_content = self.Question
        text_font = ("Arial", 20)
        text_color = "black"
        self.text_object = self.canvas_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)

          # Create a canvas for the finish frame
    
        self.canvas_finish_game_frame = Canvas(self.finish_game_frame, width=1440, height=1024)
        self.canvas_finish_game_frame.pack()
        
        image_bg5 = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg5 = image_bg5.resize((width, height))
            # Convert image to PhotoImage object
        self.tk_image_bg5 = ImageTk.PhotoImage(image_bg5)
        self.canvas_finish_game_frame.create_image(0,0,image=self.tk_image_bg5,anchor=NW)
            
        text_score_finish = Image.open("/Users/jelly/Downloads/Score3.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        text_score_finish = text_score_finish.resize((width, height))
        self.tk_text_score_finish = ImageTk.PhotoImage(text_score_finish)
        self.canvas_finish_game_frame.create_image(450, 20, image=self.tk_text_score_finish, anchor=NW)
            
        score_finish = Image.open("/Users/jelly/Downloads/box_empty.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        score_finish = score_finish.resize((width, height))
        self.tk_score_finish = ImageTk.PhotoImage(score_finish)
        self.canvas_finish_game_frame.create_image(570, 20, image=self.tk_score_finish, anchor=NW)
            
        heart_finish = Image.open("/Users/jelly/Downloads/heart.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        heart_finish = heart_finish.resize((width, height))
        self.tk_heart_finish = ImageTk.PhotoImage(heart_finish)
        self.canvas_finish_game_frame.create_image(750, 20, image=self.tk_heart_finish, anchor=NW)
            
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_lives_finish = self.canvas_finish_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)
            
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_score_finish = self.canvas_finish_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)

        congrats = Image.open("/Users/jelly/Downloads/congrats.png")
            # Resize the image to desired width and height
        width = 1200
        height = 500
        congrats = congrats.resize((width, height))
        self.tk_congrats = ImageTk.PhotoImage(congrats)
        self.canvas_finish_game_frame.create_image(110, 100, image=self.tk_congrats, anchor=NW)
            
        home_button= Image.open("/Users/jelly/Downloads/home.png")
        width = 400
        height = 100
        home_button = home_button.resize((width, height))
        self.tk_home_button = ImageTk.PhotoImage(home_button)
        self.home_button_id= self.canvas_finish_game_frame.create_image(700, 700, image=self.tk_home_button, anchor=CENTER)
        self.canvas_finish_game_frame.tag_bind(self.home_button_id, "<Button-1>", self.show_start_page)
        
   
         # Create a canvas for the lose frame
        self.canvas_lose_game_frame = Canvas(self.lose_game_frame, width=1440, height=1024)
        self.canvas_lose_game_frame.pack()
        image_bg6 = Image.open("/Users/jelly/Downloads/bg1.png")
        width = 1445
        height = 900
        image_bg6 = image_bg6.resize((width, height))
            # Convert image to PhotoImage object
        self.tk_image_bg6 = ImageTk.PhotoImage(image_bg6)
        self.canvas_lose_game_frame.create_image(0,0,image=self.tk_image_bg6,anchor=NW)
        text_score_lose = Image.open("/Users/jelly/Downloads/Score3.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        text_score_lose = text_score_lose.resize((width, height))
        self.tk_text_score_lose = ImageTk.PhotoImage(text_score_lose)
        self.canvas_lose_game_frame.create_image(450, 20, image=self.tk_text_score_lose, anchor=NW)
        
        score_lose = Image.open("/Users/jelly/Downloads/box_empty.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        score_lose = score_lose.resize((width, height))
        self.tk_score_lose = ImageTk.PhotoImage(score_lose)
        self.canvas_lose_game_frame.create_image(570, 20, image=self.tk_score_lose, anchor=NW)
            
        heart_lose = Image.open("/Users/jelly/Downloads/heart.png")
            # Resize the image to desired width and height
        width = 100
        height = 50
        heart_lose = heart_lose.resize((width, height))
        self.tk_heart_lose = ImageTk.PhotoImage(heart_lose)
        self.canvas_lose_game_frame.create_image(750, 20, image=self.tk_heart_lose, anchor=NW)
            
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_lives_lose = self.canvas_lose_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)
            
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.text_score_lose = self.canvas_lose_game_frame.create_text(text_x, text_y, text=text_content, font=text_font, fill=text_color, anchor=CENTER)

        lose = Image.open("/Users/jelly/Downloads/lose.png")
            # Resize the image to desired width and height
        width = 1200
        height = 500
        lose = lose.resize((width, height))
        self.tk_lose = ImageTk.PhotoImage(lose)
        self.canvas_lose_game_frame.create_image(110, 100, image=self.tk_lose, anchor=NW)
        
          
        new_game= Image.open("/Users/jelly/Downloads/new_game.png")
        width = 400
        height = 100
        new_game = new_game.resize((width, height))
        self.tk_new_game = ImageTk.PhotoImage(new_game)
        self.new_game_id= self.canvas_lose_game_frame.create_image(500, 700, image=self.tk_new_game, anchor=CENTER)
        self.canvas_lose_game_frame.tag_bind(self.new_game_id, "<Button-1>", self.show_how_to_play_game_page)
            
        home_button1= Image.open("/Users/jelly/Downloads/home.png")
        width = 400
        height = 100
        home_button1 = home_button1.resize((width, height))
        self.tk_home_button1 = ImageTk.PhotoImage(home_button1)
        self.home_button1_id= self.canvas_lose_game_frame.create_image(950, 700, image=self.tk_home_button1, anchor=CENTER)
        self.canvas_lose_game_frame.tag_bind(self.home_button1_id, "<Button-1>", self.show_start_page)

        self.run()
        
    def reset_game(self):
        self.score = 0
        self.lives = 5  # You can set it to your initial lives value
        self.game_finished = False
        self.words_dict = {}  # Reset the words dictionary or reinitialize it with new words
        for key, value in self.database_dict.items():
            self.words_dict[value['Ans_Num']] = {"category": value["Question"], "Ans_TH": value["Ans_TH"]}
        self.secret_word, self.Question, self.Ans_TH = self.get_new_secret_word()
        self.update_question()
        print(self.secret_word)
        print(self.Question)


    def get_new_secret_word(self):
        secret_word = random.choice(list(self.words_dict.keys()))
        Question = self.words_dict[secret_word]["category"]
        Ans_TH = self.words_dict[secret_word]["Ans_TH"]
        del self.words_dict[secret_word]
     
      
        return secret_word, Question,Ans_TH
    
    def update_score_lose(self):
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_lose_game_frame.itemconfig(self.text_lives_lose, text=text_content)
         
        # self.canvas_game_frame.itemconfig(text_object, text=text_content)
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_lose_game_frame.itemconfig(self.text_score_lose, text=text_content)
    
    def update_score_finish(self):
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_finish_game_frame.itemconfig(self.text_lives_finish, text=text_content)
         
        # self.canvas_game_frame.itemconfig(text_object, text=text_content)
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_finish_game_frame.itemconfig(self.text_score_finish, text=text_content)
    
    def update_score_display(self):
        text_x = 785
        text_y = 45
        text_content = self.lives
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_game_frame.itemconfig(self.text_lives, text=text_content)
         
        # self.canvas_game_frame.itemconfig(text_object, text=text_content)
        text_x = 620
        text_y = 45
        text_content = self.score
        text_font = ("Arial", 30)
        text_color = "black"
        self.canvas_game_frame.itemconfig(self.text_score1, text=text_content)
        
    def update_question(self):
           
        text_content = self.Question
            
        self.canvas_game_frame.itemconfig(self.text_object, text=text_content)
        
        
        
    def reset_score_and_lives(self):
        self.score = 0
        self.lives = 5
        
    def update_screen(self,event=None):
        guess = self.text_input.get()
        self.secret_word = str(self.secret_word)
        if guess == self.secret_word or guess== self.Ans_TH:
            if len(self.words_dict) >= 1:
                self.score += 1
                self.update_score_display()
                self.game_frame.update()
                self.text_input.delete(0, "end")
                time.sleep(0.3)
                self.secret_word, self.Question,self.Ans_TH = self.get_new_secret_word()
                self.update_question()
                
            else:
                self.game_finished = True
                self.text_input.delete(0, "end")
                self.update_score_finish()
                self.show_finish_game_page()
                self.main()
                
                
                # self.12.set(self.words_dict[self.secret_word]["category"])
                
        else:
            self.lives -= 1
            self.update_score_display()
            if self.lives < 1:
                self.game_finished = True
                self.update_score_lose()
                self.show_lose_game_page()
                
        self.text_input.delete(0, "end")

   
    def check_game_status(self):
        if self.game_finished:
            # Reset the game or exit the application
            self.reset_game()  # You 
    
    def run(self):
         while True:
            self.check_game_status()
            self.update_score_display()
            self.window.update_idletasks()
            self.window.update()
        # self.window.mainloop()

    def show_start_page(self,event=None):
        self.game_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.lose_game_frame.pack_forget()
        self.start_frame.pack()

    def show_game_page(self,event=None):
        # self.reset_score_and_lives()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.lose_game_frame.pack_forget()
        self.game_frame.pack()
        self.text_input.focus_set()
        
    def show_name_page(self,event=None):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.lose_game_frame.pack_forget()
        self.name_frame.pack()
        self.textentry.focus_set()
    
    def show_how_to_play_game_page(self,event=None):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.lose_game_frame.pack_forget()
        self.how_to_play_game_frame.pack()
        
    def show_lose_game_page(self,event=None):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.finish_game_frame.pack_forget()
        self.lose_game_frame.pack()
        
    def show_finish_game_page(self,event=None):
        self.game_frame.pack_forget()
        self.start_frame.pack_forget()
        self.name_frame.pack_forget()
        self.how_to_play_game_frame.pack_forget()
        self.lose_game_frame.pack_forget()
        self.finish_game_frame.pack()

if __name__ == "__main__":
    database_row = get_database_row()  
    database_dict = {}
    for row in database_row:
        key = row[0] # ใช้ index เพื่อเข้าถึง 'Id'
        value = {
            'Question': row[1],  # ใช้ index เพื่อเข้าถึง 'Question'
            'Ans_Num': row[2],    # ใช้ index เพื่อเข้าถึง 'Answer'
            'Ans_TH': row[3]       
        }
        database_dict[key] = value
    game = Game(database_dict)
    # game.run()
    # game.reset_game()
    


 
    
    
