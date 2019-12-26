import psutil
import subprocess
import os
import pyautogui
import time
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

class Window(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        pyautogui.PAUSE = 2.5
        self.master = master
        self.vegasdir = "C:\Program Files\VEGAS\VEGAS Pro 14.0\vegas140.exe"    #path to vegas
        self.projectdir = 'E:\Videos\Projects'                                  #path for projects
        self.queue = []                                                         #initialize queue
        self.init_window()                                                      #creates gui

    """
    This function creates the GUI of the main window.
    """
    def init_window(self):
        self.master.title('Batch Renderer')
        self.pack(fill = BOTH, expand = 1)
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.listbox = Listbox(self, yscrollcommand = self.scrollbar.set, selectmode = MULTIPLE, height = 15, width = 65) 
        self.enqueueButton = Button(self, text = "Enqueue file", command = self.fileBrowse)
        self.dequeueButton = Button(self, text = "Dequeue files", command = self.dequeue) 
        self.renderButton = Button(self, text = "Render", command = self.render)
        self.scrollbar.config(command = self.listbox.yview)
        self.enqueueButton.place(x = 0, y = 0)
        self.dequeueButton.place(x = 75, y = 0)
        self.renderButton.place(x = 155, y = 0)
        self.listbox.place(x = 0, y = 50)

    """
    This function handles the searching of a project file. 
    Calls a file browsing window to have the user select project files.
    The file path string is then enqueued and put into the listbox.
    """
    def fileBrowse(self):
        self.filename = filedialog.askopenfilename(initialdir = self.projectdir, title = "Select A File", filetype = (("Vegas Project Files","*.veg"), ("All Files","*.*")))
        self.queue.append(self.filename)
        self.listbox.insert(len(self.queue), self.filename)

    """
    This function handles the removal of items in a queue.
    Warns the user if nothing is selected from the listbox.
    Cleanly removes items from the queue and handles an out of range error.
    """
    def dequeue(self):
        if len(self.listbox.curselection()) == 0:
            messagebox.showwarning("Warning", "You have not selected files to remove from queue. Select some files from the listbox.")
            return

        for index in self.listbox.curselection():
            try:
                self.listbox.delete(index)
                self.queue.pop(index)
            except:
                self.listbox.delete(0)
                self.queue.pop(0)

    """
    This function is the primary function.
    Warns the user if the queue is empty.
    Opens a subprocess with the first project in the queue with Sony Vegas.
    Then follows a sequence in which:
        Waits 12 seconds before doing anything.
        Does a click event to start the render.
        Recursively checks the CPU frequency.
        Pops worked item from queue.
        Repeat until queue is empty.
    
    Then it will shutdown the computer.
    """
    def render(self):
        if self.queue == []:
            messagebox.showwarning("Warning", "There are no files in the queue.")
            return

        if (self.checkVegas()):
            messagebox.showwarning("Warning", "Vegas is already running. Please close Vegas.")
            return

        while self.queue != []:
            p = subprocess.Popen([self.queue[0], self.vegasdir], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            time.sleep(12)
            self.clickEvent()
            self.checkCPU(p)
            p.wait()
            time.sleep(1)
            self.listbox.delete(0)
            self.queue.pop(0)

        self.shutdown()

    """
    This function shuts the computer down after 3 minutes.
    Also terminates the tkinter window.
    """
    def shutdown(self):
        os.system("shutdown /s /t 180")
        root.destroy()

    """
    This function handles cursor placement and clicking to start the render process.
    """
    def clickEvent(self):
        pyautogui.moveTo(400, 62)
        pyautogui.click()

    """
    This function recursively checks the CPU frequencies.
    Function calls a different function to return the average frequencies.
    If the average is above 70.0%, then Vegas is still rendering.
    Wait 90 seconds and check again.
    Otherwise, kill Sony Vegas and proceed.
    """
    def checkCPU(self, p):
        if(self.getAvg() >= 70.0 and self.checkVegas()):
            time.sleep(90)
            self.checkCPU(p)

        else:
            if (self.checkVegas()):
                self.terminateVegas(p)

            return

    """
    This function returns a float value containing the average CPU
    frequency within the last second within 10 intervals.
    """
    def getAvg(self):
        percent = 0.0
        for i in range(10):
            percent += psutil.cpu_percent(interval=0.1)

        return(percent/10.0)

    """
    This function terminates Sony Vegas and any child process.
    """
    def terminateVegas(self, p):
        subprocess.Popen("taskkill /F /T /PID %i" %p.pid , shell=True)

    """
    This function determines if Vegas is currently running.
    """
    def checkVegas(self):
        for process in psutil.process_iter():
            try:
                if "vegas140.exe" in process.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False
            
root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()