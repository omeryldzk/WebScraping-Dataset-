import csv

from numba.core.cgutils import false_bit

fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed3)" + ".csv"
newFile = open(fixedFileName, "w", newline="")
csvwriter = csv.writer(newFile)

lang_file = open("languages.csv", "r", encoding="utf-8")
csvreaderLanguages = csv.reader(lang_file)

count = 0
for row in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(row)
        count += 1
        continue
    langaugeMatch = False
    lang_file.seek(0)
    for language in csvreaderLanguages:
        if language[1] == row[7]:
            langaugeMatch = True
            break
    if row[7] != "" and langaugeMatch == False:
        row[4] = row[4] + " (" + row[7] + ")"
        row[7] = "Türkçe"
    elif row[7] == "":
        row[7] = "Türkçe"
    csvwriter.writerow(row)