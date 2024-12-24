import csv
from fixFunctions import *


fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed4)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)

langFile = open("languages.csv", "r", encoding="utf-8")
csvreaderLang = csv.reader(langFile)


# for row in csvreaderFileToFix:
#     if row[3].find("(KKTC Uyruklu)") != -1:
#         if row[4].find("(KKTC Uyruklu)") == -1:
#             row[4] = row[4] + "(KKTC Uyruklu)"
#         row[3] = row[3].replace("(KKTC Uyruklu)", "")

wantedWords = ["25 İndirimli", "Burslu", "50 İndirimli", "Ücretli", "75 İndirimli", "Fakülte", "Yüksekokul"]

for langrow in csvreaderLang:
    wantedWords.append(langrow[1])

for row in csvreaderFileToFix:
    for i in range(3,5):
        for a in range(0,3):
            for word in wantedWords:
                if row[i].find(word) != -1:
                    row[i] = row[i].replace("("+word+")", "")
            
                    
    csvwriter.writerow(row)
                    
                    
                    
        
        