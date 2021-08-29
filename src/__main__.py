import os
import speech_recognition as sr
from tkinter import (
    Tk,
    Label,
    Text,
    filedialog,
    Frame,
    Scale,
    TOP,
    BOTH,
    LEFT,
    RIGHT,
    BOTTOM,
    END,
    HORIZONTAL,
    StringVar
)
from config import config


class VoiceToTextApp:

    def __init__(self, master: Tk):
        self.countryCodes = ["Russian (ru)", "English (en-US)"]
        self.rec = sr.Recognizer()

        self.config = config

        self.projectName = "V2T"
        self.version = "0.0.2"
        self.appName = f"{self.projectName} {self.version}"

        self.openedFileName = StringVar()
        self.openedFileName.set("No File Opened")

        self.master = master
        self.frame = Frame(self.master)

        self.frame.pack(side = BOTTOM, expand = True, fill = BOTH)

        self.master.title(self.projectName)
        self.master.config(bg = self.config["materialGray"])
        self.master.minsize(width='500', height='400')
        self.master.maxsize(width='1280', height='500')

        self.master.bind('<Control-o>', self.openFile)
        self.master.bind('<Control-q>', self.closeApp)
        self.master.bind('<Control-s>', self.saveFile)

        self.createFileNameArea()
        self.createTimeSlider()
        self.createTextArea()

        self.master.mainloop()


    def createFileNameArea(self):
        self.fileNameArea = Label(
            self.frame,
            textvariable = self.openedFileName,
            bg = self.config["materialGray"],
            fg = self.config["whiteColor"],
            font = self.config["defaultFont"]
        )

        self.fileNameArea.pack(side = LEFT, fill = BOTH, expand = False)


    def changeLabel(self, newLabel: str):
        self.openedFileName.set(newLabel)


    def createTextArea(self):
        self.textArea = Text(
            self.master,
            bg = self.config["materialGray"],
            fg = self.config["whiteColor"],
            insertbackground = self.config["whiteColor"],
            highlightcolor = self.config["blackColor"],
            highlightbackground = self.config["materialLightGray"],
            bd = 0,
            selectbackground = self.config["whiteColor"],
            font = self.config["defaultFont"]
        )

        self.textArea.pack(side = TOP, expand = True, fill = BOTH)
        self.textArea.focus()


    def createTimeSlider(self):
        self.timeSlider = Scale(
            self.frame,
            from_ = 2,
            to = 60,
            bg = self.config["materialGray"],
            orient = HORIZONTAL,
            fg = self.config["whiteColor"],
            activebackground = self.config["materialLightGray"],
            bd = 0,
            highlightbackground = self.config["materialLightGray"],
            highlightcolor = self.config["materialGray"],
            highlightthickness = 0,
            font = self.config["defaultFont"],
            sliderlength = 75,
            label = "Duration"
        )

        self.timeSlider.pack(side = RIGHT, expand = True, fill = BOTH)


    def returnText(self, file):
        with file as source:
            audio = self.rec.record(source, duration = self.timeSlider.get())
        
        self.gsr = self.rec.recognize_google(audio, language="en-US")

        self.textArea.delete('1.0', END)
        self.textArea.insert('1.0', self.gsr)


    def openFile(self, event):
        self.changeLabel("Please stand by")

        try:
            files = filedialog.askopenfile(mode = 'rb', filetypes = (('WAV file', '*.wav'), ('FLAC file', '*.flac')), initialdir = os.getenv("HOME"))
            
            self.sourceFileName = str(os.path.basename(files.name))
            self.changeLabel(self.sourceFileName)

            self.returnText(sr.AudioFile(self.sourceFileName))
        except AttributeError:
            self.changeLabel("No File Opened")


    def saveFile(self, event):
        try:
            data = self.textArea.get('1.0', END)

            if data is None:
                self.textArea.insert('1.0', "Empty file")
            else:
                files = filedialog.asksaveasfile(mode = 'w', 
                    filetypes = (
                        ('Text', '*.txt'),
                    ),
                    initialdir = os.getenv("HOME"),
                    defaultextension = ".txt",
                )

                self.changeLabel(str(os.path.basename(files.name)))
                files.write(data)
        except AttributeError:
            pass


    def closeApp(self, event):
        self.master.destroy()

if __name__ == "__main__":
    master = Tk()
    app = VoiceToTextApp(master)