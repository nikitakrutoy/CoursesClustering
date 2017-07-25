# pycodestyle -W291
# coding=utf-8
from bs4 import BeautifulSoup
import requests
import json
import os
import logging
import logging.config

import coloredlogs

from utils import *
from tst import test1

coloredlogs.install(level='DEBUG')

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'scrapy': {
            'level': 'DEBUG',
        },
    }
}


logging.config.dictConfig(DEFAULT_LOGGING)


def isLastPage(soup):
    header2 = soup.find(
        "div",
        {"class": "first_child last_child test"}).find("h2")
    return header2.string.strip() == u"По вашему запросу ничего не найдено"


def isField(tag):
    return (tag.name == "div") and (tag.find("span") is not None)


def get_rid_of_duplicates(program):
    logging.debug("getting rid of duplicates")
    pop_list = set()
    for i in range(len(program)):
        course = program[i]
        for j in range(len(program)):
            if j != i and course == program[j]:
                pop_list.add(j)
    for index in pop_list:
        program.pop(index)
    logging.debug("popped " + str(len(pop_list)) + " duplicates")
    return program


# Перебираем страницы page1.html, page2.html и тд.
# Сущестование страницы проверяем функцией isLastPage
# Если не сущетвует выходим из функции
def parse():
    program = []
    page = 0
    URL = "https://www.hse.ru/edu/courses/page{0}.html?language=&edu_level=78397&full_words=&genelective=-1&xlc=&words=&level=1191462%3A130721827&edu_year=2016&filial=22723&mandatory=&is_dpo=0&lecturer="
    while True:
        page += 1
        url = URL.format(page)
        response = requests.post(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if isLastPage(soup):
            return get_rid_of_duplicates(program)
        courses = soup.find_all(
            "div",
            {"class": "first_child last_child b-program__inner"})
        for course in courses:
            # Берем все значения, кроме года потому что его неудобно парсить))00)0
            courseDescription = {}
            courseName = course.find("h2").string.strip()
            courseDescription["Название"] = courseName.strip()
            # Уберем ненужные теги
            course = course.find("div", {"class": "last_child data"})
            #Описания
            fields = course.find_all(isField)
            for field in fields:
                data = []   # strings in tag
                #  Костыль чтобы вытащить из тэга его текст
                #  и текст внутреннго тэга, не нашел как сделать проще(((
                for string in field.strings:
                    string = string.strip()
                    # Проверка на пустую строку
                    if string:
                        data.append(string)
                # Убираем двоеточие в конце
                data[0] = data[0][:len(data[0]) - 1]
                key = data[0]
                value = data[1]
                if key == u"Преподаватель" or key == u"Преподаватели":
                    # Забираем имена преподавателей из всех ссылок данного поля
                    key = u'Преподаватели'
                    links = field.find_all("a")
                    teachers = set([link.string for link in links if link.string])Ø
                    courseDescription[key] = teachers
                elif key == u"Автор" or key == u"Авторы":
                    # Забираем имена авторов из всех ссылок данного поля
                    key = u'Авторы'
                    links = field.find_all("a")
                    authors = [link.string for link in links if link.string]
                    courseDescription[key] = authors
                elif key == u"Прогр. уч. дисц.":
                    pdf_link = field.find_all("a", limit=2)
                    pdf_link = pdf_link[1]
                    courseDescription[key] = pdf_link["href"]
                else:
                    courseDescription[key] = data[1]

            program.append(courseDescription)


def write_json(data):
    logging.debug("writing json")
    file = open("data.json", "w")
    json.dump(data, file, ensure_ascii=False)
    file.close()


def download(data):
    host = "https://www.hse.ru/"
    currentDir = os.getcwd()
    try:
        os.stat("pdf")
    except:
        os.mkdir("pdf")
    pdfDir = currentDir + "/pdf/"

    id = 0
    for course in data:
        id += 1
        course["id"] = id
        if u"Прогр. уч. дисц." in course:
            url = host + course[u"Прогр. уч. дисц."]
            logging.debug("Download started")
            response = requests.get(url)
            logging.debug("Download finished")
            filepath = pdfDir + course["Название"] + ".pdf"
            with open(filepath, "wb") as pdf:
                pdf.write(response.content)


if __name__ == "__main__":
    data = parse()
    # with open("data.json", "r") as temp:
        # data = json.load(temp)
        # temp.close()
    download(data)
    pdf_to_txt()
    add_text_data(data)
    write_json(data)
    json_to_csv(data)
    # test1()
