import csv

fileToFix = input("Enter the file name: ")
fileToFix = "..\\"+ fileToFix
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed1)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)
count = 0
for row in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(row)
        count+=1
        continue
    if row[0] == "2022":
        totalPreferenceCount = float(row[27])
        top9PrefCount = float(row[31])
        if top9PrefCount == 0:
            row[31] = "0"
        else:
            top9PrefRatio = top9PrefCount / totalPreferenceCount *10
            top9PrefRatioText = str(round(top9PrefRatio, 2))
            row[31] = top9PrefRatioText
            csvwriter.writerow(row)
    else:
        csvwriter.writerow(row)
