#!/usr/bin/env python


#Started: 9 May 2015 CE, Saturday, GMT +5:45 18:59
#Project to create a GUI-based manga downloading program for ubuntu.
#By Sanskar Chand, currently 16 years 5 months 12 days old

#This is mangwarrior3.py

from Tkinter import *
import urllibX, re, os # urllibX is urllib with the user agent changed
import bs4, pickle
import subprocess

#Import stuff
namelist = []
remove_set  = set() #Set of manganame.html files to remove
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >=0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

def chapMap(webpage):
    "Returns a mapping of chapter: link pairs"
    chapDict = dict()
    soupe = bs4.BeautifulSoup(open(webpage, 'r'))
    yummy = soupe.findAll('a')
    for tasty in yummy:
        y = None
        x = ''.join(tasty.findAll(text=True))
        if tasty.attrs.has_key('href'):
            y = tasty['href']
        chapDict[x] = y
    return chapDict

class mainGUI:
    def __init__(self, master):
        self.master = master
        self.createWidgets()

    def createWidgets(self):
        self.frame = Frame(self.master)
        self.frame.pack()

        self.label1 = Label(self.master, text='Select manga',\
                            bg='blue', fg='white')
        self.label1.pack()

        self.bar = Scrollbar()
        self.liste = Listbox()
        self.bar.pack(side=LEFT, fill=Y)
        self.liste.pack(side=LEFT, fill=Y)

        self.bar.config(command=self.liste.yview)
        self.liste.config(yscrollcommand = self.bar.set)

        for each in namelist:
            self.liste.insert(END, each)
        self.liste.bind('<Double-Button-1>', self.call_back)

        self.but = Button(self.master, text='Select Title', command=self.mangdl)
        self.but.pack(side=LEFT)

        self.val = ''

        self.closeb = Button(self.master, text='QUIT', command=self.quit)
        self.closeb.pack(side=BOTTOM)

    def call_back(self, event):
        self.val = self.liste.curselection()
        num = 0
        for x in self.val:
            num =x
        self.val = num

    def mangdl(self):
        try:
            mangaLinkMap = pickle.load(open("dbase.txt", 'r'))

            #Go to the main page of the manga title
            #and Download the first chapter. Trial.
            #But, before that, create a new folder dedicated to this
            #particular manga title and aslo a folder for chapter 1
            print "Ore ha koko ni iru"
            x  = namelist[self.val]

            # Compatibility for files
            # replace apostrophes
            x.replace("'", r"\'")

            # folcreate creates folders
            # callind order :
            # clickable_wind - chapVal - chapDL - folcreate

            # note: this turned out to be unnecessary
            # check apos below

            remove_set.add(x+'.html')

            if not os.path.isfile(x + '.html'):
                urllibX.urlretrieve('http://www.mangareader.net'\
                                    +mangaLinkMap[x], x+'.html')
            print 'Node boku mo ', mangaLinkMap[x]
            print "Soshite, sono namae ha ", x
            newDict = chapMap(x+'.html')
            clickable_wind(newDict, x)
        except:
            pass

    def quit(self):
        self.master.destroy()


def chapDL(index, listChap, mangaName):
    print listChap[index], " -<-< Doitsumo Koitsumo"
    urlH = chapDict[listChap[index]]
    print "url ha ", urlH
    print "Manganame ha ", mangaName
    apos = "\""
    apos+mangaName+apos+" "+ apos+listChap[index]+apos
    os.system("./folcreate.sh "+ apos+mangaName+apos+" "+apos+listChap[index]+apos)

    fileS = './'+mangaName+'/'+listChap[index]+ '/'+listChap[index]+'.html'

    namelist = []
    PAGES = 75 # Checks for PAGES pages
    for i in range(1, PAGES):
        #Differentiates between old-type and new-type links
        if '-' in urlH and is_int(urlH[urlH.index('-')+1]):
            print "LINKTYPE: Old"
            ind = find_nth(urlH, '-', 2)
            copy = urlH
            digiLen = 2
            copy = copy[:ind+1] + str(i) +'/' +copy[ind+len(str(i))+digiLen:]
            print "OURLINK: ", copy
            urllibX.urlretrieve("http://www.mangareader.net"+copy, fileS)
        else:
            urllibX.urlretrieve("http://www.mangareader.net"+urlH+'/'+str(i), fileS)
        #Open the chapter page
        imgSoup = bs4.BeautifulSoup(open(fileS, 'r'))
        chitra = imgSoup.findAll('img')
        #Display the source img

        for each in chitra:
            print "LINK"
            print each['src']
            link = each['src']

            #Get the filename-after the last /
            name = link[link.rfind('/')+1:len(link)]
            namelist.append(name)
            urllibX.urlretrieve(link, mangaName+'/'+listChap[index]+'/'+name)
    '''
    newJ = 1
    kuso = mangaName + '/'+listChap[index] +'/'
    for each in namelist:
        os.rename(kuso+each, kuso+str(newJ)+'.jpg')
    '''

def chapVal(mName, chapList, diction):
    print "chapVal is executed"

    try:
        for each in chapList:
            if diction[each].get():
                print "Downloading chapter ", each
                chapDL(chapList.index(each), chapList, mName)
    except KeyError:
        pass

def clickable_wind(dicto, mangaName):
    #root2 = Tk()
    root2 = Toplevel()
    print "STAGE 1"

    vsb = Scrollbar(root2,orient="vertical")
    text = Text(root2,width=40, height=20, yscrollcommand=vsb.set)
    vsb.config(command=text.yview)
    vsb.pack(side="right", fill="y")
    text.pack(side="left", fill="both", expand=True)

    print "STAGE 2"
    global chapDict
    chapDict = dicto
    global lC
    lC = dicto.keys()
    lC.sort()

    #Download or not on/off values dictionary for each chap.
    choice = dict()
    for chapter in  lC:
        choice[chapter] = IntVar()

    print "STAGE 3"
    for chapter in lC:
        temp = Checkbutton(root2, text=chapter, variable=choice[chapter])
        text.window_create("end", window=temp)
        text.insert("end", "\n") # in order to force one checkbox per line

    button = Button(root2, text='Download Chapter(s)',command= lambda:chapVal(mangaName, lC, choice))
    button.pack()

    #root2.mainloop()
    print "TEME!!!!!!!  ", val

#Make list of manga titles
if not os.path.isfile("mnrdl_list.html"):
    urllibX.urlretrieve("http://www.mangareader.net/alphabetical",\
                       "mnrdl_list.html")

myDict = {}

if not os.path.isfile("dbase.txt"):
    soup = bs4.BeautifulSoup(open('mnrdl_list.html'))
    f1 = open('dbase.txt', 'w+')
    mname = soup.findAll('a')
    for node in mname:
        a = ''.join(node.findAll(text=True))
        b = None
        if node.attrs.has_key('href'):
            b = node['href']
        myDict[a] = b
    pickle.dump(myDict, f1)
    f1.close()
else:
    f = open('dbase.txt', 'r')
    dicto = pickle.load(f)
    l = dicto.keys()
    l.sort()
    namelist = l

#Read the mangalist file into namelistf
namelist = [each.replace('\n', '') for each in namelist]




root = Tk()
myg = mainGUI(root)
root.mainloop()

for manga in remove_set:
    os.remove(manga)
