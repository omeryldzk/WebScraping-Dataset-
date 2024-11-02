from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import csv


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
    open_all_button = driver.find_element(By.XPATH, """//a[@class="label label-success openall"]""")
    open_all_button.click()
    time.sleep(1.8)

#This function selects the option with the given value
def selectOption(value):
    try:
        selection = driver.find_element(By.XPATH, "//option[@value=\"" + value + "\"]")
    except NoSuchElementException:
        raise ValueError("NO SUCH OPTION EXISTS")
    else:
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
    time.sleep(1)
    return 0



#Returns the tables of the given section name. Also scrapes the language, department name and scholarship information from the header
def searchInSection(sectionName):
    if sectionName == "genelBilgiler":
        
        title = driver.find_element(By.XPATH, """//div[@style="margin:0px;background-color:#646464;"]""")
        titleAll = title.find_element(By.XPATH,""".//h3[@class="panel-title pull-left"]""").text
        titleAll = titleAll[titleAll.index("(") + len("("):]
        titleAll = titleAll.strip(")")
        tempDict["universityLocation"] = titleAll
        genelBilgiler = driver.find_element(By.XPATH, """//div[@id="icerik_1000_1"]""")
        tables = genelBilgiler.find_elements(By.XPATH,".//table")
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
    if sectionName == "region":
        regions = driver.find_element(By.XPATH, """//div[@id="icerik_1020ab"]""")
        table = regions.find_element(By.XPATH, """.//table""") 
        return table       
    if sectionName == "preference":
        preference = driver.find_element(By.XPATH, """//div[@id="icerik_1080"]""")
        table = preference.find_element(By.XPATH, """.//table""")
        return table
    if sectionName == "admittedOrder":
        admitted = driver.find_element(By.XPATH, """//div[@id="icerik_1040"]""")
        table = admitted.find_element(By.XPATH, ".//table")
        return table
    if sectionName == "prefTrend":
        prefTrend = driver.find_element(By.XPATH, """//div[@id="icerik_1310"]""")
        table = prefTrend.find_element(By.XPATH, ".//table")
        return table
    if sectionName == "average":
        average = driver.find_element(By.XPATH, """//div[@id="icerik_1230"]""")
        table = average.find_element(By.XPATH, ".//table")
        return table

def searchInTable(table,tabletype):
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
    elif tabletype == "region":
        for row in rows:
            try:
                leftCellLoc = row.find_element(By.XPATH,""".//td[@class="thb text-left"]""")
            except NoSuchElementException:
                continue
            else:
                leftCell = leftCellLoc.text
                if leftCell == "Farklı Şehir":
                    cols = row.find_elements(By.XPATH, """.//td""")
                    col = cols[2].text
                    tempDict["outOfCityStudentRate"] = col
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
            if leftCell == "TYT":
                tempDict["avgAdmissionRanking"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
    return


#This function is for after entering the page of one Department. Scrapes the data of all academic years existing for that Department to the csv file.
def scrapeDepartment():
    if driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
        return
    closePopUp()
    year = 2023
    for i in range(0,3):
        if clickYear(year-i) == 0:
            if driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
                break
            closePopUp()
            openAll()
            tempDict["academicYear"] = year-i
            tableType = "genelBilgiler"
            tables = searchInSection(tableType)
            for table in tables:
                searchInTable(table, tableType)
            
            tableType = "region"
            table = searchInSection(tableType)
            searchInTable(table,tableType)
            
            tableType = "preference"
            table = searchInSection(tableType)
            searchInTable(table, tableType)
            
            tableType = "admittedOrder"
            table = searchInSection(tableType)
            searchInTable(table, tableType)
            
            tableType = "prefTrend"
            table = searchInSection(tableType)
            searchInTable(table, tableType)
            
            tableType = "average"
            table = searchInSection(tableType)
            searchInTable(table, tableType)
            
            writer.writerow(tempDict)
            for i in featurenames:
                tempDict[i] = None
        else:
            break        
        
        
    return

#This function clicks the Department with the given index on the list and enters the Departments page tab(that opens when you click it).
def enterDepartment(row):
    wait = WebDriverWait(driver, 10)
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
    time.sleep(0.5)
    return

def clickPageButton(buttonName):
    buttonTab = driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
    try:
        checkAccess = buttonTab.find_element(By.XPATH, """.//li[@class="paginate_button next disabled"]""")
    except NoSuchElementException:
        buttonTab.find_element(By.XPATH, ".//a[text()=\"" + buttonName + "\"]").click()
        time.sleep(6)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(4)

def clickNextPageButton():
    buttonTab = driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
    try:
        checkAccess = buttonTab.find_element(By.XPATH, """.//li[@class="paginate_button next disabled"]""")
    except NoSuchElementException:
        buttonTab.find_element(By.XPATH, """.//a[text()="Sonraki"]""").click()
        time.sleep(6)
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(4)
        return 0
    else:
        return 1


#MAIN FUNCTION
def main():
    #First we will select our program type option
    time.sleep(1)
    selectOption("ea")
    time.sleep(6)
    #We then decide numbers of elements in the table
    selectOption("100")
    time.sleep(0.5)
    #Then we decide the university type (private/government)
    selectOption("Vakıf")
    time.sleep(5)

    #This function can be applied to use the navigator bar at the bottom and start from a certain page
    clickPageButton("4")
    while True:
        temp = driver.find_element(By.XPATH,"""//table[@id="mydata"]""")
        body = temp.find_element(By.XPATH,".//tbody")
        rows = body.find_elements(By.XPATH,".//tr")
        for row in rows:
            original_window = enterDepartment(row)
            scrapeDepartment()
            exitDepartment(original_window)
            
        if clickNextPageButton() == 1:
            break
    return
     

#Creates the csv file, writes the header for all the features it will hold. 
#It will utilize writer.writerow() function for entering new rows to the csv file
with open("departments(soz).csv", mode="a") as csvfile:
    featurenames = ["academicYear","universityName","faculty","departmentName","idOSYM","programType","language","scholarshipRate","quota","occupancyRate","tuitionFee","universityLocation","baseRanking","avgAdmissionRanking","stdDeviationStudents","revenue","outOfCityStudentRate","outOfRegionStudentRate","totalPreference","weightedPreference","top1PreferenceRatio","top3PreferenceRatio","top9PreferenceRatio","avgOrderofPreference","tuitionFeeIncrease","avgAdmittedStudentPrefOrder","top1AdmittedRatio","top3AdmittedRatio","top10AdmittedRatio","admittedPrefTrendRatio","admittedGovPref", "admittedPrivPref"]
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
    driver.get(site)
    main()


    






# temp = driver.find_element(By.XPATH,"""//div[@id="icerik_1000_1"]""")
# rows = temp.find_elements(By.XPATH,".//tr")
# for row in rows:
    
#     cols = row.find_elements(By.XPATH,".//td")
    
#     for col in cols:
#         print(col.text)




