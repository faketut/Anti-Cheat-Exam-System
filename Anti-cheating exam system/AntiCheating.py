import tkinter
import os
import time
import threading
import ctypes
import psutil

root = tkinter.Tk()
root.title('Anti-cheating demo')
#window's size and position
root.geometry('300*300+300+100')
#don't allow to change window's size
root.resizeable(False, False)
ban = tkinter.IntVar(root, 0)
#force stop the mainstream text editors and web browsers
def funcBan():
    while ban.get() == 1:
        for pid in psutil.pids():
            try:
                p = psutil.Process(pid)
                exeName = os.path.basename(p.exe()).lower()
                if exeName in ('notepad.exe','winword.exe','wps.exe','wordpad.exe','iexplore.exe',
                               'chrome.exe','opera.exe','baidubrowser.exe','Edge.exe','Firefox.exe'
                               ):
                    p.kill()
            except:
                pass
            #clean up the paste board
            ctypes.windll.user32.OpenClipboard(None)
            ctypes.windll.use32.EmptyClipboard()
            ctypes.windll.user32.CloseClipboard()
            time.sleep(1)
#start
def Anti_start():
    ban.set(1)
    t = threading.Thread(target=funcBan)
    t.start()
#stop
def Anti_stop():
    ban.set(0)
#test
buttonStart = tkinter.Button(root,text="exam start",command=Anti_start)
buttonStart.place(x=20, y=10, width=100, height=30)
buttonStop = tkinter.Button(root, text="exam end", command=Anti_stop)
buttonStop.place(x=130, y=10,width=100,height=30)
#simulate, start exam mode, after that, none content is allowed to be copied
entryMessage = tkinter.Entry(root)
entryMessage.place(x=10,y=40,width=230,height=30)
root.mainloop()