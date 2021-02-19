
import tkinter as tk
import createDataSet as d
import assignScore as a

def main_function():
    url = str(E1.get())
    did = d.did_from_url(url)
    try: 
        idList = d.userWIDEID(did)
    except AttributeError: 
        # please enter a correct url
    userData = d.createTestSet(idList)
    userScore = a.assignScore("SampleDataset.csv", userData)

    return

gui = tk.Tk()
gui.geometry('300x100')
L1 = tk.Label(gui, text="Insert Part URL from Onshape: ")
L1.pack(side = "top")
E1 = tk.Entry(gui, bd =5, width = 35)
E1.pack(side = "top")
B1 = tk.Button(gui, text =" Enter ", command = main_function)
B1.pack(side = "top")
scoreLabel = tk.Label(gui, text ="SCORE: ")
scoreLabel.pack(side = "bottom")
userScoreLabel = tk.Label(gui, text="---------")
userScoreLabel.pack(side="bottom")


gui.mainloop()