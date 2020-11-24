# imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from functools import partial
import os
import cv2
import json
# import sys
# import numpy as np

model = Tk()
model.geometry('910x500')
model.config(bg='#00A6FF')
model.title('Survellance System')

# variabels
source = StringVar()
models = StringVar()

# definations and classes
def message(code,text):
    return messagebox.showinfo(code,text)

class Survellance:

    def __init__(self):

        self.endSurvellance_ = False
        self.sourceValue = None
        self.modelPath = 0
        self.OPENCV_VIDEOIO_PRIORITY_MSMF = 0
        self.load_model()
        self.selectedSource()

    def load_model(self):
        '''
        Loads the selected Survellance Model
        :return: modelPath=Path of SurvellanceModel ,used by selected_source function
        '''
        if models.get() == 'Face and Mask':
            self.modelPath = 'Chetan'
            return self.modelPath

        if models.get() == 'Face Detection':
            self.modelPath = 'Span'
            return self.modelPath
        if models.get() == 'Mask Detection':
            modelPath = 'Logo'
            return self.modelPath
        else:
            self.modelPath = 'F:\\Project\\edai_sy\\haarcascade_frontface_default.xml'
            print(f"Selected model = {models.get()}, path={self.modelPath}")
            return self.modelPath

    def endSurvellance(self):
        '''
        Ends the survellance, since same can be acheived by pressing Q
        :return: Boolean value
        '''
        self.endSurvellance_ = True
        return self.endSurvellance_

    def selectedSource(self):
        '''
        Uses the selected Model to detect (not recognize) the face.
        Input feed can be from webcam, media file.
        :return: None
        '''
        if source.get() == 'Webcam':
            self.sourceValue = 0
        elif source.get() == 'Source 1':
            self.sourceValue = 1
        elif source.get() == 'Add media':
            self.file = askopenfile(mode='r', filetypes=[('Model', '*.webm')])
            self.sourceValue = self.file.name
        print(f"Selected Source = {source.get()}, source value = {self.sourceValue},modelPath = {self.load_model()}")

        cascade = cv2.CascadeClassifier(self.load_model())
        video_capture = cv2.VideoCapture(self.sourceValue)
        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.165,
                minNeighbors=5,
                minSize=(30, 30)
            )
            print(faces)
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Display the resulting frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

def documentation():
    """
    Opens documentation of the Project
    :return: opened documentatipn readme.txt file
    """
    os.startfile('F:\\Project\\edai_sy\\readme.txt')

