
import random
import tkinter as tk
from tkinter import messagebox, Canvas
from PIL import Image, ImageTk
import requests
from io import BytesIO

def start_game():
    global lives, marbles_label, guess_var, hand_canvas, hand_closed, hand_open, marbles_list, guess_choice
    lives = 3
    guess_choice = None
    update_lives()
    generate_marbles()

def generate_marbles():
    global marbles, marbles_list
    marbles = random.randint(0, 10)
    hand_canvas.itemconfig(hand_closed, image=hand_closed_img)  # Show closed hand
    hand_canvas.itemconfig(hand_open, image="")  # Hide open hand
    for marble in marbles_list:
        hand_canvas.delete(marble)  # Remove previous marbles
    marbles_list = []
    marbles_label.config(text="")

def check_guess():
    global lives, guess_choice
    guess_choice = guess_var.get()
    
    hand_canvas.itemconfig(hand_closed, image="")  # Hide closed hand
    hand_canvas.itemconfig(hand_open, image=hand_open_img)  # Show open hand
    marbles_label.config(text=f"The hand reveals {marbles} marbles.")
    
    # Display marbles in the open hand
    x_start, y_start = 130, 160
    for i in range(marbles):
        marble = hand_canvas.create_oval(x_start, y_start, x_start + 15, y_start + 15, fill="darkgreen", outline="black")
        marbles_list.append(marble)
        x_start += 20
        if x_start > 180:
            x_start = 130
            y_start += 20
    
    if (marbles % 2 == 0 and guess_choice == "Even") or (marbles % 2 != 0 and guess_choice == "Odd"):
        messagebox.showinfo("Result", "Correct! You survive this round.")
    else:
        lives -= 1
        update_lives()
        if lives == 0:
            messagebox.showerror("Game Over", "You are eliminated... GAME OVER.")
            root.quit()
        else:
            messagebox.showwarning("Wrong", f"Wrong! Lives remaining: {lives}")
    generate_marbles()

def update_lives():
    lives_label.config(text=f"Lives: {lives}")

def load_image_from_url(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Check if request was successful
        image_data = Image.open(BytesIO(response.content))
        return ImageTk.PhotoImage(image_data)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Image Load Error", f"Failed to load image: {e}")
        return None

root = tk.Tk()
root.title("Squid Game: Marbles")
root.geometry("400x500")

title_label = tk.Label(root, text="SQUID GAME: MARBLES", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

lives_label = tk.Label(root, text="Lives: 3", font=("Arial", 12))
lives_label.pack()

hand_canvas = Canvas(root, width=300, height=300, bg="white")
hand_canvas.pack(pady=10)

# Load hand images from URL
hand_closed_img = load_image_from_url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlxeMNgcxUjf2vBET1sLp6rGZ94nNx2LF3qQ&s")
hand_open_img = load_image_from_url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTanOFr1SdOF7g6EqS_YyAWVu9U-Lpq0w-GlQ&s")

hand_closed = hand_canvas.create_image(150, 150, image=hand_closed_img if hand_closed_img else "")
hand_open = hand_canvas.create_image(150, 150, image=hand_open_img if hand_open_img else "")

marbles_list = []
marbles_label = tk.Label(root, text="", font=("Arial", 12))
marbles_label.pack()

guess_var = tk.StringVar(value="Odd")

def update_guess():
    global guess_choice
    guess_choice = guess_var.get()

odd_button = tk.Radiobutton(root, text="Odd", variable=guess_var, value="Odd", font=("Arial", 12), command=update_guess)
odd_button.pack()

even_button = tk.Radiobutton(root, text="Even", variable=guess_var, value="Even", font=("Arial", 12), command=update_guess)
even_button.pack()

guess_button = tk.Button(root, text="Submit Guess", command=check_guess, font=("Arial", 12))
guess_button.pack(pady=10)

start_game()

root.mainloop()