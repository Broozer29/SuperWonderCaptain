from tkinter import *
import time
import hashlib
import requests
import json
import random

root = Tk()
root.geometry("500x500")
titel = Label(master=root, text='Super Marvel Captain', foreground='blue', font=('Helvetica', 16), width=100, height=2)
titel.pack(pady=20, side=TOP)
score = 30

gekozenHeld = ""
superheldHint1 = ""
superheldHint2 = ""
superheldHint3 = 0

# hint1TextLabel = Label(root, text="First hint: ")
# hint1Label = Label(root, text=superheldHint1)

# hint2TextLabel = Label(root, text="Second hint: ")
# hint2Label = Label(root, text=superheldHint2)

# hint3TextLabel = Label(root, text="Third hint: ")
# hint3Label = Label(root, text=superheldHint3)

scoreLabel = Label(root, text=score)

firstCall = "http://gateway.marvel.com:80/v1/public/events"


def getHighScores(filename):
    try:
        with open(filename, 'r') as f:
            scoresfile = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, use your default values
        scoresfile = {"scores": {time.strftime("%Y/%m/%d"): 0}}
    highscores = scoresfile["scores"]
    return highscores


def saveHighScores(filename, scores):
    highscores = {"scores": scores}
    with open(filename, 'w') as f:
        json.dump(highscores, f)


def addHighScore(scores, date, score):
    scores[date] = score


def getHighScore(scores, date):
    try:
        score = scores[date]
    except KeyError:
        score = 0
    return score


def getAllTimeHighScore(scores):
    result = None
    highest = 0

    for date in scores.keys():
        score = scores[date]
        if score > highest:
            highest = score
            result = {date: score}
    return result


def getSortedScoresByDate(scores):
    result = []
    for key in sorted(scores.keys()):
        result.append({key: scores[key]})
    return result


def closeGame():
    root.destroy()


def controleerAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton):
    antwoord = entry.get()
    print(gekozenHeld)
    return antwoord == gekozenHeld


def verwijderWidgets(*widgets):
    for widget in widgets:
        widget.forget()


def geefHint(btn, superheldHint, label, textLabel):
    btn.forget()
    global score
    global hint1Label, hint2Label, hint3Label
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


def submitAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton, hint1TextLabel,
                   hint2TextLabel, hint3TextLabel, hint1Label, hint2Label, hint3Label):
    global score
    if controleerAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton):
        verwijderWidgets(submit, exit, eersteHintButton, tweedeHintButton, derdeHintButton,
                         hint1Label, hint1TextLabel, hint2Label, hint2TextLabel, hint3Label, hint3TextLabel)
        addHighScore(scores, time.strftime("%Y/%m/%d"), score)
        updateScore("Reset")
        startspel()
    else:
        score -= 3
        print("Incorrect!")


def startspel():
    global gekozenHeld, superheldHint1, superheldHint2, superheldHint3
    gekozenHeld, superheldHint1, superheldHint2, superheldHint3 = haalMarvelInfo()
    entry.delete(0, 'end')
    updateScore("Create")

    hint1TextLabel = Label(root, text="First hint: ")
    hint1Label = Label(root, text=superheldHint1)

    hint2TextLabel = Label(root, text="Second hint: ")
    hint2Label = Label(root, text=superheldHint2)

    hint3TextLabel = Label(root, text="Third hint: ")
    hint3Label = Label(root, text=superheldHint3)

    eersteHintButton = Button(root, text="Give First Hint",
                              command=lambda: geefHint(eersteHintButton, superheldHint1, hint1TextLabel, hint1Label))
    tweedeHintButton = Button(root, text="Give Second Hint",
                              command=lambda: geefHint(tweedeHintButton, superheldHint2, hint2TextLabel, hint2Label))
    derdeHintButton = Button(root, text="Give Third Hint",
                             command=lambda: geefHint(derdeHintButton, superheldHint3, hint3TextLabel, hint3Label))

    submit = Button(root, text="Submit Answer", foreground="blue",
                    command=lambda: submitAntwoord(gekozenHeld, submit, exit, eersteHintButton, tweedeHintButton,
                                                   derdeHintButton, hint1TextLabel, hint2TextLabel, hint3TextLabel,
                                                   hint1Label, hint2Label, hint3Label))
    exit = Button(root, text="Exit", command=closeGame)

    derdeHintButton.pack(side=BOTTOM)
    tweedeHintButton.pack(side=BOTTOM)
    eersteHintButton.pack(side=BOTTOM)

    entry.pack(side=BOTTOM)
    submit.pack(side=BOTTOM, pady=20)
    exit.pack(side=RIGHT)


