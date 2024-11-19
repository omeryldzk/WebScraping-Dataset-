import csv

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed6)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


count = 0
for department in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(department)
        count += 1
        continue
    if str(department[27]).find(".") != -1:
        length = len(str(department[27]))
        indexOfDot = str(department[27]).find(".")
        decimalsAfterDot = length - indexOfDot - 1
        zerosToBeAdded = 3 - decimalsAfterDot
        if zerosToBeAdded != 0:
            department[27] = str(department[27]).replace(".", "") + "0"*zerosToBeAdded
        else:
            department[27] = str(department[27]).replace(".", "")
    csvwriter.writerow(department)