class add():
    '''
    Database = Json File (MongoDb Style)
    Includes functionality of Database along with Add person Window operations
    '''
    def __init__(self):
        '''
        Loads all values from Database in a Variable
        Initialize Add person Window, which takes input as User information to add in Database
        '''

        with open('DataBase.json') as json_file:
            self.data = json.load(json_file)
            json_file.close()

        #add person Window parameters
        add = Tk()
        add.geometry('700x400')
        add.title("Add person")

        #variables
        self.gender = StringVar()
        self.count = 0

        #Initialization of Label, Buttons, Entry, Text widgets
        nameLabel = Label(add, text='Name', width=10).grid(row=0, column=0, padx=20, pady=10)
        self.nameEntry = Entry(add, width=25)
        self.nameEntry.grid(row=0, column=1, pady=10)

        idLabel = Label(add, text='Unique Code', width=15).grid(row=1, column=0, padx=20, pady=10)
        self.idEntry = Entry(add, width=25)
        self.idEntry.grid(row=1, column=1, pady=10)

        phoneLabel = Label(add, text='Phone No.', width=10).grid(row=2, column=0, padx=20, pady=10)
        self.phoneEntry = Entry(add, width=25)
        self.phoneEntry.grid(row=2, column=1, pady=10)

        emailLabel = Label(add, text='Email', width=10).grid(row=3, column=0, padx=20, pady=10)
        self.emailEntry = Entry(add, width=25)
        self.emailEntry.grid(row=3, column=1, pady=10)

        dobLabel = Label(add, text='Date of Birth', width=10).grid(row=4, column=0, padx=20, pady=10)
        self.dobEntry = Entry(add, width=25)
        self.dobEntry.grid(row=4, column=1, pady=10)

        genderlabel = Label(add, text="Gender", width=10).grid(row=5, column=0, padx=20, pady=10)
        self.genderbox = ttk.Combobox(add, textvariable=self.gender, values=["Male", "Female", "Other"], width=22)
        self.genderbox.grid(row=5, column=1, pady=10)
        self.genderbox.current(0)

        jobLabel = Label(add, text='Job/Post', width=10).grid(row=6, column=0, padx=20, pady=10)
        self.jobEntry = Entry(add, width=25)
        self.jobEntry.grid(row=6, column=1, pady=10)

        addressLabel = Label(add, text='Address', width=10).grid(row=7, column=0, padx=20, pady=10)
        self.addressEntry = Text(add, width=19, height=5)
        self.addressEntry.grid(row=7, column=1, pady=10)

        #Buttons
        modifyButton = Button(add, text='Modify ', width=10, command='#')
        modifyButton.place(x=400, y=340)
        datasetButton = Button(add, text='Take Photo', width=10, command=self.add_person)
        datasetButton.place(x=500, y=340)
        saveButton = Button(add, text='Save', width=10, command=partial(self.addData,self.data))
        saveButton.place(x=600, y=340)

        #Frame for Refernce Image
        self.photoFrame = Frame(add, width=300, height=320, bg='grey')
        self.photoFrame.place(x=380, y=10)

        add.mainloop()

    def add_person(self):
        """
        Opens Camera and captures 100 images for training.
        These images are saved to special ID named directory.
        ID is taken as Input from add person window
        Each person has individual directory.
        :return: Camera window
        This raises a warning, which is bug from OpenCV module.
        """
        cap = cv2.VideoCapture(0)
        self.count =0
        try:
            # Collect 100 samples of your face from webcam input
            while True:
                flag, frame = cap.read()

                self.count += 1
                face = cv2.resize(frame, (600, 500))
                # face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                # Save file in specified directory with unique name
                file_name_path = './Datasets/Train/Chetan/' + str(self.count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                # Put count on images and display live count
                cv2.putText(face, str(self.count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Data Collecter', face)

                if cv2.waitKey(1) == 13 or self.count == 100:  # 13 is the Enter Key
                    break
        except:
            message('Error occured','Please the application')
            pass

    def addData(self,data,filename="DataBase.json"):
        """
        Get the user information from the widgets and adds to Database
        Will popup message indicating error and exit the function , if data is not provided in required format.
        return: Error message
        """
        #Initialize empty variables to store values later

        #Will the format the data in required json format
        self.addingDict = {}

        #append the data_dict, thus making list of data tags vlaues
        self.templist = []

        self.data_tags = [ self.idEntry.get(),self.nameEntry.get(),self.phoneEntry.get()
            , self.emailEntry.get(), self.dobEntry.get(), self.genderbox.get(), self.jobEntry.get()
            , self.addressEntry.get('1.0', END)]

        if not self.data_tags[0].isdecimal():
            return message("Invalid Data Entry","Unique Code must be numeric entry")

        if not self.data_tags[1].isalpha():
            return message("Invalid Data Entry", "Name must be non-numeric entry")

        if not self.data_tags[0].isdecimal() and (len(self.data_tags)==10 or len(self.data_tags)==13):
            return message("Invalid Data Entry","Contact Number must be numeric entry with 10 digits or 12 digits")

        if self.data_tags[4].find('@') == -1:
            return message("Invalid Data Entry", "Please enter proper email")

        if not self.genderbox.get()=='Male' or self.genderbox.get()=='Female' or self.genderbox.get()=='Other':
            return message("Invalid Data Entry","Please enter proper Gender")

        #cleaning the data_tags
        with open(filename, 'w') as f:
            self.dataDict = {
                             "_id":self.data_tags[0],
                             "name": self.data_tags[1],
                             "phoneNo": self.data_tags[2],
                             "email":self.data_tags[3],
                             "Date of Birth":self.data_tags[4],
                             "Gender":self.data_tags[5],
                             "job/post/status":self.data_tags[6],
                             "Address":self.data_tags[7],
                             }
            print(self.dataDict)
            self.templist.append(self.dataDict)
            self.addingDict = {self.data_tags[0]: self.templist}
            data.update(self.addingDict)
            json.dump(data,f, indent=4)

    def find_data(self):
        '''
        finds the  required user information
        return: None
        '''
        self.findId = self.idEntry.get()
        info = self.data.get(str(self.findId))
        for _ in info:
            for value in _.values():
                print(value)

surv = Survellance

# Widgets :-
# 1. Canvas
buttonCanvas = Canvas(model, bg='blue', width=200, height=480).grid(row=0, column=0, padx=10, pady=10)

# 2. Buttons
startSurv = Button(model, text='Start Survellance', width=15, command=Survellance).place(x=50, y=25)
endSurv = Button(model, text='End Survellance', width=15, command=surv.endSurvellance).place(x=50, y=65)
addPerson = Button(model, text='Add Person', width=15, command=add).place(x=50, y=145)
removePerson = Button(model, text='Remove Person', width=15).place(x=50, y=185)
Setting = Button(model, text='Setting', width=15).place(x=50, y=225)
snapshot = Button(model, text='Snapshot', width=15).place(x=50, y=265)
help = Button(model, text='Help', width=15, command=documentation).place(x=50, y=305)
quit = Button(model, text='Quit', width=15, command=exit).place(x=50, y=385)

# 3. comboBox for Source Detection
selectModelLabel = Label(model, text="Model", width=6).place(x=40, y=105)
selectmodelbox = ttk.Combobox(model, textvariable=models,
                              values=['Face and Mask', "Face Detection", 'Mask Detection', 'Temp'], width=13)
selectmodelbox.place(x=90, y=105)
selectmodelbox.current(3)

sourcelabel = Label(model, text="Source", width=6).place(x=40, y=345)
sourcebox = ttk.Combobox(model, textvariable=source, values=["Webcam", "Source 1", "Add media"], width=10)
sourcebox.place(x=90, y=345)
sourcebox.current(0)

# 4. listboxes and respective Frames
detect = Frame(model, width=300, height=480)
detect.place(x=220, y=10)
detectScrollbar = Scrollbar(detect)
detectScrollbar.pack(side=RIGHT, fill=Y)
detectListBox = Listbox(detect, width=40, height=28, font=("Verdana", 10), yscrollcommand=detectScrollbar)
detectListBox.pack(side=LEFT, fill=BOTH)
detectScrollbar.config(command=detectListBox.yview)

details = Frame(model, width=300, height=480)
details.place(x=560, y=10)
detailsScrollbar = Scrollbar(details)
detailsScrollbar.pack(side=RIGHT, fill=Y)
detailsListBox = Listbox(details, width=40, height=28, font=("Verdana", 10), yscrollcommand=detectScrollbar)
detailsListBox.pack(side=LEFT, fill=BOTH)
detailsScrollbar.config(command=detailsListBox.yview)

model.mainloop()