def start_up():
    global score
    name = entry.get().strip()
    if name != "":
        playerName = Label(root, text="Player Name: ", pady=5)
        nameLabel = Label(root, text=name, foreground='blue', font=('Helvetica', 16))

        playerName.pack()
        nameLabel.pack()

        button.destroy()
        giveName.destroy()

        startspel()



def showHighscores():
    window = Toplevel(root)
    highscoreAllTimeLabel = Label(window, text="All time highscore: (Dag/Month/Year : Score)")
    highscoreAllTimeScore = Label(window, text=getAllTimeHighScore(scores))
    highscoreTodayLabel = Label(window, text="Today's highscore: ")
    highscoreTodayScore = Label(window, text=getHighScore(scores, time.strftime("%Y/%m/%d")))
    highscoreAllTimeLabel.pack()
    highscoreAllTimeScore.pack()
    highscoreTodayLabel.pack()
    highscoreTodayScore.pack()


def haalMarvelInfo():
    # Maak de eerste call naar de API, en haal een event op. Event in dit geval is een verhaal in een comic.
    events = roepMarvel(firstCall)

    # Selecteer alle namen van de helden die voorkomen in desbetreffend event.
    temp = roepMarvel(events[0]['resourceURI'])
    characters = temp[0]['characters']

    # Van de 20 namen die terugkomen, seleteer een willekeurige.
    randomGetal = random.randrange(1, len(characters['items']))
    heldNaam = characters['items'][randomGetal]['name']
    print("Gekozen held: ", heldNaam)

    # Roep de URL van de held(in) op.
    heldLink = characters['items'][randomGetal]['resourceURI']
    print("Heldlink: ", heldLink)

    # Bepaal in welke comic de held(in) zit.
    # Marvel 20 objecten teruggeven, dus kunnen we weer randomGetal gebruiken om een willekeurige comic te selecteren.
    heldComic = roepMarvel(heldLink)
    comicX = heldComic[0]['comics']['items'][randomGetal]['name']
    print("Gekozen comic (hint): ", comicX)

    # Bepaal in welk universum de held(in) terugkwam, en leid daarvan af in welke series hij zich bevind.
    heldSerie = roepMarvel(heldLink)
    welkeSerie = heldSerie[0]['series']['items'][0]['resourceURI']
    print("Gekozen serie (URL): ", welkeSerie)

    # Selecteer van de serie het event, en kijk naar de personages die er in voorkomen.
    aantalPersonages = roepMarvel(welkeSerie)
    # Omdat een comic niet altijd 20 personages heeft, maar ook minder kan hebben, kan hier niet randomGetal gebruikt worden.
    # In plaats daarvan wordt het aantal personages uitgerekend, en daar een willekeurige uit gekozen.
    totaalAantalPersonages = len(aantalPersonages[0]['characters']['items'])
    randomPersonageGetal = random.randrange(1, totaalAantalPersonages)
    superheldXNaam = aantalPersonages[0]['characters']['items'][randomPersonageGetal]['name']
    print("Superheld X (hint): ", superheldXNaam)

    lengteHeldnaam = len(heldNaam)

    return heldNaam, superheldXNaam, comicX, lengteHeldnaam


def roepMarvel(url):
    timestamp = str(time.time())
    private_key = "a458b3fd88726c2ccf88ae1cf3177fb645532df2"
    public_key = "d98db3e2da438da72688319eb2bc9751"
    hash = hashlib.md5((timestamp + private_key + public_key).encode('utf-8'))
    md5digest = str(hash.hexdigest())
    connection_url = url + "?ts=" + timestamp + "&apikey=" + public_key + "&hash=" + md5digest
    response = requests.get(connection_url)
    jsontext = json.loads(response.text)  # om de JSON leesbaar te printen... #
    return jsontext['data']['results']


scoresfile = 'Highscores.json'
scores = getHighScores(scoresfile)
# print("Alltime score: ", getAllTimeHighScore(scores))
# print("Sorted\n", getSortedScoresByDate(scores))
saveHighScores(scoresfile, scores)

giveName = Label(root, text="Insert your name: ")
entry = Entry(root)
button = Button(root, text="Enter", command=start_up)
highscoreKnop = Button(root, text="Highscores", command=showHighscores)

highscoreKnop.pack()
giveName.pack()
entry.pack()
button.pack()

root.mainloop()
