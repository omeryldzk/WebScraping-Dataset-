import csv

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed2)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)
count = 0
for row in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(row)
        count += 1
        continue
    else:
        if row[25] != "" and row[26] == "":
            row[26] = "0"
        elif row[25] == "" and row[26] != "":
            row[25] = "0"
        elif row[25] == "" and row[26] == "":
            if row[10] == "0":
                row[25] = "0"
                row[26] = "0"
            else:
                row[25] = "UNKNOWN"
                row[26] = "UNKNOWN"
    csvwriter.writerow(row)