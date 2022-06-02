from tkinter import StringVar
import tkinter as tk

window = tk.Tk()

frame = tk.Frame()
frame.pack()

bottomframe = tk.Frame()
bottomframe.pack(side=tk.BOTTOM)

outputstring = StringVar()
outputstring.set("default text")

# event handlers
def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)


def handle_click(event):
    string1 = '''
    Gear level: 0
    Gear type: 0
    Gear enhance lvl: 0
    Substat: Health Flat - 7, rolled 1 times
    Substat: Critical Hit Damage - 7, rolled 1 times
    Substat: Attack Percent - 8, rolled 1 times
    Substat: Critical Hit Chance - 5, rolled 1 times

    Gear score: 24.124310344827585
    Gear score potential: 69.69706766674207
    '''
    print("The button was clicked!")
    output["text"] = string1

def start_click():
    string1 = '''
    Gear level: 0
    Gear type: 0
    Gear enhance lvl: 0
    Substat: Health Flat - 7, rolled 1 times
    Substat: Critical Hit Damage - 7, rolled 1 times
    Substat: Attack Percent - 8, rolled 1 times
    Substat: Critical Hit Chance - 5, rolled 1 times

    Gear score: 24.124310344827585
    Gear score potential: 69.69706766674207
    '''
    outputstring.set(string1)


def stop_click():
    outputstring.set("Stopped")



startbutton = tk.Button(
    text="Start",
    width=25,
    height=5,
    command=start_click
)
stopbutton = tk.Button(
    text="Stop",
    width=25,
    height=5,
    command=stop_click
)
output = tk.Label(
    bottomframe,
    textvariable=outputstring
)


# Bind keypress event to handle_keypress()
# window.bind("<Key>", handle_keypress)
startbutton.pack(fill=tk.Y, side=tk.LEFT)
stopbutton.pack(fill=tk.Y, side=tk.LEFT)
output.pack(side=tk.BOTTOM)

window.mainloop()