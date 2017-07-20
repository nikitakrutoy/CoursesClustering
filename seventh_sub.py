# Достаем 7 тему из документа и пихаем в файл .txt
def seventh_sub(textFile):
    currentDir = os.getcwd()
    txtDir = currentDir + '/txt/' + textFile
    isCreated('text')
    
    try:
        with open(txtDir) as file:
            file = ' '.join(' '.join([str(line) for line in file]).split())
            subject = re.search(r'Содержание дисциплины(.+)8 Образовательные технологии', file, re.DOTALL).group(1)

            subjectFile = open('text/' + textFile, 'w')
            subjectFile.write(subject)
            subjectFile.close()
    except:
        return False
