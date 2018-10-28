from operator import itemgetter
import json
import time


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
    result: None
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


scoresfile = 'Highscores.json'
scores = getHighScores(scoresfile)

addHighScore(scores, "2020/01/01", 543)
addHighScore(scores, "2019/01/01", 123)

print(getHighScore(scores, "2019/01/01"))
print(getHighScore(scores, "2018/10/27"))
print(getHighScore(scores, "2018/10/25"))
print("Alltime score: ", getAllTimeHighScore(scores))

print("Sorted\n", getSortedScoresByDate(scores))
saveHighScores("test.json", scores)
