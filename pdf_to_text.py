import os

def isCreated(dir):
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

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
        print(pdfFile, textFile)
        subprocess.call(['pdftotext', pdfFile, textFile, '-enc', 'UTF-8'])
