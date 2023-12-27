import os

TOTAL = 5
TOTAL_SINGAL = 5
TOTAL_MULTI = 4
TOTAL_JUDGE = 5

SINGLE_SCORE = 20
SINGLE_NUMBER = 2
MULTI_SCORE = 40
MULTI_NUMBER = 1
JUDGE_SCORE = 20
JUDGE_NUMBER = 1

TOTAL_SCORE = SINGLE_SCORE*SINGLE_NUMBER+MULTI_SCORE*MULTI_NUMBER+JUDGE_SCORE*JUDGE_NUMBER

DataPath = '\\'+'files'+'\\'

STATE_INIT = 1
STATE_SINGLE = 2
STATE_MULTI = 3
STATE_JUDGE = 4
STATE_DONE = 5

TIME = 60
#get current path, find user information table and question bank
def getCurrentPath():
    path = os.getcwd()
    return path


#display user's choice list->str
#e.g. [A]->A
def list2str(changList)->str:
    res = ''
    for index in range(len(changList)):
        res = res + str(changList[index])
    return res

