from tkinter import *
import time


# ---------------------------------- Functions ----------------------------------


# Get running time
def get_time():
    str_time = time.strftime("%I:%M:%S %p")
    realtime.config(text=str_time)
    realtime.after(1000, get_time)


# Get actual day
def get_day():
    return time.strftime("%A")


# Get actual date
def get_date():
    return time.strftime("%b %d, %Y")


# ------------------------------------- GUI -------------------------------------


# Create a windows intance
window = Tk()
window.geometry("390x240")

# Create icon and title for windows title bar
icon = PhotoImage(file="title-bar-logo.png")
window.iconphoto(True, icon)
window.title("Realtime Date and Time")

# Label for running digital time
realtime = Label(
    window,
    font=("Arial", 50),
    bg="black",
    fg="#ffffff",
)
realtime.grid(row=0, column=0)

# Label for the actual day
day = Label(
    window,
    text=get_day(),
    font=("Arial", 50),
    fg="#111111",
)
day.grid(row=1, column=0)

# Label for the actual date
date = Label(
    window,
    text=get_date(),
    font=("Arial", 50),
    fg="#111111",
)
date.grid(row=2, column=0)
get_time()

window.mainloop()
