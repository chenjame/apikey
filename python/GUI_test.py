
import tkinter as tk

gui = tk.Tk()
global url

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

L1 = tk.Label(gui, text="Insert Part URL: ").grid(row = 0, column=0)
#L1.pack(side = "left")
E1 = tk.Entry(gui, bd =5).grid(row=0,column=2)
#E1.pack(side = "left")
B = tk.Button(gui, text =" Enter ", command = main_function).grid(row=0,column=5)
#B.pack(side = "right")
scoreLabel = tk.Label(gui, text ="SCORE: ").grid(row=1,column =3)
#scoreLabel.pack(side ="bottom")

gui.mainloop()