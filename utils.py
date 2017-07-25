import os
import subprocess
import csv
import re
import codecs
import logging
from tqdm import tqdm
from lang import detect_language
from textblob import TextBlob
import operator

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
    for pdfFile in tqdm(pdfFiles):
        pdfFileName = pdfFile.split("/")[-1].split(".")[0]
        textFile = txtDir + pdfFileName.strip() + '.txt'
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
    parsedData = {}
    currentDir = os.getcwd()
    txtDir = currentDir + "/txt"
    courses = os.listdir(txtDir)
    disciplinesCounter = 0
    сontentCounter = 0
    for course in courses:
        textData = {}
        # print(course, len(courses))
        filename = txtDir + "/" + course
        with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as f:
            text = f.read()

        brokenPattern = "kek"
        disciplinesResult = re.search(disciplinesPattern, text, re.DOTALL)
        if disciplinesResult:
            disciplinesCounter += 1
            textData["discipline"] = disciplinesResult.group(1)
        else:
            logging.debug(course + " - disciplines not parsed")
        # else:
        #     logging.debug(result.group(1))

        # Ищем содержание дисциплины(проверяем на соответсвие одному из 2 наиболее встречаемых форматов)
        contentResult1 = re.search(contentPattern[0], text, re.DOTALL)
        contentResult2 = re.search (contentPattern[1], text, re.DOTALL)
        if contentResult1:
            сontentCounter += 1
            textData["content"] = contentResult1.group(1)
        elif contentResult2:
            сontentCounter += 1
            textData["content"] = contentResult2.group(1)
        else:
            logging.debug(course + " - content not parsed")
        courseName = course.split(".")[0]
        parsedData[courseName.strip()] = textData

    disciplinesAccuracy = disciplinesCounter/len(courses)
    contentAccuracy = сontentCounter/len(courses)
    logging.info("Disciplines accuracy: " + str(int(disciplinesAccuracy*100)) + "%" )
    logging.info("Content accuracy: " + str(int(contentAccuracy*100)) + "%")
    logging.info("Number of courses: " + str(len(courses)))
    return parsedData

def add_text_data(data):
    currentDir = os.getcwd()
    txtDir = currentDir + "/txt"
    for course in data:
        courseName = course["Название"]
        if u"Прогр. уч. дисц." in course:
            filename = txtDir + "/" + courseName + ".txt"
            with codecs.open(filename, "r", encoding='utf-8', errors='ignore') as f:
                textData = f.read()
                if detect_language(textData) == "english":
                    blob = TextBlob(textData)
                    textData = blob.translate(from_lang="en", to="ru").raw

                course["Text"] = textData




def add_discipline_data(data):
    disciplinesPattern1 = r"Место дисциплины в структуре образовательной программы\n*(.*)"
    contentPattern1 = r"Содержание (?:дисциплины|курса|программы)(.*)(?:Образовательные технологии|Оценочные средства для текущего контроля и аттестации студента|Образцы заданий по различным формам контроля|Основная литература )"
    conentPattern2 = r"Цели освоения (?:дисциплины|курса|программы)(.*)(?:Используемая и рекомендуемая литература)*"
    contentPatterns = [contentPattern1, conentPattern2]
    # contentPattern = "Содержание (?:дисциплины|курса|программы)\n*.*"
    parsedData = test_regexp(disciplinesPattern1, contentPatterns)
    print(len(data))
    for course in data:
        courseName = course["Название"]
        try:
            courseTextData = parsedData[courseName]
        except KeyError:
            pass
        if "discipline" in courseTextData:
            course["discipline"] = courseTextData["discipline"]
        if "content" in courseTextData:
            course["content"] = courseTextData["content"]


def get_rid_of_shitty_lines(doc):
    shittyLinesPattern = "Национальный исследовательский университет «Высшая школа экономики» Программа дисциплины.*для направления.*подготовки бакалавра"
    pass

def clear_documents():
    pass
