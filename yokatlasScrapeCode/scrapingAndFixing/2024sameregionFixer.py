import csv

fileToFix = input("Enter the file name: ")
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
        if row[10] != "0":
            if row[26] == "" and row[25] != "":
                row[26] = "% 0,0"
            if row[25] == "" and row[26] != "":
                row[25] = "% 0,0"
            
    csvwriter.writerow(row)