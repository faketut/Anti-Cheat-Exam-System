import ctypes
import threading
import time
import psutil
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from threading import Timer
from Functions import FUNCTIONS, checkAccount, addUser
from Config import *

# get random question data
dataList = FUNCTIONS()
#print(dataList.SingleList)
#print(dataList.MultiList)
#print(dataList.JudgeList)

# front-end class: interface and data usage of registeration and answering
class UI:
    #init params
    def __init__(self):
        self.ban = None
        self.state = STATE_INIT
        self.count = 0
        self.minute = TIME
        self.second = 0
        self.ans = []
        self.score = 0
        self.loginWindow = tk.Tk()
        self.initialLoginWindow(self.loginWindow)

    #init loginWindow
    def initialLoginWindow(self, loginWindow):
        loginWindow['bg'] = 'skyblue'
        loginWindow.title('Anti-cheating Exam System-login/register')
        loginWindow.resizable(width=False,height=False)

        width = loginWindow.winfo_screenwidth()
        height = loginWindow.winfo_screenheight()
        loginWindow.geometry("400x200+%d+%d" % (width/2 - 200, height/2 - 200))

        self.varAccount = tk.StringVar()
        self.varAccount.set('')
        self.varKey = tk.StringVar()
        self.varKey.set('')

        self.labelAccount = tk.Label(loginWindow, text='user_id:',
                                     justify=tk.RIGHT, width=60)
        self.labelKey = tk.Label(loginWindow, text='password:',
                                 justify=tk.RIGHT, width=60)

        self.labelAccount.place(x=20,y=20,width=160,height=40)
        self.labelKey.place(x=20,y=70,width=160,height=40)

        self.account = tk.Entry(loginWindow, width=80, textvariable=self.varAccount)
        self.account.place(x=200, y=20, width=160, height=40)
        self.key = tk.Entry(loginWindow, show='*', width=80, textvariable=self.varKey)
        self.key.place(x=200, y=70, width=160, height=40)

        buttonOK = tk.Button(loginWindow, text='login', command=self.login)
        buttonOK.place(x=20,y=140,width=100,height=40)
        buttonRegister = tk.Button(loginWindow, text='register', command=self.register)
        buttonRegister.place(x=140,y=140,width=100,height=40)
        buttonCancel = tk.Button(loginWindow, text='cancel',command=self.cancelLogin)
        buttonCancel.place(x=260,y=140,width=100,height=40)

        loginWindow.bind('<Escape>', lambda e: loginWindow.destroy())
        loginWindow.mainloop()

    def login(self):
        name = self.account.get()
        passwd = self.key.get()
        nameList, passwordList = checkAccount('user_id.txt')
        for i in range(len(nameList)):
            if name == nameList[i]:
                if passwd == passwordList[i]:
                    tk.messagebox.showinfo(title='Hint', message='login successfully!')
                    self.loginWindow.destroy()
                    self.mainWindow = tk.Tk()
                    self.initialMainWindow(self.mainWindow)
                    return
        tk.messagebox.showerror('Hint', message='incorrect username or password!')
        return

    def cancelLogin(self):
        self.varAccount.set('')
        self.varKey.set('')

    def register(self):
        name = self.account.get()
        passwd = self.key.get()
        if name == "" or passwd == "":
            tk.messagebox.showerror('Hint', messagebox='please enter password!')
            return
        userNameList, userPasswordList = checkAccount('user_id.txt')
        if not userNameList or not userPasswordList:
            addUser('user_id.txt', name, passwd)
            return
        for userName in userNameList:
            if name == userName:
                tk.messagebox.showerror('Hint',message='user already exists!')
                return
        registerSuccessful = addUser('user_id.txt', name, passwd)
        if registerSuccessful:
            messagebox.showinfo('Hint',message='register successfully!')

    def initialMainWindow(self, mainWindow):
        self.width = mainWindow.winfo_screenwidth()
        self.height = mainWindow.winfo_screenheight()
        mainWindow.geometry("800x540+%d+%d" % (self.width/2 - 400, self.height/2 - 300))
        mainWindow['bg'] = 'skyblue'
        mainWindow.title('Anti-cheating Exam System-start exam')
        mainWindow.resizable(width=False,height=False)

        #start anti-cheating procedure
        self.ban = tk.IntVar()
        def funcBan():
            while self.ban.get() == 1:
                for pid in psutil.pids():
                    try:
                        p = psutil.Process(pid)
                        exeName = os.path.basename(p.exe().lower())
                        if exeName in ('notepad.exe','winword.exe','wps.exe','wordpad.exe','iexplore.exe',
                               'chrome.exe','opera.exe','baidubrowser.exe','Edge.exe','Firefox.exe'):
                            p.kill()
                    except:
                        pass
                ctypes.windll.user32.OpenClipboard(None)
                ctypes.windll.user32.EmptyClipboard()
                ctypes.windll.user32.CloseClipboard()
                time.sleep(1)

        def Anti_start():
            self.ban.set(1)
            t = threading.Thread(target=funcBan)
            t.start()

        Anti_start()
        mainWindow.protocol('WM_DELETE_WINDOW', self.closeMainWindow)
        self.setMenu(mainWindow)
        mainWindow.bind('<Escape>', lambda e: self.closeMainWindow)

        self.totalCount = dataList.Single.totalNum + \
                          dataList.Multi.totalNum + dataList.Judge.totalNum
        print(self.totalCount)

        #create exam components
        self.showInitFsm()
        #show result
        self.watchDog()
        mainWindow.mainloop()

    def showInitFsm(self):
        #score module
        self.varScore = tk.StringVar()
        self.varScore.set(str(self.score) + '\\' + str(TOTAL_SCORE))
        self.showScore = tk.Label(self.mainWindow, textvariable=self.varScore, fg='brown')
        self.showScore.place(x=10,y=70,width=150,height=50)
        self.showScoreName = tk.Label(self.mainWindow, text='score',
                                      width=150,height=50,justify='center',
                                      anchor='ne',fg='white',bg='grey',
                                      padx=20,pady=10)
        self.showScoreName.place(x=10,y=130,width=150,height=60)

        #time module
        self.varTimeLft = tk.StringVar()
        self.timeLeft = tk.Label(self.mainWindow, textvariable=self.varTimeLft)
        self.timeLeft.place(x=10,y=190,width=150,height=50)
        self.showTimeLeft = tk.Label(self.mainWindow, text='remaining time',
                                     width=150, height=50, justify='left',
                                     anchor='ne',fg='white',bg='grey',
                                     padx=20,pady=10)
        self.showTimeLeft.place(x=10,y=130,width=150,height=60)

        #option module
        self.varButtonA = tk.StringVar()
        self.varButtonA.set(
            'A. ' + str(dataList.SingleList[self.count % SINGLE_NUMBER]['A'])
        )
        self.varButtonB = tk.StringVar()
        self.varButtonB.set(
            'B. ' + str(dataList.SingleList[self.count % SINGLE_NUMBER]['B'])
        )
        self.varButtonC = tk.StringVar()
        self.varButtonC.set(
            'C. ' + str(dataList.SingleList[self.count % SINGLE_NUMBER]['C'])
        )
        self.varButtonD = tk.StringVar()
        self.varButtonD.set(
            'D. ' + str(dataList.SingleList[self.count % SINGLE_NUMBER]['D'])
        )
        self.buttonA = tk.Button(self.mainWindow, textvariable=self.varButtonA,
                                 command=self.buttonAFsm)
        self.buttonB = tk.Button(self.mainWindow, textvariable=self.varButtonB,
                                 command=self.buttonBFsm)
        self.buttonC = tk.Button(self.mainWindow, textvariable=self.varButtonC,
                                 command=self.buttonCFsm)
        self.buttonD = tk.Button(self.mainWindow, textvariable=self.varButtonD,
                                 command=self.buttonDFsm)
        self.buttonOK = tk.Button(self.mainWindow, text='confirm',
                                 command=self.buttonOKFsm)

        self.buttonA.place(x=100,y=300,width=300,height=50)
        self.buttonB.place(x=100,y=350,width=300,height=50)
        self.buttonC.place(x=100,y=400,width=300,height=50)
        self.buttonD.place(x=100,y=450,width=300,height=50)
        self.buttonOK.place(x=500,y=450,width=150,height=50)

        self.showUserSelect = tk.Label(self.mainWindow, text='chosen',
                                       width=150,height=50,justify='left',
                                       anchor='ne',fg='white',bg='grey',
                                       padx=20,pady=10)
        self.showUserSelect.place(x=500,y=300,width=150,height=60)

        self.varChoice = tk.StringVar()
        self.varChoice.set(list2str(self.ans))
        self.showChoice = tk.Label(self.mainWindow, textvariable=self.varChoice)
        self.showChoice.place(x=500,y=360,width=150,height=50)

        #question module
        self.subject = scrolledtext.ScrolledText(self.mainWindow, height=8,
                                                 width=40)
        self.subject.place(x=190,y=10)
        print('1st single-choice ques')
        self.count = 0
        self.state = STATE_SINGLE
        self.subject.insert('end','question'+ str(self.count +1) + ':' +
                            dataList.SingleList[self.count]['content']
                            + '\n')

    #choose operation
    #choose A
    def buttonAFsm(self):
        print('  [Event: buttonA clicked]')
        if self.state == STATE_SINGLE:
            self.ans = []
            self.ans.append('A')
        elif self.state == STATE_MULTI:
            if 'A' not in self.ans:
                self.ans.append('A')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('A')
        else:
            self.ans = []
            self.ans.append('TRUE')
        self.varChoice.set(list2str(self.ans))
    def buttonBFsm(self):
        print('  [Event: buttonB clicked]')
        if self.state == STATE_SINGLE:
            self.ans = []
            self.ans.append('B')
        elif self.state == STATE_MULTI:
            if 'B' not in self.ans:
                self.ans.append('B')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('B')
        else:
            self.ans = []
            self.ans.append('TRUE')
        self.varChoice.set(list2str(self.ans))
    def buttonCFsm(self):
        print('  [Event: buttonC clicked]')
        if self.state == STATE_SINGLE:
            self.ans = []
            self.ans.append('C')
        elif self.state == STATE_MULTI:
            if 'C' not in self.ans:
                self.ans.append('C')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('C')
        else:
            self.ans = []
            self.ans.append('FALSE')
        self.varChoice.set(list2str(self.ans))
    def buttonDFsm(self):
        print('  [Event: buttonD clicked]')
        if self.state == STATE_SINGLE:
            self.ans = []
            self.ans.append('D')
        elif self.state == STATE_MULTI:
            if 'D' not in self.ans:
                self.ans.append('D')
                self.ans = sorted(self.ans)
            else:
                self.ans.remove('D')
        else:
            self.ans = []
            self.ans.append('FALSE')
        self.varChoice.set(list2str(self.ans))

    #check answer
    def buttonOKFsm(self):
        self.score += self.checkAns()
        self.varScore.set(str(self.score) + '/' + str(TOTAL_SCORE))
        self.count = self.count + 1
        self.varChoice.set('')
        if self.count >= TOTAL:
            self.showDoneFsm()
            return
        self.ans = []
        if self.state == STATE_SINGLE:
            self.showSingleFsm()
        elif self.state == STATE_MULTI:
            self.showMultiFsm()
        elif self.state == STATE_JUDGE:
            self.showJudgeFsm()
    #show result
    def checkAns(self)->int:
        if self.state == STATE_SINGLE:
            print("score on single-choice:", self.count)
            if list2str(self.ans) == dataList.SingleList[self.count]['correct answer']:
                return SINGLE_SCORE
            else:
                return 0
        elif self.state == STATE_MULTI:
            print("score on multi_choice:")
            if list2str(self.ans) == dataList.MultiList[self.count - SINGLE_NUMBER]['correct answer']:
                return MULTI_SCORE
            else:
                return 0
        else:
            print("score on judgment:")
            if list2str(self.ans) == dataList.JudgeList[self.count - SINGLE_NUMBER - MULTI_NUMBER]['correct answer']:
                return JUDGE_SCORE
            else:
                return 0
    #update ques (next)
    def updateSubject(self, listName, number, state):
        print(self.count)
        self.subject.delete(0.0, tk.END)
        if state == STATE_SINGLE:
            print("2nd single-choice")
            self.subject.insert('end','question'+str(self.count + 1) + ':' +
                                listName[self.count]['content']+'\n')
            self.varButtonA.set('A. '+str(listName[self.count]['A']))
            self.varButtonB.set('B. '+str(listName[self.count]['B']))
            self.varButtonC.set('C. '+str(listName[self.count]['C']))
            self.varButtonD.set('D. '+str(listName[self.count]['D']))
        elif state == STATE_MULTI:
            print("1st multi-choice")
            self.subject.insert('end', 'question'+str(self.count +1)+ ':' +
                                listName[self.count-SINGLE_NUMBER]['content']
                                + '\n')
            self.varButtonA.set('A. '+str(listName[self.count - SINGLE_NUMBER]['A']))
            self.varButtonB.set('B. '+str(listName[self.count - SINGLE_NUMBER]['B']))
            self.varButtonC.set('C. '+str(listName[self.count - SINGLE_NUMBER]['C']))
            self.varButtonD.set('D. '+str(listName[self.count - SINGLE_NUMBER]['D']))
        else:
            self.subject.delete(0.0, tk.END)
            self.subject.insert('end','question'+str(self.count + 1) + ':' +
                                dataList.JudgeList[self.count-SINGLE_NUMBER-MULTI_NUMBER]['content']
                                + '\n')
            self.buttonTrue=tk.Button(self.mainWindow,text='TRUE',command=self.buttonAFsm)
            self.buttonFalse=tk.Button(self.mainWindow,text='FALSE',command=self.buttonCFsm)
            self.buttonTrue.place(x=100,y=300,width=300,height=50)
            self.buttonFalse.place(x=100,y=350,width=300,height=50)

    #generate single-choice
    def showSingleFsm(self):
        if self.count < SINGLE_NUMBER:
            self.state = STATE_SINGLE
            self.updateSubject(dataList.SingleList, SINGLE_NUMBER,self.state)
        else:
            self.state = STATE_MULTI
            self.buttonA.place(x=100,y=300,width=300,height=50)
            self.buttonB.place(x=100,y=350,width=300,height=50)
            self.buttonC.place(x=100,y=400,width=300,height=50)
            self.buttonD.place(x=100,y=450,width=300,height=50)
            self.updateSubject(dataList.MultiList, SINGLE_NUMBER,self.state)

    #generate multi-choice
    def showMultiFsm(self):
        if SINGLE_NUMBER <= self.count < SINGLE_NUMBER + MULTI_NUMBER:
            self.state = STATE_MULTI
            self.updateSubject(dataList.MultiList, MULTI_NUMBER,self.state)
        else:
            self.state = STATE_JUDGE
            self.buttonA.destroy()
            self.buttonB.destroy()
            self.buttonC.destroy()
            self.buttonD.destroy()
            self.updateSubject(dataList.JudgeList, JUDGE_NUMBER,self.state)

    #generate judge
    def showJudgeFsm(self):
        if SINGLE_NUMBER+MULTI_NUMBER <= self.count < self.totalCount:
            self.state = STATE_JUDGE
            self.subject.delete(0.0, tk.END)
            print('2nd judgement')
            self.updateSubject(dataList.JudgeList,JUDGE_NUMBER,self.state)
        else:
            self.state = STATE_DONE

    #exam end
    def showDoneFsm(self):
        self.ban.set(0)
        self.buttonTrue.destroy()
        self.buttonFalse.destroy()
        self.buttonA.destroy()
        self.buttonB.destroy()
        self.buttonC.destroy()
        self.buttonD.destroy()
        self.buttonOK.destroy()
        self.showChoice.destroy()
        self.subject.destroy()
        #time ending
        self.timeCount.cancel()
        self.showScoreName = tk.Label(self.mainWindow, text='final score:',
                                      width=150,height=50,justify='left',
                                      anchor='nw',fg='white',bg='grey',)
        self.showScoreName.place(x=10,y=10,width=150,height=50)
        print("program end!")
        #show score
        if self.score < 60:
            messagebox.showinfo('Got '+str(self.score)+'. Try it again.')
            self.mainWindow.destroy()
        elif 60 <= self.score <= 85:
            messagebox.showinfo('Got '+str(self.score)+'. You can improve it.')
            self.mainWindow.destroy()
        else:
            messagebox.showinfo('Got '+str(self.score)+'. Excellence!')
            self.mainWindow.destroy()

    #create menu
    def setMenu(self, window):
        menubar = tk.Menu(window)
        filemenu = tk.Menu(menubar,tearoff=0)
        filemenu.add_command(label='exit',command=window.destroy)
        infoMenu = tk.Menu(menubar,tearoff=0)
        infoMenu.add_command(label='software info',command=self.menuInfo)
        menubar.add_cascade(label='exit program',menu=filemenu)
        menubar.add_cascade(label='software info',menu=infoMenu)
        window.config(menu=menubar)

    def menuInfo(self):
        messagebox.showinfo('Hint','Created by Jian! Thanks for your support.')

    #timer
    def watchDog(self):
        timeleft = 60*self.minute+self.second
        timeleft -=1
        self.second = self.second -1
        if self.second <0:
            self.minute=self.minute-1
            self.second=59
        if self.minute<0 or timeleft ==0:
            self.state=STATE_DONE
            self.showDoneFsm()
        self.varTimeLft.set(str(self.minute)+':' +str(self.second))
        self.timeCount = Timer(1,self.watchDog, ())
        self.timeCount.start()

    #close program hint
    def closeMainWindow(self):
        self.ban.set(0)
        ans = messagebox.askyesno(title='exit',message='You didn\'t save it. Still want to exit?')
        if ans:
            self.mainWindow.destroy()
        else:
            self.ban.set(1)
            pass

#program entrance
if __name__ == '__main__':
    test = UI()










