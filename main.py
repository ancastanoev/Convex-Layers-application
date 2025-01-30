#this file is just the main entry point of teh appliction, and it provides a way to access the principal file, which is gui.py
import tkinter as tk
from gui import Convexlayersapp

def main():
    root = tk.Tk()


    root.title("Convex Layers Demo - Five Algorithms")
    app = Convexlayersapp(mainwindow=root)
    app.mainloop()



if __name__ == "__main__":
    main()
