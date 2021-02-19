
import tkinter as tk

def did_from_url (url):
    print(url)
    startIndex = url.find("/documents/") + 11 #3 #find where the start of /d/ for did + 3 indecies bc of "/" + "d" + "/"
    try:
        endIndex = url.find("/w")
    
    except:
        endIndex = url.find("/v")
    did = "" #initialize did as a str

    #build did from url chr by chr
    for i in range (startIndex, endIndex):
        did += url[i]
    return did

def main_function():
    url = str(E1.get())
    did = did_from_url(url)

    return

gui = tk.Tk()
gui.geometry('300x100')
L1 = tk.Label(gui, text="Insert Part URL: ")
L1.pack(side = "top")
E1 = tk.Entry(gui, bd =5, width = 35)
E1.pack(side = "top")
B1 = tk.Button(gui, text =" Enter ", command = main_function)
B1.pack(side = "top")
scoreLabel = tk.Label(gui, text ="SCORE:      ")
scoreLabel.pack(side = "bottom")


gui.mainloop()