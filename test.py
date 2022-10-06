from tkinter import *
import csv
import configparser
import os
import labels
from reportlab.graphics import shapes
from PyPDF2 import PdfFileReader
import subprocess
import customtkinter
from datetime import datetime

dataFile = os.path.dirname(os.path.abspath(__file__))+"\\data.txt"
ico = os.path.dirname(os.path.abspath(__file__))+"\\ddl.ico"

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")

master = customtkinter.CTk()
master.title('DDL Mini Portal')
master.geometry("700x550")
master.minsize(700,550)
master.maxsize(700,550)
master.iconbitmap(ico)

configParser = configparser.RawConfigParser()   
configFilePath = os.path.dirname(os.path.abspath(__file__))+"\\config.ini"
configParser.read(configFilePath)
printer = configParser.get('config' , 'printer')
acroread = configParser.get('config' , 'acroread')

patientList = []
patientDataHashMap = {}

specs = labels.Specification(45, 22, 1, 1, 45, 22, corner_radius=2)

class patientInfo:

    def __init__(self, name, dob, ssn, ma, intype):
        # Get the name and dob and orderdate info from pdf
        self.name = name
        self.dob = dob
        self.ssn = ssn
        self.ma = ma
        self.intype = intype

    def getName(self):
        return self.name

    def getDOB(self):
        return self.dob

    def getSSN(self):
        return self.ssn

    def getMA(self):
        return self.ma

    def getInType(self):
        return self.intype

def update(data):
    listBox.delete(0, END)

    for item in data:
        listBox.insert(END, item.getName() + " DOB: " + item.getDOB() + " SSN: " + item.getSSN())

def popUp(msg):
    popUp = Toplevel(master)
    popUp.title()
    popUp.geometry("450x200")
    popUp.minsize(450,200)
    popUp.maxsize(450,200)
    popUp.iconbitmap(ico)
    label = Label(popUp, text=msg, font=("Helvetica", 12), pady=50)
    label.pack()
    popUp.mainloop()

def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    label.add(shapes.String(3, 45, obj.getName(), fontName="Helvetica", fontSize=12))
    label.add(shapes.String(3, 30, "DOB: " + obj.getDOB(), fontName="Helvetica", fontSize=10))
    label.add(shapes.String(3, 15, dt_string, fontName="Helvetica", fontSize=10))

def printLabel(patient):
    label_path = os.path.dirname(os.path.abspath(__file__))+"\\label.pdf"
    sheet = labels.Sheet(specs, draw_label, border=True)
    sheet.add_label(patient)
    sheet.save(label_path)

    file = open(label_path, 'rb')
    readpdf = PdfFileReader(file)
    if(readpdf.numPages != 0): 
        cmd='"%s" /N /T "%s" "%s"'%(acroread,label_path,printer)  
        proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        
    file.close()

def addPatientFile(name_entry,dob_entry,ssn_entry,ma_entry,inType_entry,newPatientForm):
    if name_entry == '' or dob_entry == '':
        popUp("Name or DOB cannot be empty.")
    else:
        file = open(dataFile, "a")
        file.write("\n{},{},{},{},{}".format(name_entry,dob_entry,ssn_entry,ma_entry,inType_entry))
        file.close()
        updatePatientList()
        update(patientList)
        newPatientForm.destroy()
        popUp("Patient added successfully.")


def clear(name_entry,dob_entry,ssn_entry,ma_entry,inType_entry):
    name_entry.delete(0, END)
    dob_entry.delete(0, END)
    ssn_entry.delete(0, END)
    ma_entry.delete(0, END)
    inType_entry.delete(0, END)

