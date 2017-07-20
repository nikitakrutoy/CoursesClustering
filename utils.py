import os
import subprocess
import csv
import re
import codecs
import logging

def isCreated(dir):
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)


# Переводит pdf файлы из папки currnet_dir/pdf
# В текст и записывает в файлы в папке currnet_dir/txt
def pdf_to_txt():
    # Берем список файлов в текущей папке
    currentDir = os.getcwd()
    isCreated("pdf")
    isCreated("txt")
    pdfDir = currentDir + "/pdf/"
    txtDir = currentDir + "/txt/"
    files = os.listdir(pdfDir)
    # Фильтруем файлы расширения .pdf и запихиваем в список
    pdfFiles = [pdfDir + i for i in filter(lambda file: file.endswith('.pdf'), files)]

    # Переписываем файлы .pdf в .txt
    for pdfFile in pdfFiles:
        pdfFileName = pdfFile.split("/")[-1].split(".")[0]
        textFile = txtDir + pdfFileName + '.txt'
        # print(pdfFile, textFile)
        subprocess.call(['pdftotext', pdfFile, textFile, '-enc', 'UTF-8'])


# Custom json_to_csv
def json_to_csv(data):
    csvfile = csv.writer(open("data.csv", 'w', newline=''))

    features = list()

    for dictionary in data:
        for key in dictionary:
            if key not in features:
                features.append(key)


    # Write CSV Header, If you dont need that, remove this line
    csvfile.writerow(features)

    for dictionary in data:
        row = [dictionary.get(key, None) for key in features]
        csvfile.writerow(row)


def test_regexp(disciplinesPattern, contentPattern):
    currentDir = os.getcwd()
    txtDir = currentDir + "/txt"
    courses = os.listdir(txtDir)
    disciplinesCounter = 0
    contentCounter = 0
    for course in courses:
        filename = txtDir + "/" + course
        with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as f:
            text = f.read()

        brokenPattern = "kek"
        result = re.search(disciplinesPattern, text)
        if result is None:
            disciplinesCounter += 1
            logging.debug(course + " - disciplines not parsed")
        result = re.search(contentPattern, text)
        if result is None:
            contentCounter += 1
            logging.debug(course + " - content not parsed")
    logging.debug("Disciplines not found in " + str(disciplinesCounter) + " files")
    logging.debug("Content not found in " + str(disciplinesCounter) + " files")
    logging.debug("Number of courses: " + str(len(courses)))

def get_rid_of_shitty_lines(doc):
    shittyLinesPattern = "Национальный исследовательский университет «Высшая школа экономики» Программа дисциплины.*для направления.*подготовки бакалавра"
    with open(doc, "r") as f:
        text = f.read()
        result = re.search(shittyLinesPattern, text)
        logging.debug(result.group(0))

def clearDocuments():
    currentDir = os.getcwd()
    txtDir = currentDir + "/txt"
    courses = os.listdir(txtDir)
    get_rid_of_shitty_lines()
