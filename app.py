import random
import tkinter as tk
from tkinter import ttk

# create main window
root = tk.Tk()
root.title("Wordle")
root.geometry("400x600")

def load_words(file):
    with open(file, 'r') as file:
        words = file.read().splitlines()
    return words

def game_over():
    for widget in root.winfo_children():
        widget.destroy()

    over_label = ttk.Label(root, text="Game Over", font=("Helvetica", 16))
    over_label.pack(pady=20)

    answer_label = ttk.Label(root, text=f"The word was: {answer}", font=("Helvetica", 14))
    answer_label.pack(pady=10)

    play_again_button = ttk.Button(root, text="Play Again", command=reset_game)
    play_again_button.pack(pady=20)

    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

def you_win():
    global current_row
    for widget in root.winfo_children():
        widget.destroy()

    win_label = ttk.Label(root, text="You Win!", font=("Helvetica", 16))
    win_label.pack(pady=20)

    play_again_button = ttk.Button(root, text="Play Again", command=reset_game)
    play_again_button.pack(pady=20)

    exit_button = ttk.Button(root, text="Exit", command=root.quit)
    exit_button.pack(pady=10)

def reset_game():
    global current_row, answer, labels
    current_row = 0
    answer = random.choice(words).lower()

    for widget in root.winfo_children():
        widget.destroy()
    create_ui()

def check_guess(guess, c_answer):
    result = [''] * 5
    answer_list = list(c_answer)

    for i in range(5):
        if guess[i] == answer_list[i]:
            result[i] = 'green'
            answer_list[i] = None

    for i in range(5):
        if result[i] == '':
            if guess[i] in answer_list:
                result[i] = 'yellow'
                answer_list[answer_list.index(guess[i])] = None
            else:
                result[i] = 'gray'
    print("Check Guess - Guess: ", guess)
    print("Check Guess - Colors: ", result)
    return result

def display_guess(guess, colors):
    for n, letter in enumerate(guess):
        labels[current_row][n].config(text=letter)

        if colors[n] == 'green':
            labels[current_row][n].configure(background="green")
        elif colors[n] == 'yellow':
            labels[current_row][n].configure(background="yellow")
        else:
            labels[current_row][n].configure(background="gray")

        labels[current_row][n].update_idletasks()

def validate_length(value):
    if len(value) <= 5:
        return True
    return False

vcmd = (root.register(validate_length), '%P')
words = load_words('words.txt')
answer = random.choice(words).lower()

print("Words loaded:", words)  # debugging: makes sure the file is being read correctly
print("Chosen answer:", answer)
current_row = 0

def submit_guess():
    global current_row
    guess = entry.get().lower()
    if len(guess) == 5:
        colors = check_guess(guess, answer)
        display_guess(guess, colors)
        if guess == answer:
            you_win()
            return
        current_row += 1
        entry.delete(0, tk.END)
        if current_row >= len(labels):
            print("Game Over")
            game_over()
    else:
        print("Enter a 5-letter word")

def create_ui():
    global labels, entry

    label = ttk.Label(root, text="WORDLE", font=("Helvetica", 16))
    label.pack(pady=20)

    grid_frame = ttk.Frame(root)
    grid_frame.pack(pady=10)

    # create grid
    labels = []
    for i in range(6):
        row_labels = []
        for j in range(5):
            label = tk.Label(grid_frame, font=("Helvetica", 14), width=2, height=2, borderwidth=1, relief="solid")
            label.grid(row=i, column=j, padx=5, pady=5)
            row_labels.append(label)
        labels.append(row_labels)

    entry = tk.Entry(root, font=("Helvetica", 14), validate='key', validatecommand=vcmd)
    entry.pack(pady=10)

    button = ttk.Button(root, text="Submit guess", command=submit_guess)
    button.pack(pady=20)

create_ui()
root.mainloop()