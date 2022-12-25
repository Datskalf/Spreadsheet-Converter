import tkinter as tk
from tkinter import filedialog as fd
import os

import csv
import json

WINDOW_SIZE = "600x400"
SUPPORTED_FILETYPES = [
    {
        "Name": "CSV",
        "Extension": "*.csv"
    },
    {
        "Name": "JSON",
        "Extension": "*.json"
    },
    {
        "Name": "Excel worksheet",
        "Extension": "*.xlsx"
    }
]

inputfile = ""



def openInputFile() -> None:
    global inputfile, inputFileLabelText

    filetypes = [(f"{ft['Name'].lower()} files", ft['Extension']) for ft in SUPPORTED_FILETYPES]
    #for t in SUPPORTED_FILETYPES:
    #    filetypes.append((f"{t.lower()} files", f"*.{t.lower()}"))
    filetypes.append(("all files", "*.*"))
    

    inputfile = fd.askopenfilename(
        title="Select spreadsheet file",
        initialdir = os.path.expanduser('~/Documents'),
        filetypes=tuple(filetypes)
    )

    inputFileLabelText.set(inputfile.split('/')[-1])

def openOutputFile() -> str:
    outputfile = fd.askopenfilename(
        title="Select output file",
        initialdir=os.path.expanduser('~/Documents'),
        filetypes=SUPPORTED_FILETYPES
    )

    return outputfile

    


def convert() -> None:
    global inputfile
    outputfile = openOutputFile()

    filetypeIn = inputfile.split('.')[-1]
    filetypeOut = outputfile.split('.')[-1]

    data = []



    #################################### Read data ####################################
    with open(inputfile) as fileIn:
        if filetypeIn == 'csv':
            reader = csv.reader(fileIn)
            for row in reader:
                data.append(row)
    


    #################################### Write data ###################################
    with open(outputfile) as fileOut:
        if filetypeOut == 'csv':
            writer = csv.writer(fileOut)
            for line in data:
                writer.writerow(line)
        
        


top = tk.Tk()
top.title("Spreadsheet Converter")
top.geometry(WINDOW_SIZE)

###### Input
inputFrame = tk.Frame(top, pady=16)
inputFrame.pack(side = tk.TOP, expand=False)

getInputFileButton = tk.Button(inputFrame, text="Load file to convert", command=openInputFile)
getInputFileButton.pack(side = tk.TOP)

inputFileTextLabel = tk.Label(inputFrame, text="Selected file: ")
inputFileTextLabel.pack(side = tk.TOP)

inputFileLabelText = tk.StringVar()
inputFileLabel = tk.Label(inputFrame, textvariable=inputFileLabelText)
inputFileLabel.pack(side = tk.TOP)



###### Output
outputFrame = tk.Frame(top, height=300)
outputFrame.pack(side = tk.TOP, expand=True)

radiobuttons = []
for i, key in enumerate(SUPPORTED_FILETYPES):
    radiobutton = tk.Radiobutton(outputFrame, text=key['Name'], value=key['Name'])
    radiobutton.pack(anchor='w')
    radiobuttons.append(radiobutton)
radiobuttons[0].select()

convertFileButton = tk.Button(outputFrame, text="Convert file", state=tk.DISABLED, command=convert)
convertFileButton.pack(side=tk.TOP)

top.mainloop()