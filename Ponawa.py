import os
from tkinter import Button, Label, Scrollbar, Tk, ttk,Toplevel,PhotoImage,filedialog,messagebox,scrolledtext
from tkinter.constants import *

imageLocPath = "images/"

iconLoc = imageLocPath+"favicon.png"
browseIcoLoc = imageLocPath+"folder.png"
addTextIcoLoc = imageLocPath+"addtext.png"
removeTextIcoLoc=imageLocPath+"removetext2.png"
replaceTextIcoLoc=imageLocPath+"replacetext.png"
serializeIcoLoc=imageLocPath+'sequence.png'
infoIcoLoc=imageLocPath+'info.png'
undoIcoLoc=imageLocPath+'undo1.png'


undoCache1 = "_undo_cache1"
undoCache2 = "_undo_cache2"

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 20
        y = y + cy + self.widget.winfo_rooty() +32
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="white", relief=SOLID, borderwidth=1,
                      font=("sans-serif", "9", "bold"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


app = Tk()
app.title("Multi-File Rename Tool")
app.geometry("400x200+500+200")
app.resizable(width=False,height=False)

icon  = PhotoImage(file = iconLoc)
app.iconphoto(False,icon)

data=""
disable_tool_btns=True

def ADD_TEXT_IN_FILE_NAMES(text):
    files_list  = data
    with open(undoCache1,"w+") as temp:
        for i in files_list:
            if((not i.endswith(".py")) and i.__contains__(".") and (not i.endswith(".cache"))):
                print("entered")
                
                file_with_dest = i.split("/")

                filename = file_with_dest[-1]
                filename = text + " "+filename

                newName=''
                for j in range(len(file_with_dest)):
                    if(j!=len(file_with_dest)-1):
                        newName += file_with_dest[j]+"/"
                    else:
                        newName += filename

                print(newName)
                temp.write(i+","+newName+"\n")
                os.rename(i,newName)

def REMOVE_TEXT_FROM_FILE_NAMES(remove):
    files_list  = data

    with open(undoCache1,"w+") as temp:
        for i in files_list:
            if(i.__contains__(remove) and (not i.endswith(".py")) and i.__contains__(".") and (not i.endswith(".cache"))):
                file_with_dest = i.split("/")

                filename = file_with_dest[-1]
                filename = filename.replace(remove,"")
                filename = filename.strip()


                newName=''
                for j in range(len(file_with_dest)):
                    if(j!=len(file_with_dest)-1):
                        newName += file_with_dest[j]+"/"
                    else:
                        newName += filename

                newName = newName.strip()
                print(newName)
                temp.write(i+","+newName+"\n")
                os.rename(i,newName)

def REPLACE_TEXT_FROM_FILE_NAMES(old_text,new_text):
    files_list  = data
    with open(undoCache1,"w+") as temp:
        for i in files_list:
            if(i.__contains__(old_text) and (not i.endswith(".py")) and i.__contains__(".")):
                print("entered")

                file_with_dest = i.split("/")

                filename = file_with_dest[-1]
                filename = filename.replace(old_text,new_text)
                filename = filename.strip()

                newName=''
                for j in range(len(file_with_dest)):
                    if(j!=len(file_with_dest)-1):
                        newName += file_with_dest[j]+"/"
                    else:
                        newName += filename

                newName = newName.strip()
                print(newName)
                temp.write(i+","+newName+"\n")
                os.rename(i,newName)

def SERIALIZE_FILE_NAMES(text):
    files_list = data
    n=1
    with open(undoCache1,"w+") as temp:
        for i in files_list:
            if((not i.endswith(".py")) and i.__contains__(".") and (not i.endswith(".cache"))):
                print("entered")                
                file_with_dest = i.split("/")

                filename = file_with_dest[-1]
                ext = filename.split('.')[-1]

                filename = filename.replace(filename,text+" "+str(n)+"."+ext)
                filename = filename.strip()

                newName=''
                for j in range(len(file_with_dest)):
                    if(j!=len(file_with_dest)-1):
                        newName += file_with_dest[j]+"/"
                    else:
                        newName += filename

                newName = newName.strip()
                print(newName)
                temp.write(i+","+newName+"\n")
                os.rename(i,newName)
                n+=1

def UNDO_LAST_CHANGE():
    with open(undoCache1,"r") as temp:
        data = temp.read()
        dataList = data.split("\n")
        for currFileData in dataList:
            fileDataList = currFileData.split(",")
            if(len(fileDataList)==2):
                print(fileDataList)
                os.rename(fileDataList[1],fileDataList[0])


def toggleToolBtns():
    if(disable_tool_btns):
        addTextBtn['state'] = 'disabled'
        removeTextBtn['state'] = 'disabled'
        replaceTextBtn['state'] = 'disabled'
        serializeBtn['state'] = 'disabled'
    else:
        addTextBtn['state']  = 'normal'
        removeTextBtn['state'] = 'normal'
        replaceTextBtn['state'] = 'normal'
        serializeBtn['state'] = 'normal'

def checkStatus():
    global disable_tool_btns
    if(data==''):
        disable_tool_btns = True
    else:
        disable_tool_btns = False
    
    toggleToolBtns()

def getFile():
    global data
    data = filedialog.askopenfilenames( filetypes = (
            ('All files', '*.*'),
            ('text files', '*.txt')
        )
    )

    print(data)
    checkStatus()

def resetData():
    global data
    data = ""
    print("data reset")
    checkStatus()
    with open(undoCache2,"w+") as file:
        file.write("false")


def handleAddText():
    global addTextWindow
    addTextWindow = Toplevel(app)
    addTextWindow.title("Add Text To File Names")
    addTextWindow.geometry("300x100+550+250")
    addTextWindow.resizable(width=False,height=False)
    addTextWindow.iconphoto(False,icon)
    

    def addText():
        text = text_ent.get()
        text = text.strip()
        if(text!=''):
            ADD_TEXT_IN_FILE_NAMES(text)
            print(text)
            resetData()
            addTextWindow.grab_release()
            messagebox.showinfo("Successful!","Selected files have been successfully renamed!")
            addTextWindow.destroy()
        else:
            messagebox.showerror("Invalid Text Input","Please Enter Some Text!")
    
    def cancel():
        addTextWindow.grab_release()
        addTextWindow.destroy()

    text_lbl = text_lbl = ttk.Label(addTextWindow, text = 'Text: ')
    text_lbl.place(x=20,y=10)

    text_ent = ttk.Entry(addTextWindow,width=30)
    text_ent.place(x=80,y=10)

    add_btn = ttk.Button(addTextWindow, text = 'Add',command=addText)
    add_btn.place(x=80,y=50)

    cancel_btn = ttk.Button(addTextWindow, text = 'Cancel',command=cancel)
    cancel_btn.place(x=200,y=50)

    addTextWindow.grab_set()

def handleRemoveText():
    global removeTextWindow
    removeTextWindow = Toplevel(app)
    removeTextWindow.title("Remove Text From File Names")
    removeTextWindow.geometry("300x100+550+250")
    removeTextWindow.resizable(width=False,height=False)

    removeTextWindow.iconphoto(False,icon)

    def removeText():
        text = text_ent.get()
        text = text.strip()
        if(text!=''):
            print(text)
            REMOVE_TEXT_FROM_FILE_NAMES(text)
            resetData()
            removeTextWindow.grab_release()
            messagebox.showinfo("Successful!","Selected files have been successfully renamed!")
            removeTextWindow.destroy()
            
        else:
            messagebox.showerror("Invalid Text Input","Please Enter Some Text!")
    
    def cancel():
        removeTextWindow.grab_release()
        removeTextWindow.destroy()


    text_lbl = text_lbl = ttk.Label(removeTextWindow, text = 'Text: ')
    text_lbl.place(x=20,y=10)

    text_ent = ttk.Entry(removeTextWindow,width=30)
    text_ent.place(x=80,y=10)

    text_ent.insert(0,"Copy of [Kayoanime]")

    remove_btn = ttk.Button(removeTextWindow, text = 'Remove',command=removeText)
    remove_btn.place(x=80,y=50)

    cancel_btn = ttk.Button(removeTextWindow, text = 'Cancel',command=cancel)
    cancel_btn.place(x=200,y=50)   

    removeTextWindow.grab_set()

def handleReplaceText():
    global replaceTextWindow
    replaceTextWindow = Toplevel(app)
    replaceTextWindow.title("Replace Text From File Names")
    replaceTextWindow.geometry("300x140+550+250")
    replaceTextWindow.resizable(width=False,height=False)

    replaceTextWindow.iconphoto(False,icon)

    def replaceText():
        oldtext = old_text_ent.get()
        oldtext = oldtext.strip()

        newtext = new_text_ent.get()
        newtext = newtext.strip()

        if(oldtext!='' and newtext!=''):
            print(oldtext,newtext)
            REPLACE_TEXT_FROM_FILE_NAMES(oldtext,newtext)
            resetData()
            replaceTextWindow.grab_release()
            messagebox.showinfo("Successful!","Selected files have been successfully renamed!")
            replaceTextWindow.destroy()

        else:
            messagebox.showerror("Invalid Text Input","Please Enter Some Text In Both Fields!")


    def cancel():
        replaceTextWindow.grab_release()
        replaceTextWindow.destroy()

    old_text_lbl = ttk.Label(replaceTextWindow, text = 'Old Text: ')
    old_text_lbl.place(x=20,y=10)

    old_text_ent = ttk.Entry(replaceTextWindow,width=30)
    old_text_ent.place(x=80,y=10)

    new_text_lbl = ttk.Label(replaceTextWindow, text = 'New Text: ')
    new_text_lbl.place(x=20,y=40)

    new_text_ent = ttk.Entry(replaceTextWindow,width=30)
    new_text_ent.place(x=80,y=40)

    replace_btn = ttk.Button(replaceTextWindow, text = 'Replace',command=replaceText)
    replace_btn.place(x=80,y=100)

    cancel_btn = ttk.Button(replaceTextWindow, text = 'Cancel',command=cancel)
    cancel_btn.place(x=200,y=100) 

    replaceTextWindow.grab_set()

def handleSerializeFiles():
    global serializeFilesWindow
    serializeFilesWindow = Toplevel(app)
    serializeFilesWindow.title("Serialize File Names")
    serializeFilesWindow.geometry("300x100+550+250")
    serializeFilesWindow.resizable(width=False,height=False)
    serializeFilesWindow.iconphoto(False,icon)


    def serializeFiles():
        text = text_ent.get()
        text = text.strip()
        if(text!=''):
            SERIALIZE_FILE_NAMES(text)
            print(text)
            resetData()
            serializeFilesWindow.grab_release()
            messagebox.showinfo("Successful!","Selected files have been successfully renamed!")
            serializeFilesWindow.destroy()
        else:
            messagebox.showerror("Invalid Text Input","Please Enter Some Text!")
    
    def cancel():
        serializeFilesWindow.grab_release()
        serializeFilesWindow.destroy()

    text_lbl = text_lbl = ttk.Label(serializeFilesWindow, text = 'Initial Text: ')
    text_lbl.place(x=20,y=10)

    text_ent = ttk.Entry(serializeFilesWindow,width=30)
    text_ent.place(x=90,y=10)

    serialize_btn = ttk.Button(serializeFilesWindow, text = 'Serialize',command=serializeFiles)
    serialize_btn.place(x=90,y=50)

    cancel_btn = ttk.Button(serializeFilesWindow, text = 'Cancel',command=cancel)
    cancel_btn.place(x=200,y=50)

    serializeFilesWindow.grab_set()

def handleUndo():
    isUndo = ""
    with open(undoCache2,"r+") as file:
        isUndo = file.read()
        print(isUndo)

    if (isUndo!="true"):
        try:
            UNDO_LAST_CHANGE()
        except:
            print("errorr")
        messagebox.showinfo("Undo Success!","Last change has been undone!")

        with open(undoCache2,"w+") as file:
            file.write("true")
    else:
        messagebox.showwarning("NO UNDO!","LAST UNDO ALREADY USED!")

def onMouseOver(event):
    showSelectedFilesBtn['bg'] = '#FF7E77'
    showSelectedFilesBtn['fg'] = 'white'

def onMouseOut(event):
    showSelectedFilesBtn['bg'] = '#4DCFE0'
    showSelectedFilesBtn['fg'] = 'black'

def showSelectedFiles():
    global showSelectedFilesWindow
    showSelectedFilesWindow = Toplevel(app)
    showSelectedFilesWindow.title("Selected Files")
    showSelectedFilesWindow.geometry("500x250+450+250")
    showSelectedFilesWindow.resizable(width=False,height=False)
    showSelectedFilesWindow.iconphoto(False,icon)

    textField = scrolledtext.ScrolledText(showSelectedFilesWindow,wrap="none",font=("monospace",10,"normal",),fg="grey")
    textHsb = Scrollbar(showSelectedFilesWindow, orient="horizontal", command=textField.xview)
    textField.configure(xscrollcommand=textHsb.set)


    def showData():
        temp = ''
        for i in data:
            temp+=i+"\n"
        return temp

    if(data!=""):
        textField.delete("1.0",END)
        textField.insert(INSERT,showData())
    else:
        textField.delete("1.0",END)
        textField.insert(INSERT,"No Files Selected!")
    
    textHsb.pack(side=BOTTOM,expand=True,fill=X)
    textField.pack(expand=True, fill=BOTH)

    textField['state'] = 'disabled'
    
    

    


browseIcon = PhotoImage(file = browseIcoLoc)
selectFilesBtn = ttk.Button(app,image=browseIcon,text="Select Files",command=getFile)
selectFilesBtn.place(x=185,y=20)
CreateToolTip(selectFilesBtn,"Select files on which you \nwant to perform renaming.")

addTextIcon = PhotoImage(file = addTextIcoLoc)
addTextBtn = ttk.Button(app, image=addTextIcon,command=handleAddText,state='disabled')
addTextBtn.place(x=50,y=90)
CreateToolTip(addTextBtn,"Add text in the start of the file name.")

removeTextIcon = PhotoImage(file = removeTextIcoLoc)
removeTextBtn = ttk.Button(app, image=removeTextIcon,command=handleRemoveText,state='disabled')
removeTextBtn.place(x=140,y=90)
CreateToolTip(removeTextBtn,"Remove text from the file name.")

replaceTextIcon = PhotoImage(file = replaceTextIcoLoc)
replaceTextBtn = ttk.Button(app, image=replaceTextIcon,command=handleReplaceText,state='disabled')
replaceTextBtn.place(x=230,y=90)
CreateToolTip(replaceTextBtn,"Replace text from the file name.")

serializeIcon = PhotoImage(file = serializeIcoLoc)
serializeBtn = ttk.Button(app, image=serializeIcon,command=handleSerializeFiles,state='disabled')
serializeBtn.place(x=310,y=90)
CreateToolTip(serializeBtn,"Rename files in a serial manner with an initial text.")


infoIcon = PhotoImage(file = infoIcoLoc)
infoBtn = Button(app,image=infoIcon,border=0,command=lambda: messagebox.showinfo("INFO","This app is developed by Abhishek."))
infoBtn.place(x=360,y=10)
CreateToolTip(infoBtn,"About")


showSelectedFilesBtn = Button(app,text='View Selected Files', bg='#4DCFE0',font=("arial",10,"bold"), borderwidth=0, command=showSelectedFiles)
showSelectedFilesBtn.bind('<Enter>', onMouseOver)
showSelectedFilesBtn.bind('<Leave>', onMouseOut)
showSelectedFilesBtn.place(x=30,y=160)

undoIcon = PhotoImage(file=undoIcoLoc)
undoBtn = ttk.Button(app, image=undoIcon,command=handleUndo)
undoBtn.place(x=350,y=150)
CreateToolTip(undoBtn,"Undo the last action performed.")

app.mainloop()
