import csv

theirfeatureNames = ["bolum","fakulte","universite","burs","sehir","dil","score_last","range_last","score_first","range_first","faculty_member_count","year","enrollment","capacity","Oran","demand","ratio_same_city","number_same_city","average_range","min_range","average_score","min_score","range_average_demand","range_first_demand","number_first_preference_enrollment","number_three_preference_enrollment","number_ten_preference_enrollment","enroll_average_range","number_preference_same_city","number_preference_same_department","total_preference","average_enrollment_rate_same_faculty_university","average_enrollment_rate_same_university","average_enrollment_rate_same_department_private_universities","average_enrollment_rate_same_department_state_universities","demand_capacity_same_department_private_universities","demand_capacity_same_department_state_universities","demand_capacity_same_faculty_university","average_demand_change_percentage_years_same_department","faculty_student_ratio_in_university"]

fileToMap = input("Enter the file name: ")
file = open(fileToMap, "r", encoding="utf-8")
csvreaderFileToMap = csv.DictReader(file, fieldnames=theirfeatureNames)

featurenames = ["academicYear", "universityName", "universityType","faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount"]

mappedFileName = fileToMap.replace(".csv", "") + "(mapped)" + ".csv"
newFile = open(mappedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.DictWriter(newFile, fieldnames=featurenames)


tempDict = {}
for i in featurenames:
    tempDict[i] = None

csvwriter.writeheader()
for index,row in enumerate(csvreaderFileToMap):
    if index != 0:
        for i in featurenames:
            tempDict[i] = None
        tempDict["academicYear"] = row["year"]
        tempDict["universityName"] = row["universite"]
        #tempDict["universityType"]
        tempDict["faculty"] = row["fakulte"]
        tempDict["departmentName"] = row["bolum"]
        #tempDict["idOSYM"]
        #tempDict["programType"]
        tempDict["language"] = row["dil"]
        tempDict["scholarshipRate"] = row["burs"]
        tempDict["quota"] = row["capacity"] 
        tempDict["occupiedSlots"] = row["enrollment"]
        #tempDict["tuitionFee"]
        #tempDict["universityFoundingYear"]
        #tempDict["facultyFoundingYear"]
        tempDict["universityLocation"] = row["sehir"]
        #tempDict["universityRegion"]
        #tempDict["profCount"]
        #tempDict["assoCount"]
        #tempDict["docCount"]
        tempDict["baseRanking"] = row["range_last"]
        tempDict["topRanking"] = row["range_first"]
        tempDict["avgAdmissionRanking(TYT)"] = row["average_range"]
        tempDict["baseAdmissionRanking(TYT)"] = row["min_range"]
        #tempDict["stdDeviationStudents"]
        #tempDict["revenue"]
        tempDict["outOfCityStudentRate"] = row["ratio_same_city"] #Have to substract from 100 since reverse
        #tempDict["sameRegionStudentRate"]
        tempDict["totalPreference"] = row["demand"]
        #tempDict["weightedPreference"]
        tempDict["top1PreferenceRatio"] = row["range_first_demand"]
        #tempDict["top3PreferenceRatio"]
        #tempDict["top9PreferenceRatio"]
        tempDict["avgOrderofPreference"] = row["range_average_demand"]
        #tempDict["tuitionFeeIncrease"]
        tempDict["avgAdmittedStudentPrefOrder"] = row["enroll_average_range"]
        tempDict["top1AdmittedRatio"] = row["number_first_preference_enrollment"] #Have to be changed to ratio
        tempDict["top3AdmittedRatio"] = row["number_three_preference_enrollment"] #Have to be changed to ratio
        tempDict["top10AdmittedRatio"] = row["number_ten_preference_enrollment"] #Have to be changed to ratio
        #tempDict["admittedPrefTrendRatio"]
        #tempDict["admittedGovPref"]
        #tempDict["admittedPrivPref"]
        tempDict["admittedTotalPref"] = row["total_preference"]
        tempDict["admittedTotalDepartmentPref"] = row["number_preference_same_department"]
        #tempDict["currentStudentCount"]
        csvwriter.writerow(tempDict)
    
    
    