"""
@name ed_GUI.py

This module provides a graphical frontend for the 
level editor.

"""

import Tkinter as Tk
import tkFileDialog
import editor


def quitGUI(root):
    root.destroy()

def popUp(message):
    """
    Show dialog box containing message.
    """
    print(message)


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
        self.lw = Tk.StringVar()    # For storing level width
        self.newFrame = None    # this frame holds widgets for newlevel optons 
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

    def createNewlevelWidgets(self):
        """
        Provide widgets to the user for creating a new editable level.
        """

        self.newFrame = Tk.Frame(height=6, bd=1, relief=Tk.SUNKEN)
        self.newFrame.grid(row=3, column=0)

        widthLabel = Tk.Label(self.newFrame,
                              text="Enter level width(>=500)")

        entryField = Tk.Entry(self.newFrame, text=self.lw)
        createBut = Tk.Button(self.newFrame, text="Create", 
                              command=self.createLevel)

        widthLabel.grid(row=3, column=0)
        entryField.grid(row=4, column=0)
        createBut.grid(row=4, column=1)

    def createEditlevelWidgets(self):
        """
        Provide widgets to the user for editing an existing level.
        """

        myFile = tkFileDialog.askopenfile(parent=self.master, mode='rb', 
                                          title='Choose a file(.lvf)')

        if myFile != None:
            
            name = myFile.name
            myFile.close()
            
            # The filename must have a .lvf extension
            if name[-3:] != 'lvf':
                print("Invalid Filename")
                return

            quitGUI(self.master)
            editor.editLevel(name)
    
    def createLevel(self):
        """
        Create a new editable level.
        """

        lwidth = self.lw.get()

        try:
            width = int(lwidth)
        except ValueError:
            popUp("Please enter an integer.")
            return

        quitGUI(self.master)
        editor.newLevel(width)

    def handleMode(self):
        """
        Handle editor modes after the user 
        presses appropriate buttons.
        """

        dat = self.mode.get()

        if dat == self.mode_list[0]:
            self.mode_string = "NEW"
            self.createNewlevelWidgets()

        elif dat == self.mode_list[1]:
            self.mode_string = "EDIT"
            # Remove any existing "NEW" widgets
            # Or rather, remove the entire frame
            if self.newFrame is not None:
                self.newFrame.destroy()

            self.createEditlevelWidgets()
        else:
            print("Please select a valid option.")

        print("You have selected {} mode.".format(self.mode_string))

def main():
    root = Tk.Tk()
    myGUI = mainGUI(root)
    Tk.mainloop()

if __name__ == '__main__':
    main()
