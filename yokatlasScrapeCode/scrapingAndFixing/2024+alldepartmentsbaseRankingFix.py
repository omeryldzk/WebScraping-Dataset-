import csv

updated_features = ["academicYear", "universityName", "universityType","faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount", "baseScore", "topScore"]

fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.DictReader(file, fieldnames=updated_features)

newFile = open(fileToFix.replace(".csv", "") + "(fixed5)" + ".csv", "w", newline="", encoding="utf-8")
csvwriter = csv.DictWriter(newFile, fieldnames=updated_features)

csvwriter.writeheader()

tempDict = {}
for i in updated_features:
    tempDict[i] = ""
    
for index, row in enumerate(csvreaderFileToFix):
    if index == 0:
        continue
    for i in updated_features:
        tempDict[i] = ""
    for col in ["baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)"]:
        if row[col] != "" or row[col] != "Dolmadı" and row[col].find(".") != -1:
            while len(row[col]) - row[col].rfind(".") - 1  < 3:
                row[col] = row[col] + "0"
            row[col] = row[col].replace(".", "")
    for i in updated_features:
        tempDict[i] = row[i]
    csvwriter.writerow(tempDict)
        