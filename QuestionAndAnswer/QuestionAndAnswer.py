# import pandas as pd
# from random import *
import importlib
"""
    Multichoice Question: [Question, [A,B,C,D]] and Answer is A

    ChoiceLetter Question: [Question, Choice_Letter, Answer]

    Connect Word Question: 

"""

pd = importlib.import_module("pandas")
def GetNameLevel() -> dict:
    file = open("QuestionAndAnswer/LevelName.txt", mode = "r", encoding="utf-8")
    Data = file.read().split("\n")
    Data = [Data[i].split(" : ") for i in range(len(Data))]
    
    result = {}
    for D in range(len(Data)):
        result[int(Data[D][0])] = Data[D][1]
    
    return result


def GetQuestion(level, ChildLevel, IsAdmin = False):
    QuestionSystem = []

    if not IsAdmin:
        data = pd.read_excel(f"QuestionAndAnswer\\Level{level}\\{ChildLevel}.xlsx")
    
    else:
        data = pd.read_excel(f"QuestionAndAnswer\\{level}\\{ChildLevel}.xlsx")

    def multichoice(Question):
        Q = data["Question"][Question]
        A = data["A"][Question]
        B = data["B"][Question]
        C = data["C"][Question]
        D = data["D"][Question]
        QuestionSystem.append([TypeQuestion, Q, [A,B,C,D], A])
    
    def choiceLetter(Question):
        Q = data["Question"][Question]
        Question_1 = data["Question_1"][Question].split(", ")
        Answer = data["Answer"][Question]
        Voice = data["Voice"][Question]

        QuestionSystem.append([TypeQuestion, Q, Question_1, Answer, Voice])

    for Question in range(len(data["Type Question"])):
        TypeQuestion = data["Type Question"][Question]

        if TypeQuestion == 0:
            multichoice(Question)
        
        elif TypeQuestion == 1:
            choiceLetter(Question)
        
        elif TypeQuestion == 20:
            multichoice(Question)
        
        elif TypeQuestion == 21:
            choiceLetter(Question)
        
        elif TypeQuestion == 30:
            Connect_Word_Dictionary = {}
            
            for i in range(1, 5):
                Connect_Word = data[f"Question_3_{i}"][Question].split(" -#- ")
                Connect_Word_Dictionary[Connect_Word[0]] = Connect_Word[1]
            
            QuestionSystem.append([TypeQuestion, Connect_Word_Dictionary])

    return QuestionSystem

levelDictionary = GetNameLevel()