import subprocess
import sys
import os
from PyPDF2 import PdfReader

def Install(package: str):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def GetPdfFiles(inputDir):
    for file in os.listdir(path=inputDir):
        if file.endswith(".pdf"):
            yield file

def ReadPdfFiles(files, inputDir):
    for file in files:
        reader = PdfReader(inputDir + "/" + file)
        page = reader.pages[0]
        yield page.extract_text()


def FindAllInStr(text: str, word: str):
    found = text.find(word)
    daysIndexes = [found]
    while found != -1:
        text = text[daysIndexes[-1] + len(word) + 1:]
        found = text.find(word)
        daysIndexes.append(found + daysIndexes[-1])       
    
    return daysIndexes[:-1]

def GetTablesFromText(text: str, indexes: list):
    indexes.append(-1)
    for i in range(1, len(indexes)):
        yield text[indexes[i - 1] : indexes[i] - 4]

def FormHeader(tableStr):
    return map(lambda section: section.replace(",", " |") if "," in section else section, tableStr[:tableStr.find("\n")].split("  "))

def FormBody(tableStr):
    rest = tableStr.split("  ")

    body = []
    #fix this weird bug with col Przedmiot
    for i, line in enumerate(rest):
        if line.startswith("/") and line.endswih("/"):
            body[-1] += rest[i]
        else:
            body.append(line)
   
    return body

def FormText(tableStr):
    #header
    header = FormHeader(tableStr)
    result = " | ".join(header) + "UWAGI \n"

    #cleanup after forming header
    tableStr = tableStr[tableStr.find("\n") + 1:]
    
    #body
    body = FormBody(tableStr)
    result += " | ".join(body)

    return '[row][col size = 12 screen="sm"]\n[table width="100%" head="true"]\n' + result + "[/table]\n[/col]\n[/row]"

def WriteToFile(texts: list, name: str):
    text = "\n".join(texts)
    with open(f"{name}.txt", "w", encoding='utf-8') as fh:
        fh.write(text)
