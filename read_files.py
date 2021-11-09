from tika import parser
import pandas as pd
import docx
import glob
import os
import PyPDF2


def read(file):
    read_pdf = PyPDF2.PdfFileReader(file)
    page_num = read_pdf.getNumPages()
    content = []
    for i in range(page_num):
        page = read_pdf.getPage(i)
        page_content = page.extractText()
        page_content = page_content.replace('\u2122', "'")
        content.append(page_content)
    return content


def readDataset(file_path):
    read_files = glob.glob(os.path.join(file_path, "*.*"))
    print(read_files)
    np_array_values = []
    for files in read_files:
        individual = files
        np_array_values.append(" ".join(readInputFile(individual)))
    print(np_array_values)
    return np_array_values


def getDocText(fileName):
    text = []
    doc = docx.Document(fileName)
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)


def readInputFile(individual):
    array_values = []
    st = ""
    if individual.endswith(".pdf"):
        with open(individual, 'rb') as pdfFileObj:  # Open lorem.txt for reading text
            raw = parser.from_file(pdfFileObj)
        array_values.append(raw['content'])
        # raw = read(individual)
        # for r in raw:
        #     st = st + (r.replace("\n", ""))
    if individual.endswith(".docx"):
        txt = getDocText(individual)
        array_values.append(txt)
    if individual.endswith(".txt"):
        with open(individual, 'rt', encoding='utf-8') as myfile:  # Open lorem.txt for reading text
            txt = myfile.read()  # Read the entire file to a string
        array_values.append(txt)
        myfile.close()
    if individual.endswith(".csv"):
        txt = pd.read_csv(individual, header=0, encoding='utf-8')
        array_values.append(txt)
    return array_values
