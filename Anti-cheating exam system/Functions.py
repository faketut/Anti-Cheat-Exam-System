import pandas as pd
import random
from Config import *

#check if user exist
def checkAccount(filename)->tuple:
    path = getCurrentPath() + DataPath +filename
    fid = open(path, 'r+')
    accountList = []
    userNameList, userPasswordList = [],[]
    line = fid.readlines()
    for child in line:
        accountList.append(child.strip("\n").split(' '))
    print(accountList)
    for name, password in accountList:
        userNameList.append(name)
        userPasswordList.append(password)
    fid.close()
    return userNameList, userPasswordList

#add new user
def addUser(filenmae, userName: str, userPassword: str):
    try:
        path = getCurrentPath() + DataPath +filenmae
        txtfile = open(path, 'a')
        data = '\n' + userName + ' ' + userPassword
        txtfile.close()
        return True
    except:
        return False

#single-choice ques
class SingleChoiceSubject:
    def __init__(self):
        self.scorePer = SINGLE_SCORE
        self.totalNum = SINGLE_NUMBER
        self.subjectList = {}
        self.path = getCurrentPath() + DataPath + 'questions.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='SingleChoice')
        self.temList = [] #store one-line of information
        self.randList = [] #store chosen questions

    def generateRand(self):
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, TOTAL_SINGAL-1)
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue
            print("Single choice:",self.randList)

    def getData(self):
        self.generateRand()
        count = 0
        for randCount in self.randList:
            self.subjectList[count] = {}
            self.subjectList[count]['content'] = self.df['content'][randCount]
            self.subjectList[count]['A'] = self.df['A'][randCount]
            self.subjectList[count]['B'] = self.df['B'][randCount]
            self.subjectList[count]['C'] = self.df['C'][randCount]
            self.subjectList[count]['D'] = self.df['D'][randCount]
            self.subjectList[count]['correct answer'] = self.df['correct answer'][randCount]
            count = count + 1
        return self.subjectList

#multiple-choice ques
class JudgeSubject:
    def __init__(self):
        self.scorePer = JUDGE_SCORE
        self.totalNum = JUDGE_NUMBER
        self.subjectList = {}
        self.path = getCurrentPath() + DataPath + 'questions.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='judgement')
        self.temList = [] #store one-line of information
        self.randList = [] #store chosen questions

    def generateRand(self):
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, TOTAL_JUDGE-1)
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue
            print("Judgement choice:",self.randList)

    def getData(self):
        self.generateRand()
        count = 0
        for randCount in self.randList:
            self.subjectList[count] = {}
            self.subjectList[count]['content'] = self.df['content'][randCount]
            self.subjectList[count]['correct answer'] = self.df['correct answer'][randCount]
            count = count + 1
        return self.subjectList

#judge ques
class MultiChoiceSubject:
    def __init__(self):
        self.scorePer = MULTI_SCORE
        self.totalNum = MULTI_NUMBER
        self.subjectList = {}
        self.path = getCurrentPath() + DataPath + 'questions.xlsx'
        self.df = pd.read_excel(self.path, sheet_name='MultipleChoice')
        self.temList = [] #store one-line of information
        self.randList = [] #store chosen questions

    def generateRand(self):
        count = 0
        while count < self.totalNum:
            randCount = random.randint(0, TOTAL_MULTI-1)
            if randCount not in self.randList:
                self.randList.append(randCount)
                count = count + 1
            else:
                continue
            print("Multiple choice:",self.randList)

    def getData(self):
        self.generateRand()
        count = 0
        for randCount in self.randList:
            self.subjectList[count] = {}
            self.subjectList[count]['content'] = self.df['content'][randCount]
            self.subjectList[count]['correct answer'] = self.df['correct answer'][randCount]
            count = count + 1
        return self.subjectList

#Data interface with the front-end
class FUNCTIONS:
    def __init__(self):
        self.Single = SingleChoiceSubject()
        self.Multi = MultiChoiceSubject()
        self.Judge = JudgeSubject()
        self.SingleList = self.Single.getData()
        self.MultiList = self.Multi.getData()
        self.JudgeList = self.Judge.getData()

    def test(self):
        print("SingleList:",self.SingleList)
        print("MultiList:",self.MultiList)
        print("JudgeList:",self.JudgeList)

#test
if __name__ == '__main__':
    test = FUNCTIONS()
    test.test()




