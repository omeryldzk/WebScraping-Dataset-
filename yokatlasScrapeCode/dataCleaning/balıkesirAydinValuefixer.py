import csv

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed5)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


count = 0
for department in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(department)
        count += 1
        continue
    if department[14] == "AYDIN" or department[14] == "BALIKESİR":
        department[25] = str(float(department[25].replace("%","").replace(",","")) / 100)
        department[26] = str(float(department[26].replace("%", "").replace(",", "")) / 100)
    csvwriter.writerow(department)