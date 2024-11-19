import csv

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed8)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


count = 0
for department in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(department)
        count += 1
        continue
    if department[35] == "%" or department[35] == "":
        department[35] = "%0,0"
    if department[36] == "%" or department[35] == "":
        department[36] = "%0,0"
    if department[37] == "%" or department[35] == "":
        department[37] = "%0,0"
    csvwriter.writerow(department)