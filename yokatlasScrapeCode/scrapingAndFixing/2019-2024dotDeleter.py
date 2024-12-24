import csv

fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed2)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)

for row in csvreaderFileToFix:
    cols = [19,20,21,22]
    for i in cols:
        if row[i] != "" or row[i] != "Dolmadı":
            if row[i].find(".") != -1:
                row[i] = row[i].replace(".","")
    csvwriter.writerow(row)