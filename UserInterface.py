from tkinter import *
import time
root = Tk()
root.geometry("500x500")
titel = Label(master = root, text = 'Super Marvel Captain', foreground = 'blue', font=('Helvetica', 16), width = 100, height = 2)
titel.pack(pady = 20, side = TOP)
score = 30


hint1TextLabel = Label(root, text="First hint: ")
hint1Label = Label(root, text="hoi")

hint2TextLabel = Label(root, text="Second hint: ")
hint2Label = Label(root, text="hoi")

hint3TextLabel = Label(root, text="Third hint: ")
hint3Label = Label(root, text="hoi")

scoreLabel = Label(root, text = score)
def closeGame():
    root.destroy()


def controleerAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton):
    antwoord = entry.get()
    return antwoord == gekozenHeld


def verwijderWidgets(*widgets):
    for widget in widgets:
        widget.forget()

def geefHint(btn, superheldHint, label, textLabel):

    btn.forget()
    global score
    if superheldHint != "destroy":
        label.pack()
        textLabel.pack()
        score -= 1
        updateScore("Update")

def updateScore(scoreAvailable):
    global scoreLabel
    global score
    if scoreAvailable == "Update":
        scoreLabel.destroy()
        scoreLabel = Label(root, text=score)
        scoreLabel.pack(side=LEFT)
    elif scoreAvailable == "Create":
        scoreLabel = Label(root, text=score)
        scoreLabel.pack(side=LEFT)
    elif scoreAvailable == "Reset":
        score = 30
        scoreLabel.destroy()
        scoreLabel = Label(root, text=score)

def submitAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton):
    if controleerAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton):
        verwijderWidgets(submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton,
                         hint1Label, hint1TextLabel, hint2Label, hint2TextLabel, hint3Label, hint3TextLabel)
        updateScore("Reset")
        startspel()


def startspel():
    entry.delete(0, 'end')
    gekozenHeld = "test"
    updateScore("Create")
    superheldHint1 = 'hey'
    superheldHint2 = 'hoi'
    superheldHint3 = 'hai'

    eersteHintButton = Button(root, text = "Give First Hint", command = lambda: geefHint(eersteHintButton, superheldHint1, hint1TextLabel, hint1Label))
    tweedeHintButton = Button(root, text = "Give Second Hint", command = lambda: geefHint(tweedeHintButton, superheldHint2, hint2TextLabel, hint2Label))
    derdeHintButton = Button(root, text = "Give Third Hint", command = lambda: geefHint(derdeHintButton, superheldHint3, hint3TextLabel, hint3Label))

    submit = Button(root, text = "Submit Answer", foreground = "blue", command = lambda: submitAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton))
    exit = Button(root, text = "Exit", command = closeGame)

    tweedeHintButton.pack(side = BOTTOM)
    derdeHintButton.pack(side = BOTTOM)
    eersteHintButton.pack(side = BOTTOM)

    entry.pack(side = BOTTOM)
    submit.pack(side = BOTTOM, pady = 20)
    exit.pack(side = RIGHT)



def start_up():
    name = entry.get().strip()
    if name != "":
        playerName = Label(root, text="Player Name: ", pady = 5)
        nameLabel = Label(root, text = name, foreground = 'blue', font=('Helvetica', 16))

        playerName.pack()
        nameLabel.pack()

        button.destroy()
        giveName.destroy()

        startspel()


giveName = Label(root, text="Insert your name: ")
entry = Entry(root)
button = Button(root, text="Enter", command=start_up)

giveName.pack()
entry.pack()
button.pack()

root.mainloop()