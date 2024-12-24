import csv

fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)

for row in csvreaderFileToFix:
    if row[0] == "2024.0":
        percentRows = [25,26,29,30,31]
        a = [32,34]
        for i in percentRows:
            if row[i] != "":
                row[i] = str(float(row[i].replace("% ", "").replace(",","."))/10)
        for i in a:
            if row[i] != "":
                row[i] = row[i].replace(",",".")
    csvwriter.writerow(row)