def addPatient():
    newPatientForm = Toplevel(master)
    newPatientForm.title()
    newPatientForm.geometry("550x300")
    newPatientForm.iconbitmap(ico)
    title = Label(newPatientForm, text="Create a New Patient", font=("Helvetica", 16))
    title.grid(row=0, column=0, columnspan=2, pady="10")

    name_label = Label(newPatientForm, text="Name", font=("Helvetica", 12)).grid(row=1,column=0,sticky=W,padx=20)
    dob_label = Label(newPatientForm, text="Date of Birth", font=("Helvetica", 12)).grid(row=2,column=0,sticky=W,padx=20)
    ssn_label = Label(newPatientForm, text="SSN", font=("Helvetica", 12)).grid(row=3,column=0,sticky=W,padx=20)
    ma_label = Label(newPatientForm, text="MA#", font=("Helvetica", 12)).grid(row=4,column=0,sticky=W,padx=20)
    inType_label = Label(newPatientForm, text="Insurance Type", font=("Helvetica", 12)).grid(row=5,column=0,sticky=W,padx=20)

    name_entry = customtkinter.CTkEntry(master=newPatientForm,width=250,height=25,corner_radius=10)
    name_entry.grid(row=1,column=1)
    dob_entry = customtkinter.CTkEntry(master=newPatientForm,width=250,height=25,corner_radius=10)
    dob_entry.grid(row=2,column=1,padx=20)
    ssn_entry = customtkinter.CTkEntry(master=newPatientForm,width=250,height=25,corner_radius=10)
    ssn_entry.grid(row=3,column=1,padx=20)
    ma_entry = customtkinter.CTkEntry(master=newPatientForm,width=250,height=25,corner_radius=10)
    ma_entry.grid(row=4,column=1,padx=20)
    inType_entry = customtkinter.CTkEntry(master=newPatientForm,width=250,height=25,corner_radius=10)
    inType_entry.grid(row=5,column=1,padx=20)

    add_customer_button = customtkinter.CTkButton(newPatientForm, text="Add Patient", command=lambda:addPatientFile(name_entry.get(),dob_entry.get(),ssn_entry.get(),ma_entry.get(),inType_entry.get(),newPatientForm), height=30, width=200)
    add_customer_button.grid(row=6,column=0,padx=20,pady=20)
    clear_customer_button = customtkinter.CTkButton(newPatientForm, text="Clear", command=lambda:clear(name_entry,dob_entry,ssn_entry,ma_entry,inType_entry), height=30, width=200)
    clear_customer_button.grid(row=6,column=1,padx=20,pady=20)

    newPatientForm.mainloop()

def comprehensive(patientDetail):
    print("comprehensive button clicked")

def infoBox(event):
    searchBar.delete(0, END)
    try:
        print(listBox.get(listBox.curselection()))
    except:
        print("error")
        return

    patientDetail = patientDataHashMap.get(listBox.get(listBox.curselection()))
    infoBox = Toplevel(master)
    infoBox.title()
    infoBox.geometry("550x300")
    infoBox.iconbitmap(ico)
    nameLabel = Label(infoBox, text="Name: " + patientDetail.getName(), font=("Helvetica", 12))
    nameLabel.pack(pady=10)
    dobLabel = Label(infoBox, text="Date of Birth: " + patientDetail.getDOB(), font=("Helvetica", 12))
    dobLabel.pack(pady=10)
    sexLabel = Label(infoBox, text="SSN: " + patientDetail.getSSN(), font=("Helvetica", 12))
    sexLabel.pack(pady=10)
    MALabel = Label(infoBox, text="MA#: " + patientDetail.getMA(), font=("Helvetica", 12))
    MALabel.pack(pady=10)
    inTypeLabel = Label(infoBox, text="Insurance Type: " + patientDetail.getInType(), font=("Helvetica", 12))
    inTypeLabel.pack(pady=10)
    screenButton = customtkinter.CTkButton(infoBox, text="Screen", command=lambda: [printLabel(patientDetail), infoBox.destroy()], height=30, width=200)
    screenButton.pack(side=LEFT,pady=10,padx=35)
    sendButton = customtkinter.CTkButton(infoBox, text="Confirmation", command=lambda: [comprehensive(patientDetail), infoBox.destroy()], height=30, width=200)
    sendButton.pack(side=RIGHT,pady=10,padx=35)
    infoBox.mainloop()

def search(event):
    typed = searchBar.get()

    if typed == '':
        data = patientList
    else:
        data = []
        for item in patientList:
            if typed.lower() in item.getName().lower() or typed.lower() in item.getDOB().lower() or typed.lower() in item.getSSN().lower():
                data.append(item)

    print(typed)
    update(data)

def updatePatientList():
    with open(dataFile, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            pass
    patient = patientInfo(row['NAME'], row['DOB'], row['SSN'], row['MA#'], row['Insurance Type'])
    patientList.append(patient)
    patientDataHashMap.update({patient.getName() + " DOB: " + patient.getDOB() + " SSN: " + patient.getSSN() : patient})

def temp_text(e):
   searchBar.delete(0,"end")

with open(dataFile, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        patient = patientInfo(row['NAME'], row['DOB'], row['SSN'], row['MA#'], row['Insurance Type'])
        patientList.append(patient)
        patientDataHashMap.update({patient.getName() + " DOB: " + patient.getDOB() + " SSN: " + patient.getSSN() : patient})

searchBar = customtkinter.CTkEntry(master=master,width=350,height=35,corner_radius=10)
searchBar.insert(0, "Search patient by name, dob or ssn...")
searchBar.pack(pady=20)
listBox = Listbox(master, height=20, width=100, font=(14), bg='#d0dadb')
listBox.pack(padx=5)
button = customtkinter.CTkButton(master, text="Add New Patient", command=addPatient, height=30, width=200)
button.pack(pady=20)

if 1:
    update(patientList)

searchBar.bind("<FocusIn>", temp_text)
listBox.bind("<Double-1>", infoBox)
searchBar.bind("<KeyRelease>", search)
master.mainloop()