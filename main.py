import tkinter as tk
import random

# Initialize game window
root = tk.Tk()
root.title("Egg Catcher Game")
root.resizable(False, False)
canvas = tk.Canvas(root, width=500, height=500, bg="lightblue")
canvas.pack()

# Basket properties
basket = canvas.create_rectangle(200, 450, 300, 470, fill="brown")
basket_speed = 20

# Egg properties
eggs = []
egg_speed = 5
egg_interval = 2000  # Time interval for new eggs (ms)
score = 0
game_running = True

# Display score
score_text = canvas.create_text(50, 20, text=f"Score: {score}", font=("Arial", 14), fill="black")

# Function to move basket
def move_basket(event):
    if not game_running:
        return
    x1, _, x2, _ = canvas.coords(basket)
    if event.keysym == "Left" and x1 > 0:
        canvas.move(basket, -basket_speed, 0)
    elif event.keysym == "Right" and x2 < 500:
        canvas.move(basket, basket_speed, 0)

# Function to create eggs
def create_egg():
    if not game_running:
        return
    x_pos = random.randint(50, 450)
    egg = canvas.create_oval(x_pos, 0, x_pos + 20, 20, fill="yellow")
    eggs.append(egg)
    root.after(egg_interval, create_egg)

# Function to move eggs
def move_eggs():
    global score, game_running
    if not game_running:
        return

    for egg in eggs[:]:
        canvas.move(egg, 0, egg_speed)
        x1, y1, x2, y2 = canvas.coords(egg)
        bx1, _, bx2, by2 = canvas.coords(basket)

        # Check if egg is caught
        if y2 >= 450 and bx1 < x1 and x2 < bx2:
            canvas.delete(egg)
            eggs.remove(egg)
            score += 1
            canvas.itemconfig(score_text, text=f"Score: {score}")
        elif y2 > 500:  # Egg missed
            game_over()
            return

    root.after(50, move_eggs)

# Game over function
def game_over():
    global game_running
    game_running = False
    canvas.create_text(250, 250, text=f"Game Over!\nFinal Score: {score}", font=("Arial", 20), fill="red")
    restart_btn = tk.Button(root, text="Restart", command=restart_game)
    canvas.create_window(250, 300, window=restart_btn)

# Restart game function
def restart_game():
    global eggs, score, game_running
    for egg in eggs:
        canvas.delete(egg)
    eggs.clear()
    canvas.coords(basket, 200, 450, 300, 470)
    score = 0
    canvas.itemconfig(score_text, text=f"Score: {score}")
    game_running = True
    create_egg()
    move_eggs()

# Bind keys for basket movement
canvas.bind_all("<Left>", move_basket)
canvas.bind_all("<Right>", move_basket)

# Start game
create_egg()
move_eggs()
root.mainloop()
