import csv


featureNames = ["academicYear", "universityName", "universityType", "totalForeignStudents", "totalStudentNumber"]
compileFile = open("foreignStudentDataFinal.csv", mode="w", encoding="utf8")
compileCsv = csv.DictWriter(compileFile, fieldnames=featureNames ,delimiter=",")
compileCsv.writeheader()
tempDict = {}
for i in featureNames:
    tempDict[i] = None
academicYear = 2023
for i in range(0,2):
    foreignFile = open(".\\csv_files\\foreign" + str(academicYear - i) + "-" +str(academicYear + 1 - i) + ".csv", mode="r", encoding="utf8")
    foreignCsv = csv.reader(foreignFile, delimiter=',')
    tempName = ""
    tempType = ""
    studentFile = open(".\\csv_files\\studentCount" + str(academicYear - i) + "-" +str(academicYear + 1 - i) + ".csv", mode="r", encoding="utf8")
    studentCsv = csv.reader(studentFile, delimiter=',')
    #row[10] = studentCount
    tempForeignCount = 0
    tempStudentCount = 0
    for row in foreignCsv:
        tempName = row[0]
        tempName = tempName.removeprefix("\ufeff")
        tempForeignCount = tempForeignCount + int(row[6])
        tempType = row[1]
        for row2 in studentCsv:
            if tempName == row2[1]:
                tempStudentCount = row2[10]
                break
        break
    for row in foreignCsv:
        if tempName == row[0]:
            tempForeignCount += int(row[6])
        else:
            tempDict["academicYear"] = academicYear
            tempDict["universityName"] = tempName
            tempDict["universityType"] = tempType
            tempDict["totalForeignStudents"] = tempForeignCount
            tempDict["totalStudentNumber"] = tempStudentCount
            compileCsv.writerow(tempDict)
            tempForeignCount = int(row[6])
            tempName = row[0]
            tempType = row[1]
            compileFile.flush()
            if tempName == "TOPLAM":
                break
            for row2 in studentCsv:
                if tempName == row2[1]:
                    tempStudentCount = row2[10]
                    break            
        tempName = row[0]
        
    academicYear -= 1
            
            
    