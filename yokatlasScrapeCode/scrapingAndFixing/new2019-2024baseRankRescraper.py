import csv
from selenium import webdriver
import platform

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fixFunctions import *

updated_features = ["academicYear", "universityName", "universityType","faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount", "baseScore", "topScore"]



fileToFix = "updated_2019-2024(withIDs)(fixed).csv"
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.DictReader(file, fieldnames=updated_features)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed2)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.DictWriter(newFile, fieldnames=updated_features)

if platform.system() == "Darwin":
    path = '../resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
    
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService)
wait = WebDriverWait(driver, 30)

tempDict = {}
for i in updated_features:
    tempDict[i] = ""
    
csvwriter.writeheader()


for index,row in enumerate(csvreaderFileToFix):
    if index == 0:
        continue
    for i in updated_features:
        tempDict[i] = ""
        
    for i in updated_features:
        tempDict[i] = row[i]
    
    if row["academicYear"] == "2024.0":
        baseRankingg = row["baseRanking"]
        if (row["baseRanking"] == "" and row["topRanking"] != "") or (row["baseRanking"] == "---"):
            idOsym = row["idOSYM"]
            link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + idOsym
            driver.get(link)
            closePopUp(driver, wait)
            openAll(driver, wait)
            wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1070"]""")))
            lastPersonSection = driver.find_element(By.XPATH, """//div[@id="icerik_1070"]""")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1070 table""")))
            table = lastPersonSection.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
            rows = table.find_elements(By.XPATH, """.//tr""")
            baseRanking = ""
            for row2 in rows:
                cols = row2.find_elements(By.XPATH, """.//td""")
                if cols[0].text == "Yerleştiği Başarı Sırası*" or cols[0].text == "Yerleştiği Başarı Sırası *":
                    baseRanking = cols[1].text
            tempDict["baseRanking"] = baseRanking
    csvwriter.writerow(tempDict)
    newFile.flush()
                