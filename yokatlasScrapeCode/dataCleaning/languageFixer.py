import csv

from pygments.lexers.csound import newline

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed)" + ".csv"
newFile = open(fixedFileName, "w")
csvwriter = csv.writer(newFile)

lang_file = open("languages.csv", "r", encoding="utf-8")
csvreaderLanguages = csv.reader(lang_file)

count = 0
for row in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(row)
        count += 1
        continue
    departmentName = row[4]
    index = departmentName.find("(")
    language = ""
    if index != -1:
        index2 = departmentName.find(")")
        language = departmentName[index+1:index2]
        languageChecker = False
        lang_file.seek(0)
        for lang in csvreaderLanguages:
            if lang[1] == language:
                languageChecker = True
                break
        if languageChecker:
            row[4] = departmentName.replace(" ("+language+")", "")
            row[7] = language
            csvwriter.writerow(row)
            newFile.flush()
        else:
            csvwriter.writerow(row)
    elif row[7] == "English":
        row[7] = "İngilizce"
        csvwriter.writerow(row)
        newFile.flush()
    elif row[7] == "Turkish":
        row[7] = "Türkçe"
        csvwriter.writerow(row)
        newFile.flush()