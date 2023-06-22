from tkinter import *
from tkinter import filedialog
from tkinter import Text
from tkinter import messagebox
from Rope import *
from BMAlgorithm import *

####### from docx import Document
class TextEditor:
    
    def __init__(self,root):
        self.root = root
        self.savecount = 0  # ----------2
        self.name=0
        self.root.title("Text Editor TARAS")

        self.root.geometry("900x660")

        self.filename = None
        # self.words = 0
        self.characters = 0
        self.check,self.repl=False,False
        # self.title = StringVar()  # Title variable
        self.index=0
        self.status = StringVar()  # Status Variable
        # self.status1 = StringVar()

        # Text Pad working.
        # self.titlebar = Label(self.root,textvariable=self.title,font=("Helvetica", 16),relief=GROOVE)
        # self.titlebar.pack(side=TOP,fill=Y)
        # self.settitle()

        # Creating Statusbar
        self.statusbar = Label(self.root,textvariable = self.status,font=("Arial", 12),relief=GROOVE)
        self.statusbar.pack(side=BOTTOM, fill=BOTH)
        self.status.set("© 2022 TARAS")

        # # creating another status bar----------4

        # self.statusbar1 = Label(self.root,textvariable=self.status1,anchor='sw',font=("times new roman", 15))

        # self.statusbar1.pack(side=BOTTOM,fill=BOTH)
        # self.status1.set("words = 0")

        # self.root.status ("nsudsm")

        # Creating Scrollbar

        scrol_y = Scrollbar(self.root)
        self.txtarea = Text(self.root, yscrollcommand=scrol_y.set, font=("Arial", 11), selectbackground="yellow",selectforeground="Red", fg='black', bg='white')
        self.txt = self.txtarea.get("1.0", END)
        self.words = self.txt.count(" ") + self.txt.count("\n")
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_y.config(command=self.txtarea.yview)
        self.txtarea.pack(fill=BOTH, expand=50)

         # Creating Menu: 
        self.menubar = Menu(self.root, font=("Arial",18), activebackground="yellow")
        self.root.config(menu=self.menubar)

        # Creating File Menu
        self.filemenu = Menu(self.menubar, font=("Arial", 11), activebackground="skyblue", tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New",accelerator="Ctrl+N", command=self.newfile)
        self.filemenu.add_command(label="New Window",accelerator="Ctrl+shift+N", command=self.newwindow)
        self.filemenu.add_command(label="Open",accelerator="Ctrl+O", command=self.openfile)
        self.filemenu.add_command(label="Save",accelerator="Ctrl+S", command=self.savefile)
        self.filemenu.add_command(label="Save As",accelerator="Ctrl+shift+S", command=self.saveasfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.exit)

        # Edit menu:
        self.editmenu = Menu(self.menubar, font=("Arial", 11), activebackground="skyblue", tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.editmenu.add_command(label="Cut",accelerator="Ctrl+X", command=self.cut)
        self.editmenu.add_command(label="Copy",accelerator="Ctrl+C", command=self.copy)
        self.editmenu.add_command(label="Paste",accelerator="Ctrl+V", command=self.paste)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Undo",accelerator="Ctrl+Z", command=self.undo)
        self.editmenu.add_command(label="Redo",accelerator="Ctrl+Y", command=self.redo)
        self.editmenu.add_separator()
        self.editmenu.add_command(label="Find",accelerator="Ctrl+F", command=self.find)
        self.editmenu.add_command(label="Replace",accelerator="Ctrl+H", command=self.replace)
        self.editmenu.add_separator()
        self.saveState()


        self.shortcuts()  # -----------3

    # def settitle(self):
    #     # if self.filename:
    #     #     #Updating Title as Filename
    #     #     self.title.set("Text editor")
    #     # else:
    #           # Updating Title
    #     self.title.set("TEXT PAD")

    def newfile(self, *args):
        self.txtarea.delete("1.0", END)
        # Clear Area first
        self.filename = None
        # New File as None
        # self.settitle()
        # self.status.set("New File Created")  # Status created form welcome to editor to new file created
        self.savecount = 0
        # self.status1.set("words = 0")
        # self.insertbutton()
        self.saveState()
  
    def newwindow(self, *args):
        newroot = Tk()
        TextEditor(newroot)
        newroot.mainloop()
        self.saveState()
  
    def openfile(self, *args):
        # Exception handling
        # self.words = 0
        try:
            self.filename = filedialog.askopenfilename(title="select file",
                                                   filetypes=[("Text files", "*.txt"), ("Python Files", "*.py")])
            print(self.filename)
            if self.filename != None:
                self.savecount += 1
                infile = open(self.filename, "r")  # read mode
                # 1=len(infile)
                self.txtarea.delete("1.0", END)  # clearing text area

                counter = 0
                while True:
                    if counter > 11 and counter % 6 == 0:
                        character = infile.read(6)
                        if not character:
                            break
                        rope,self.characters = self.insertion(character, self.characters)
                        
                        # self.words += character.count(" ")
                        # self.words += character.count("/n")
                        # self.status.config(self.words)
                        # self.status1.configure()
                        self.txtarea.insert(END, character)
                    else:
                        character = infile.read(11)
                        if not character:
                            break
                        rope,self.characters = add_first(character)
                        # self.words+=character.count(" ")
                        # self.words+=character.count("\n")
                        self.txtarea.insert(END, character)
                        # self.st.Updating()
                        # self.txtarea.edit_modified (words)
                    counter = +1
                infile.close()

                # self.settitle()
                # self.status.set("Opened sucessfully")  # status changed!
                # self.status1.set(str(self.words) + " words")
        except Exception as e:
                 print("Can't Access",e)
        self.saveState()

    def saveasfile(self, *args):
        # Exception Handling
        try:
            # Asking for file name and type to save
            self.filename = filedialog.asksaveasfilename(title="Save file as", defaultextension=".txt",initialfile="untitled.txt", filetypes=(("Text Files", "*.txt"), ("Python", "*.py")))
            # Reading the data from the text area
            data = self.txtarea.get("1.0", END)
            # Opening file in write mode
            outfile = open(self.filename, "w")
            # Writting data into file
            outfile.write(data)
            # closing file
            outfile.close()
            # updating filename as untitled
            # self.filename=untitledfile
            # Calling Set titile
            # self.settitle()
            # updating Status
            # self.status.set("Saved successfully")
        except Exception as e:
            print("Can't Access",e)
        self.saveState()

    def savefile(self, *args):
        try:
            if self.savecount != 0:
                if self.filename != None:
                    data = self.txtarea.get("1.0", END)  # reading the file
                    outfile = open(self.filename, "w")  # opening File in write mode
                    outfile.write(data)
                    outfile.close()
                    # self.settitle()
                    # self.status.set("Saved Successfully")  # status changed
                    # self.status1.set(str(self.words) + " word")
                    # else:
                    #  Self.saveasfile()
            elif self.savecount == 0:
                self.savecount += 1
                self.saveasfile()
        except Exception as e:
            print("Can't access")
        self.saveState()

    def exit(self, *args):
             self.root.destroy()
             self.saveState()

    def cut(self, *args):
        try:
            self.cuttext=self.txtarea.selection_get()
            self.txtarea.delete(self.txtarea.index("sel.first"),self.txtarea.index("sel.last"))
        except:
            self.cuttext=""
        self.name=1 # cut indentifier
        self.saveState()
        
    def copy(self, *args):
        try:
            self.copytext=self.txtarea.selection_get()
        except:
            self.copytext=""
        self.name=2 # copy indentifier
        self.saveState()

    def paste(self, *args):
        ind=self.txtarea.index(INSERT)
        if(self.name==1):
            self.txtarea.insert(ind,self.cuttext)
        elif(self.name==2):
            self.txtarea.insert(ind,self.copytext)
        else:
            self.txtarea.insert(ind,"")
        self.saveState()
     # List for storing savestates
# List for storing savestates
    obj = []
    # List for storing undone save states
    objR = []
    def undo(self, *args):
       self._undo(self.txtarea)
       
    def redo(self, *args):
       self._redo(self.txtarea)
       
     # Takes most recent save state(other then the current), pops and removes it from the list. Adds this to the redo savestate list. Calls the main undo function on this savestate
    def _save(self, text):
        self.obj.append(self.saveT())
    def _undo(self, text):
        n = len(self.obj) - 1
        self.objR.append(self.saveT())
        self.undoT(self.obj[n-1])
        del(self.obj[n-1])

    # Takes the most recent save state from the redo state list, and calls the undo function for it. It removes this from the Rlist, and adds this to the undo state list.

    def _redo(self, text):
        n = len(self.objR)
        self.obj.append(self.saveT())
        self.undoT(self.objR[n-1])
        del(self.objR[n-1])

    # Returns an object containing the contents of the textbox
    def saveT(self):
      return Memento(self.txtarea.get("1.0", END))
    # Replaces the current text on the screen with the content of a memento object
    def undoT(self,memento):
        # reinsert text to text box here.
        replacement_text = memento.content
        self.txtarea.delete(0.0, "end")
        self.txtarea.insert(0.0, replacement_text)
    
    def saveState(self):
        self._save(self.txtarea)
    
    
    def find(self, *args):
        if(not self.check):
            self.inputtxt = Text(self.root,height = 1.5,width = 30)
            self.inputtxt.config(highlightbackground = "black",highlightthickness=2)
            self.inputtxt.pack()
            self.but=Button(self.root,text="Find",command=self.find_bt)
            self.but.pack(side='top') 
            self.check=True
        else:
            self.txtarea.tag_remove("high","1.0", END)
            self.inputtxt.destroy()
            self.but.destroy()
            self.check=False   
        self.saveState() 
   
    def find_bt(self,*args):
        f=BMAlgorithm()
        self.currloc=0
        try:
            self.select=self.txtarea.selection_get()
            self.index=self.txtarea.index("sel.first")
        except Exception :
            self.select=""
            self.index=0
        
        
        if(self.select==""):
            self.pat=self.inputtxt.get("1.0", END)
        else:
            self.pat=self.select
            self.inputtxt.delete("1.0",END)
            self.inputtxt.insert("1.0",self.pat)
            
            
        self.txt=self.txtarea.get("1.0", END)
        self.txtarea.tag_remove("high","1.0", END)
        if(self.pat[-1]==" "):
            self.pat=self.pat.replace(" ", "") 
        
        if(self.txt!="\n" and self.pat!="\n"):
            print("inside")
            if(self.pat[-1]=="\n"):
                self.pat=self.pat[:-1]
            self.inputtxt.config(highlightbackground = "black",highlightthickness=2)
            s=f.findall(self.txt,self.pat)
            self.color("red","cyan",s=s,txt=self.txt,pat=self.pat)
            self.match=s
            
        elif(self.pat=="\n"):
            self.inputtxt.config(highlightbackground = "red",highlightthickness=2)
        if(self.index!=0):
            self.index=[i for i in range(len(self.matloc)) if(self.matloc[i][0]==self.index)][0] 
        self.currloc=self.index
        print(self.index,self.currloc)  
        self.saveState()
            
    def color(self,fg,bg,s=[0],txt="",pat=""):
        newline =1
        j=0;
        count=0
        self.matloc=[]
        for i in range(len(txt)):
            if(txt[i]=="\n"):
                newline +=1
                j=-1
            if( count!=len(s) and  i==s[count]):
                self.matloc.append(((str(newline)+"."+str(j)),str(newline)+"."+str(j+len(pat))))
                self.txtarea.tag_add("high", str(newline)+"."+str(j), str(newline)+"."+str(j+len(pat)))
                self.txtarea.tag_config("high", background=bg, foreground=fg)
                count+=1
            j+=1 
        self.saveState()
  
    def replace(self, *args):
        if(not self.repl):
            if(not self.check):
                self.find()
            self.down=0
            self.currloc=self.index
            self.change=self.currloc
            self.getreplace= Text(self.root,height = 1.5,width = 30)
            self.getreplace.config(highlightbackground = "black",highlightthickness=2)
            self.getreplace.pack()
            self.replace=Button(self.root,text="Replace",command=self.replacefun)
            self.replace.pack(side='top') 
            self.replaceAll=Button(self.root,text="Replace All",command=self.replaceAllfun)
            self.replaceAll.pack(side='top') 
            
            self.upbtn=Button(self.root,text="↑",command=self.upfun)
            self.upbtn.pack(side='right')
            self.downbtn=Button(self.root,text="↓",command=self.downfun)
            self.downbtn.pack(side='right')
            # ↓
            self.repl=True
        else:
            self.txtarea.tag_remove("high","1.0", END)
            self.inputtxt.destroy()
            self.but.destroy()
            self.downbtn.destroy()
            self.upbtn.destroy()
            self.getreplace.destroy()
            self.replace.destroy()
            self.replaceAll.destroy()
            self.repl=False
            self.check=False
        self.saveState()
            
    def replacefun(self, *args):
        self.replacetxt=self.getreplace.get("1.0", END)
        self.replacetxt=self.replacetxt.replace("\n","")
        self.replacetxt=self.replacetxt.replace(" ","")
        self.txtarea.delete(self.matloc[self.currloc][0],self.matloc[self.currloc][1])
        self.txtarea.insert(self.matloc[self.currloc][0],self.replacetxt)
        self.find_bt()
        self.down=0
        self.up=0
        self.saveState()
        
    def replaceAllfun(self, *args):
        self.replacetxt=self.getreplace.get("1.0", END)
        self.replacetxt=self.replacetxt.replace("\n","")
        self.replacetxt=self.replacetxt.replace(" ","")
        i=0
        while(len(self.matloc)!=0):
            self.txtarea.delete(self.matloc[0][0],self.matloc[0][1])
            self.txtarea.insert(self.matloc[0][0],self.replacetxt)
            self.find_bt()
        self.saveState()
            
    def upfun(self, *args):
        if(self.currloc==0):
           self.change=self.currloc
           self.currloc=len(self.matloc)-1
           self.up=0
        else:
           self.change=self.currloc
           self.up=-1
           
        self.txtarea.tag_remove("high1",self.matloc[self.change][0],self.matloc[self.change][1])
        self.currloc+=self.up
        self.txtarea.tag_add("high1",self.matloc[self.currloc][0],self.matloc[self.currloc][1])
        self.txtarea.tag_config("high1", background="pink", foreground="black")
        self.saveState()
           
    def downfun(self, *args):
        
        self.txtarea.tag_remove("high1",self.matloc[self.change][0],self.matloc[self.change][1])
        self.currloc+=self.down
        self.txtarea.tag_add("high1",self.matloc[self.currloc][0],self.matloc[self.currloc][1])
        self.txtarea.tag_config("high1",background="pink", foreground="black")
        if(self.currloc!=len(self.matloc)-1):
            self.down=1
            self.change=self.currloc
        else:
           self.change=self.currloc
           self.currloc=0
           self.down=0
        self.saveState()
      
    def shortcuts(self, *args):  # Binding Ctrlen to newfile funtion
        self.txtarea.bind("<Control-n>", self.newfile)
        self.txtarea.bind("<Control-N>", self.newwindow)
        self.txtarea.bind("<Control-o>", self.openfile)
        self.txtarea.bind("<Control-s>", self.savefile)
        self.txtarea.bind("<Control-S>", self.saveasfile)  # not working
        self.txtarea.bind("<Control-e>", self.exit)
        self.txtarea.bind("<Control-x>", self.cut)
        self.txtarea.bind("<Control-c>", self.copy)
        self.txtarea.bind("<<Control-v>>", self.paste)
        self.txtarea.bind("<Control-z>", self.undo)
        self.txtarea.bind("<Control-y>", self.redo)
        self.txtarea.bind("<Control-f>", self.find)
        self.txtarea.bind("<Control-h>", self.replace)
        self.saveState()

 # Memory Objects
class Memento:
       def __init__(self, content):
          self.content = content


root = Tk()
TextEditor(root)
root.mainloop()
# TextEditor.insertbutton()
