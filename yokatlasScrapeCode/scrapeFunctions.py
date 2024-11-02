from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import csv

featurenames = ["academicYear","universityName","faculty","departmentName","idOSYM","programType","language","scholarshipRate","quota","occupancyRate","tuitionFee","universityFoundingYear","facultyFoundingYear","universityLocation","universityRegion","profCount","assoCount","docCount","baseRanking","topRanking","avgAdmissionRanking(TYT)","baseAdmissionRanking(TYT)","stdDeviationStudents","revenue","outOfCityStudentRate","sameRegionStudentRate","totalPreference","weightedPreference","top1PreferenceRatio","top3PreferenceRatio","top9PreferenceRatio","avgOrderofPreference","tuitionFeeIncrease","avgAdmittedStudentPrefOrder","top1AdmittedRatio","top3AdmittedRatio","top10AdmittedRatio","admittedPrefTrendRatio","admittedGovPref", "admittedPrivPref","admittedTotalPref","admittedTotalDepartmentPref","currentStudentCount"]

#Creates the csv file, writes the header for all the features it will hold. 
#It will utilize writer.writerow() function for entering new rows to the csv file
file = open("SehirlerBolgeler.csv", mode="r", encoding="utf8")
regionFile = csv.reader(file, delimiter=",")
filename = input("Enter a file name either existing or a new file name (this wont truncate the file but only append to it.)")
csvfile = open(filename, mode="a")
writer = csv.DictWriter(csvfile, fieldnames=featurenames)
writer.writeheader()
tempDict = {}
for i in featurenames:
    tempDict[i] = None
#Site link and path for utilizing the webdriver are introduced to the code. Then it opens the site on chrome by driver.get(site)
site = 'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say'
path = 'C:\\Users\\AliCe\\OneDrive\\Belgeler\\chrome driver\\chromedriver-win64\\chromedriver.exe'
cService = webdriver.ChromeService(executable_path = path)
driver = webdriver.Chrome(service = cService)
wait = WebDriverWait(driver, 10)
driver.get(site)

#This function closes the popup warning that comes to screen if it does exist.
def closePopUp():
    try:
        close_button = driver.find_element(By.XPATH,"""//span[@class="featherlight-close-icon featherlight-close"]""")
    except NoSuchElementException:
        pass
    else:
        close_button.click()
    
#This function finds and clicks the "Hepsini Aç"(open all) button then waits 0.2 seconds to ensure clickable is open by the time we start scraping.
def openAll():
    wait.until(EC.presence_of_element_located((By.XPATH, """//a[@class="label label-success openall"]""")))
    open_all_button = driver.find_element(By.XPATH, """//a[@class="label label-success openall"]""")
    open_all_button.click()

#This function selects the option with the given value
def selectOption(value):
    wait.until(EC.presence_of_element_located((By.XPATH, "//option[@value=\"" + value + "\"]")))
    selection = driver.find_element(By.XPATH, "//option[@value=\"" + value + "\"]")
    selection.click()

#Clicks the academic year sections in the department page
def clickYear(year):
    temp = driver.find_element(By.XPATH,"""//div[@class="panel panel-default"]""")
    try:
        yearButton = temp.find_element(By.XPATH, ".//font[text()=\"" + str(year) + " Yılı\"]")
    except NoSuchElementException:
        return 1 
    else:
        yearButton = yearButton.find_element(By.XPATH, "./..")
        yearButton.click()   
    return 0



