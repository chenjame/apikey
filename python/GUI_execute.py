
import tkinter as tk
import createDataSet as d
import assignScore as a

def main_function():
    global userScoreText
    url = str(E1.get())
    did = d.did_from_url(url)
    try: 
        idList = d.userWIDEID(did)
    except AttributeError: 
        userScoreText = "Uh Oh, Please Input Correct URL"
        userScoreLabel.config(text = userScoreText)
    userData = d.createTestSet(idList)
    userScore = a.assignScore("SampleDataset.csv", userData)
    userScoreText = userScore
    userScoreLabel.config(text = userScore)
    return

gui = tk.Tk()
gui.geometry('300x110')
L1 = tk.Label(gui, text="Insert Part URL from Onshape: ")
L1.pack(side = "top")
E1 = tk.Entry(gui, bd =5, width = 35)
E1.pack(side = "top")
B1 = tk.Button(gui, text =" Enter ", command = main_function)
B1.pack(side = "top")
scoreLabel = tk.Label(gui, text ="SCORE: ")
scoreLabel.pack(fill = "x")
userScoreText = " -------------- "
userScoreLabel = tk.Label(gui,text = userScoreText)
userScoreLabel.pack(side = "bottom")


gui.mainloop()