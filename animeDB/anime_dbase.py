#!/usr/bin/python

# Sanskar Chand 2016-09-14 C.E.
# Here's hoping that I'll be able to understand this
# after a month without overheating my brain.

import tkinter as tk 
import tkinter.ttk as ttk
import tkinter.font as tkFont
import json
import datetime
import projutils

# CONSTANTS
anidb_fname = "dbase.pysdb"


#Data format
#(SN, Ani_name, genre, eps, datetime)

def dummy():
    pass


def get_sn():
    """
    Returns SN from data_list by sorting by 
    index 0 (SN)
    """

    if len(data_list) == 0:
        return "1"


    l = sorted(data_list)
    last_sn = l[-1][0]
    new_sn = int(last_sn) + 1
    return str(new_sn)

def actual_fix(index, sn):
    
    """
    Actaully fixes SN.
    index -> Index after which inconsistencies start
    """
    l = sorted(data_list)
    for idx, each in enumerate(l[index:]):
        new_sn = str(sn + idx)
        data_list[idx][0] = new_sn

def fix_sn():
    """
    Wrapper for actual_fix to SN from where it becomes inconsistent
    """

    if len(data_list) == 0:
        return 
        
    l = sorted(data_list)

    if l[0] != 1:
        actual_fix(0, 1)

    for idx, each in enumerate(l):
        
        try:
            diff = int(each[0]) - int(l[idx+1][0])
            if diff != 1:
                actual_fix(idx, int(each[0]))
        
        except IndexError:
            return

    # Finally, write all the changes
    globalWriteDbase()


def sortby(tree, col, descending):
    
    data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]

    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)

    # switch heading
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
                    int(not descending)))

class Application(tk.Frame):
    
    def __init__(self, master=None):
        
        tk.Frame.__init__(self, master)

        self.mutex = False # determines existence of child windows
        self.sel_list = [] # list of selected items in tree

        self.grid()
        self.createWidgets()    
    
    def createWidgets(self):
        #WIDGETS_MAIN
        self.quitButton = tk.Button(self, text="Quit",
                                    command=self.quit)
        self.quitButton.grid(row=0, column=1)

        #WIDGETS_BUTTONS

        self.addButton = tk.Button(self, text="Add Anime", relief="groove",
                                         command=self.addAnime)
        self.delButton = tk.Button(self, text="Del Anime", relief="groove",
                                         command=self.delAnime)

        self.addButton.grid(row=1, column=1)
        self.delButton.grid(row=1, column=2)

        #WIDGETS_SCROLLBAR
        '''
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.yScroll.grid(row=2, column=0, sticky=tk.N+tk.S)
        self.xScroll.grid(row=4, column=1, columnspan=8,sticky=tk.E+tk.W)
        '''

        #WIDGETS_LISTBOX
        '''
        self.lBox = tk.Listbox(self, height=24, width=40,
                               xscrollcommand=self.xScroll.set,
                               yscrollcommand=self.yScroll.set)
        self.lBox.grid(row=2, column=1, columnspan=8,
                       sticky=tk.N+tk.S+tk.E+tk.W)
        '''
        '''
        self.xScroll['command'] = self.lBox.xview
        self.yScroll['command'] = self.lBox.yview
        '''

        #WIDGET_TREEVIEW

        container = ttk.Frame()
        #container.pack(fill='both', expand=True)
        container.grid()

        self.tree = ttk.Treeview(columns=data_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, 
                            xscrollcommand=hsb.set)

        self.tree.bind("<<TreeviewSelect>>", self.make_sel_list)

        self.tree.grid(column=1, row=2, sticky='nsew', in_=container)
        vsb.grid(column=2, row=2, sticky='ns', in_=container)
        hsb.grid(column=1, row=3, sticky='ew', in_=container)

        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        self.build_tree()

    def build_tree(self):
        
        for col in data_header:
            self.tree.heading(col, text=col.title(),
                              command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col, width=tkFont.Font().measure(col.title()))

        for item in data_list:
            
            self.tree.insert('', 'end', values=item)
            # adjust column width if required
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(data_header[ix], width=None) < col_w:
                    self.tree.column(data_header[ix], width=col_w)

    def make_sel_list(self, event):
        
        self.sel_list = self.tree.selection()


    def addAnime(self):
        
        if not self.mutex:
            self.root2 = tk.Toplevel() # new root (ex. frame)
            self.root2.title("Entry Wizard")
            self.mutex = True   # opened a child window

        else:
            return

        # Add buttons and text labels
        self.aniField = tk.Text(self.root2, height=4, width=18)
        self.aniLabel = tk.Label(self.root2, text="Anime name:")

        self.genreField = tk.Text(self.root2, height=2, width=8)
        self.genreLabel = tk.Label(self.root2, text="Genre:")

        self.epField = tk.Text(self.root2, height=1, width=4)
        self.epLabel = tk.Label(self.root2, text="Episodes:")

        self.sendButton = tk.Button(self.root2, text="Save",
                               command=self.saveData)

        self.aniLabel.grid(row=0, column=0)
        self.aniField.grid(row=1, column=0)
        self.genreLabel.grid(row=0, column=1)
        self.genreField.grid(row=1, column=1)
        self.epLabel.grid(row=0, column=2)
        self.epField.grid(row=1, column=2)
        self.sendButton.grid(row=3, column=2)

    def delAnime(self):
        
        
        for each in self.sel_list:
            dicto = self.tree.item(each)
            name = dicto["values"][1]
            print("Deleting : {}".format(name))
            
            #step0: delete item from tree
            self.tree.delete(each)

            #step1: remove from list
            for datum in data_list:
                if datum[1] == name:
                    data_list.remove(datum)

        #step2: recalucalate SN's
        fix_sn()

        #step2: write dbase
        globalWriteDbase(data_list)

    def saveData(self):
        """
        Retrieves data from entry form, changes them into a json-able format, 
        and writes them.
        """


        #ani_name = self.aniField.get("sentinel", tk.INSERT)

        ani_name = self.aniField.get("1.0", tk.END).strip()
        genre = self.genreField.get("1.0", tk.END).strip()
        eps = self.epField.get("1.0", tk.END).strip()

        cur_dtime = datetime.datetime.now()
        dtime_string = projutils.format_datetime(cur_dtime)

        my_sn = get_sn()

        datum = [my_sn, ani_name, genre, eps, dtime_string]
        data_list.append(datum)

        # Insert into tree
        self.tree.insert('', 'end', values=datum)
        globalWriteDbase(data_list)

        # destroy child window
        self.root2.destroy()
        self.mutex = False



def globalWriteDbase(data_list):
    
    try:
        with open(anidb_fname, 'w') as dbfile:
            json.dump(data_list, dbfile)
        
        return 0

    except:
        
        return -1
        

def globalReadDbase():
    
    try:
        with open(anidb_fname, 'r')  as dbfile:
            
            data_list = json.load(dbfile) 
            return data_list
    except:
        return []



data_header = ["SN", "Anime name", "Genre", "Episodes", "Date added"]
#data_list = [("1", "Gintama", "Comedy, Adventure, Drama", "216",
#"2016-09-10 16:54")]

if __name__ == "__main__":
    data_list = globalReadDbase()
    print(data_list)

    pro = Application()
    #pro.master.geometry('640x440+40+40')
    pro.master.title("Anime DBase Program")
    pro.mainloop()

