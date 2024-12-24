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

fileToFix = "new2019-2024(fixed4).csv"
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.DictReader(file, fieldnames=updated_features)

helperFile = "2019-2024.csv"
helperFile = open(helperFile, "r", encoding="utf-8")
csvreaderHelper = csv.DictReader(helperFile, fieldnames=updated_features)


newFile = open(fileToFix.replace(".csv", "") + "(fixed5)" + ".csv", "w", newline="", encoding="utf-8")
csvwriter = csv.DictWriter(newFile, fieldnames=updated_features)

tempDict = {}
for i in updated_features:
    tempDict[i] = ""


csvwriter.writeheader()

for index, row in enumerate(csvreaderFileToFix):
    if index == 0:
        continue
    for i in updated_features:
        tempDict[i] = ""
    for i in updated_features:
        tempDict[i] = row[i]
    if row["academicYear"] == "2024":
        for helperRow in csvreaderHelper:
            if helperRow["academicYear"] == "2024":
                if row["idOSYM"] == helperRow["idOSYM"]:
                    for i in updated_features:
                        tempDict[i] = helperRow[i]
                    break
    csvwriter.writerow(tempDict)
        