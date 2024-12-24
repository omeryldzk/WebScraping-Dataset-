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

theirfeatureNames = ["bolum","fakulte","universite","burs","sehir","dil","score_last","range_last","score_first","range_first","faculty_member_count","year","enrollment","capacity","Oran","demand","ratio_same_city","number_same_city","average_range","min_range","average_score","min_score","range_average_demand","range_first_demand","number_first_preference_enrollment","number_three_preference_enrollment","number_ten_preference_enrollment","enroll_average_range","number_preference_same_city","number_preference_same_department","total_preference","average_enrollment_rate_same_faculty_university","average_enrollment_rate_same_university","average_enrollment_rate_same_department_private_universities","average_enrollment_rate_same_department_state_universities","demand_capacity_same_department_private_universities","demand_capacity_same_department_state_universities","demand_capacity_same_faculty_university","average_demand_change_percentage_years_same_department","faculty_student_ratio_in_university"]

oldDataset = "dataset.csv"
oldDatasetFile = open(oldDataset, "r", encoding="utf-8")
csvreaderOldDataset = csv.DictReader(oldDatasetFile, fieldnames=theirfeatureNames)

updated_features = ["academicYear", "universityName", "universityType","faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount", "baseScore", "topScore"]


fixedFileName = fileToFix.replace(".csv", "") + "(fixed7)" + ".csv"
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
    for index2, theirfeature in enumerate(csvreaderOldDataset):
        if index2 == 0:
            continue
        tempDict["baseScore"] = theirfeature["score_last"].replace(",",".")
        tempDict["topScore"] = theirfeature["score_first"].replace(",",".")
        break
        
    csvwriter.writerow(tempDict)