#Returns the tables of the given section name. Also scrapes the language, department name and scholarship information from the header
def searchInSection(sectionName,tempDict,regionfile):
    if sectionName == "genelBilgiler":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@style="margin:0px;background-color:#646464;"]""")))
        title = driver.find_element(By.XPATH, """//div[@style="margin:0px;background-color:#646464;"]""")
        titleAll = title.find_element(By.XPATH,""".//h3[@class="panel-title pull-left"]""").text
        titleAll = titleAll[titleAll.index("(") + len("("):]
        titleAll = titleAll.strip(")")
        region = determineRegion(regionfile,titleAll)
        tempDict["universityRegion"] = region
        tempDict["universityLocation"] = titleAll
        
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1000_1"]""")))
        genelBilgiler = driver.find_element(By.XPATH, """//div[@id="icerik_1000_1"]""")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1000_1 > table""")))
        tables = genelBilgiler.find_elements(By.XPATH,".//table")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1000_1 big""")))
        tableHeader = genelBilgiler.find_element(By.XPATH,""".//big""" ).text
        index = tableHeader.find("(İngilizce)")
        if index != -1:
            tempDict["language"] = "English"
            tableHeader = tableHeader.replace(" (İngilizce) ","")
        else:
            tempDict["language"] = "Turkish"
        index = tableHeader.find("(")
        if index != -1:
            if tableHeader.find("(Burslu)") != -1:
                tempDict["scholarshipRate"] = 100
                tableHeader = tableHeader.replace("(Burslu)","")
            elif tableHeader.find("(%50 İndirimli)") != -1:
                tempDict["scholarshipRate"] = 50 
                tableHeader = tableHeader.replace("(%50 İndirimli)","")
            elif tableHeader.find("(Ücretli)") != -1:
                tempDict["scholarshipRate"] = 0 
                tableHeader = tableHeader.replace("(Ücretli)","")
            elif tableHeader.find("(%25 İndirimli)") != -1:
                tempDict["scholarshipRate"] = 25 
                tableHeader = tableHeader.replace("(%25 İndirimli)","") 
            elif tableHeader.find("(%75 İndirimli)") != -1:
                tempDict["scholarshipRate"] = 75 
                tableHeader = tableHeader.replace("(%75 İndirimli)","")
        tempDict["departmentName"] = tableHeader  
        return tables   
    elif sectionName == "region":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1020ab"]""")))
        regions = driver.find_element(By.XPATH, """//div[@id="icerik_1020ab"]""")
        tables = regions.find_elements(By.XPATH, """.//table[@class="table table-bordered"]""") 
        return tables       
    elif sectionName == "preference":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1080"]""")))
        preference = driver.find_element(By.XPATH, """//div[@id="icerik_1080"]""")
        table = preference.find_element(By.XPATH, """.//table""")
        return table
    elif sectionName == "admittedOrder":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1040"]""")))
        admitted = driver.find_element(By.XPATH, """//div[@id="icerik_1040"]""")
        table = admitted.find_element(By.XPATH, ".//table")
        return table
    elif sectionName == "prefTrend":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1310"]""")))
        prefTrend = driver.find_element(By.XPATH, """//div[@id="icerik_1310"]""")
        table = prefTrend.find_element(By.XPATH, ".//table")
        return table
    elif sectionName == "average":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1230"]""")))
        average = driver.find_element(By.XPATH, """//div[@id="icerik_1230"]""")
        tables = average.find_elements(By.XPATH, ".//table")
        return tables
    elif sectionName == "admittedPref":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1300"]""")))
        average = driver.find_element(By.XPATH, """//div[@id="icerik_1300"]""")
        table = average.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
        return table
    elif sectionName == "admittedSameDepartmentPref":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1340a"]""")))
        average = driver.find_element(By.XPATH, """//div[@id="icerik_1340a"]""")
        table = average.find_element(By.XPATH, ".//table")
        return table
    elif sectionName == "academics":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_2050"]""")))
        average = driver.find_element(By.XPATH, """//div[@id="icerik_2050"]""")
        table = average.find_element(By.XPATH, ".//table")
        return table
    elif sectionName == "totalStudent":
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_2010"]""")))
        average = driver.find_element(By.XPATH, """//div[@id="icerik_2010"]""")
        table = average.find_element(By.XPATH, ".//table")
        return table
    
