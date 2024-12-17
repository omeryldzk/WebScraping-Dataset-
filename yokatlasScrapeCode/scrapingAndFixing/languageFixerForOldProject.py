import csv


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
        index = row[4].find(language[1])
        if index != -1:
            row[4] = row[4]. replace("(" + language[1] + ")", "") 
            row[7] = language[1]
    
    csvwriter.writerow(row)