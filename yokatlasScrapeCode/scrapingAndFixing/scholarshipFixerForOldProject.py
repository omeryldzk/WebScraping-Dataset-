import csv


fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed4)" + ".csv"
newFile = open(fixedFileName, "w", newline="")
csvwriter = csv.writer(newFile)

count = 0
for row in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(row)
        count += 1
        continue
    scholarship = row[8]
    row[4].replace("("+row[8]+")","")
    if row[8] == "Ücretsiz":
        row[8] = ""
    elif row[8] == "Burslu":
        row[8] = 100
    elif row[8] == "50 İndirimli":
        row[8] = 50
    elif row[8] == "25 İndirimli":
        row[8] = 25
    elif row[8] == "75 İndirimli":
        row[8] = 75
    elif row[8] == "Ücretli":
        row[8] = 0
    csvwriter.writerow(row)