def searchInTable(table,tabletype,tempDict,tableCount):
    body = table.find_element(By.XPATH, ".//tbody")
    rows = body.find_elements(By.XPATH, ".//tr")
    if tabletype == "genelBilgiler":
        for row in rows:
            leftCell = row.find_element(By.XPATH,""".//td[@class="thb text-left"]""").text
            if leftCell == "ÖSYM Program Kodu":
                tempDict["idOSYM"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell == "Üniversite":
                tempDict["universityName"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell == "Fakülte / Yüksekokul":
                tempDict["faculty"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell == "Puan Türü":
                tempDict["programType"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell == "Genel Kontenjan":
                tempDict["quota"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell == "Genel Kontenjana Yerleşen":
                tempDict["occupancyRate"] = int(row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text) if row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text != "---" else 0 / int(tempDict["quota"]) * 100
            elif leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası *" or leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası*":
                tempDict["baseRanking"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
            elif leftCell.find("Tavan Başarı Sırası(0,12) *") != -1 or leftCell.find("Tavan Başarı Sırası(0,12)*") != -1:
                tempDict["topRanking"] = row.find_element(By.XPATH,""".//td[@class="text-center vert-align"]""").text
    elif tabletype == "region":
        for row in rows:
            cols = row.find_elements(By.XPATH, """.//td""")
            leftCell = cols[0].text
            if leftCell == "Farklı Şehir":
                col = cols[2].text
                tempDict["outOfCityStudentRate"] = col
            elif leftCell == tempDict["universityRegion"]:
                col = cols[2].text
                tempDict["sameRegionStudentRate"] = col
    elif tabletype == "preference":
        for row in rows:
            try:
                totalPref = row.find_element(By.XPATH, """.//td[@class="thr text-left"]""")  
            except NoSuchElementException:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
                if leftCell == "Ortalama Tercih Edilme Sırası":
                    tempDict["avgOrderofPreference"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
                elif leftCell == "Birinci Sırada Tercih Eden Sayısı":
                    cols = row.find_elements(By.XPATH, ".//td")
                    col = cols[2].text
                    tempDict["top1PreferenceRatio"] = col
                elif leftCell == "İlk Üç Sırada Tercih Eden Sayısı":
                    cols = row.find_elements(By.XPATH, ".//td")
                    col = cols[2].text
                    tempDict["top3PreferenceRatio"] = col
                elif leftCell == "İlk Dokuz Sırada Tercih Eden Sayısı":
                    cols = row.find_elements(By.XPATH, ".//td")
                    col = cols[2].text
                    tempDict["top9PreferenceRatio"] = col                   
            else:
                totalPrefCount = row.find_element(By.XPATH, """.//td[@align="center"]""").text
                tempDict["totalPreference"] = totalPrefCount
    elif tabletype == "admittedOrder":
        for row in rows:
            leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
            if leftCell == "Birinci Tercih Olarak Yerleşen Sayısı":
                cols = row.find_elements(By.XPATH, """.//td""")
                col = cols[2].text
                tempDict["top1AdmittedRatio"] = col
            elif leftCell == "İlk Üç Tercih Olarak Yerleşen Sayısı":
                cols = row.find_elements(By.XPATH, """.//td""")
                col = cols[2].text
                tempDict["top3AdmittedRatio"] = col
            elif leftCell == "İlk On Tercih Olarak Yerleşen Sayısı":
                cols = row.find_elements(By.XPATH, """.//td""")
                col = cols[2].text
                tempDict["top10AdmittedRatio"] = col
            elif leftCell == "Yerleşenler Ortalama Kaçıncı Tercihinde Yerleşti":
                tempDict["avgAdmittedStudentPrefOrder"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
    elif tabletype == "prefTrend":
        for row in rows:
            leftCell = row.find_element(By.XPATH, """.//td[@class="thb"]""").text
            if leftCell == "Devlet":
                tempDict["admittedGovPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
            elif leftCell == "Vakıf":
                tempDict["admittedPrivPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
    elif tabletype == "average":
        for row in rows:
            leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
            if leftCell == "TYT" and tableCount == 0:
                tempDict["avgAdmissionRanking(TYT)"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
            elif leftCell == "TYT" and tableCount == 1:
                tempDict["baseAdmissionRanking(TYT)"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
    elif tabletype == "admittedPref":
        for row in rows:
            leftCell = row.find_element(By.XPATH, """.//td[@class="thb"]""").text
            if leftCell == "Kullanılan Tercih":
                tempDict["admittedTotalPref"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
            
    elif tabletype == "admittedSameDepartmentPref":
        for row in rows:
            leftCell = row.find_element(By.XPATH, """.//td[@width="60%"]""").text
            tempDict["admittedTotalPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
            break
    elif tabletype == "academics":
        for row in rows:
            cols = row.find_elements(By.XPATH, """.//td""")
            if cols[0].text == "Profesör":
                tempDict["profCount"] = cols[1].text
            elif cols[0].text == "Doçent":
                tempDict["assoCount"] = cols[1].text
            elif cols[0].text == "Doktor Öğretim Üyesi":
                tempDict["docCount"] = cols[1].text
    elif tabletype == "totalStudent":
        for row in rows:
            # leftCell = row.find_element(By.XPATH, """.//td[@class="thr"]""").text
            cols = row.find_elements(By.XPATH, """.//td""")
            col = cols[1].text
            tempDict["currentStudentCount"] = col
            break
                
    return


#This function is for after entering the page of one Department. Scrapes the data of all academic years existing for that Department to the csv file.
def scrapeDepartment(tempDict,writer,regionfile):
    if driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
        return
    closePopUp()
    year = 2023
    for i in range(0,3):
        if driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
            break
        
        closePopUp()
        openAll()
        
        tempDict["academicYear"] = year - i
        tableCount = 0
        
        tableType = "genelBilgiler"
        tables = searchInSection(tableType,tempDict,regionfile)
        for table in tables:
            searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "region"
        tables = searchInSection(tableType,tempDict,regionfile)
        for table in tables:
            searchInTable(table,tableType, tempDict,tableCount)
        
        tableType = "preference"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "admittedOrder"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "prefTrend"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "average"
        tables = searchInSection(tableType,tempDict,regionfile)
        for table in tables:
            searchInTable(table, tableType, tempDict, tableCount)
            tableCount += 1
        
        tableType = "admittedPref"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "admittedSameDepartmentPref"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "academics"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        
        tableType = "totalStudent"
        table = searchInSection(tableType,tempDict,regionfile)
        searchInTable(table, tableType, tempDict,tableCount)
        

        writer.writerow(tempDict)
        for a in featurenames:
            tempDict[a] = None
        
        if clickYear(year-i-1) == 1:
            break             
    return

#This function clicks the Department with the given index on the list and enters the Departments page tab(that opens when you click it).
def enterDepartment(row):
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1
    link = row.find_element(By.XPATH,""".//a[@target="_blank"]""")
    link.click()
    wait.until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break
    time.sleep(1)
    return original_window

#Closes the tab of recently scraped department.
def exitDepartment(original_window):
    driver.close()
    driver.switch_to.window(original_window)
    return

def clickPageButton(buttonName):
    buttonTab = driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
    try:
        button = buttonTab.find_element(By.XPATH, ".//a[text()=\"" + buttonName + "\"]")
    except NoSuchElementException:
        raise ValueError(buttonName + " Button doesn't exist!!")
    else:
        button.click()    
        time.sleep(5)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)

def clickNextPageButton():
    buttonTab = driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
    try:
        buttonTab.find_element(By.XPATH, """.//li[@class="paginate_button next disabled"]""")
    except NoSuchElementException:
        buttonTab.find_element(By.XPATH, """.//a[text()="Sonraki"]""").click()
        time.sleep(5)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)
        return 0
    else:
        return 1
    
def determineRegion(regionfile,cityName):
    file.seek(0)
    region = ""
    for row in regionfile:
        if cityName == row[1]:
            return row[2]
    return region