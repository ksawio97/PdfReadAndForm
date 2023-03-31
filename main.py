from functions import *
#installs PyPDF2 if it doesn't exist
Install("PyPDF2")

inputDir = "pdf"
files = tuple(GetPdfFiles(inputDir))

texts = ReadPdfFiles(files, inputDir)

outputDir = "output/"
for i, text in enumerate(texts):
    foundDays = sum(list((map(lambda word: FindAllInStr(text, word), ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"]))), [])
    tables = list(map(lambda text: FormText(text), list(GetTablesFromText(text, foundDays))))
    WriteToFile(tables, outputDir + files[i].split(".")[0])