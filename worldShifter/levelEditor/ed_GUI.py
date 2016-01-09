"""
@name ed_GUI.py

This module provides a graphical frontend for the 
level editor.

"""

import Tkinter as Tk


class mainGUI:
    
    def __init__(self, master):
        """
        Initialisation params:
            master -> root window
        
        """

        self.master = master
        self.mode = Tk.StringVar()
        self.mode_list = ["Create Level",
                          "Edit Existing Level"
                         ]

        self.mode_string = "" # Actual mode string

        self.createWidgets()

    def createWidgets(self):
        """
        Create widgets for frontend.
        The widgets are:
          -> An OptionMenu for choosing between
             the NEW and EDIT modes
          -> A field for entering level width
          -> Various buttons
        """
        textLabel = Tk.Label(self.master, text="Select Editor Mode:")
        dropDown = Tk.OptionMenu(self.master, self.mode, *self.mode_list)
        selectBut = Tk.Button(self.master, text="Select Mode", command=\
                                self.handleMode)

        textLabel.grid(row=0, column=1)
        dropDown.grid(row=1, column=0)
        selectBut.grid(row=2, column=1)

    def handleMode(self):
        """
        Handle editor modes after the user 
        presses appropriate buttons.
        """

        dat = self.mode.get()

        if dat == self.mode_list[0]:
            self.mode_string = "NEW"
        elif dat == self.mode_list[1]:
            self.mode_string = "EDIT"
        else:
            print("Please select a valid option.")

        print("You have selected {} mode.".format(self.mode_string))

def main():
    root = Tk.Tk()
    myGUI = mainGUI(root)
    Tk.mainloop()
