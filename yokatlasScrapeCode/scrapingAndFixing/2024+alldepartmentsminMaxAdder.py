import csv

old_features = ["academicYear", "universityName", "universityType", "faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount"]

fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.DictReader(file, fieldnames=old_features)

minMax2021_2023 = "2024+alldepartments(minMaxScore).csv"
minMax2021_2023File = open(minMax2021_2023, "r", encoding="utf-8")
csvreaderMinMax2021_2023 = csv.reader(minMax2021_2023File)

minMax2024 = "2024+alldepartments(minMaxScore2)(fixed).csv"
minMax2024File= open(minMax2024, "r", encoding="utf-8")
csvreaderMinMax2024 = csv.reader(minMax2024File)

updated_features = ["academicYear", "universityName", "universityType","faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount", "baseScore", "topScore"]


fixedFileName = fileToFix.replace(".csv", "") + "(fixed4)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
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
    for i in old_features:
        tempDict[i] = row[i]
    if row["academicYear"] == "2021":
        csvwriter.writerow(tempDict)
        continue
    elif row["academicYear"] == "2022" or row["academicYear"] == "2023":
        for minMaxRow in csvreaderMinMax2021_2023:
            rowIdOSYM = row["idOSYM"]
            minMaxIdOSYM = minMaxRow[0]
            if minMaxIdOSYM == rowIdOSYM:
                tempDict["baseScore"] = minMaxRow[1].replace(",", ".")
                tempDict["topScore"] = minMaxRow[2].replace(",", ".")
                break
    elif row["academicYear"] == "2024":
        for minMaxRow in csvreaderMinMax2024:
            if minMaxRow[0] == row["idOSYM"]:
                tempDict["baseScore"] = minMaxRow[1].replace(",", ".")
                tempDict["topScore"] = minMaxRow[2].replace(",", ".")
                break
    csvwriter.writerow(tempDict)
