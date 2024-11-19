from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time
import csv
import platform


class ScrapeFunctions:
    featurenames = ["academicYear", "universityName", "faculty", "departmentName", "idOSYM", "programType", "language",
                    "scholarshipRate", "quota", "occupiedSlots", "tuitionFee", "universityFoundingYear",
                    "facultyFoundingYear", "universityLocation", "universityRegion", "profCount", "assoCount", "docCount",
                    "baseRanking", "topRanking", "avgAdmissionRanking(TYT)", "baseAdmissionRanking(TYT)",
                    "stdDeviationStudents", "revenue", "outOfCityStudentRate", "sameRegionStudentRate", "totalPreference",
                    "weightedPreference", "top1PreferenceRatio", "top3PreferenceRatio", "top9PreferenceRatio",
                    "avgOrderofPreference", "tuitionFeeIncrease", "avgAdmittedStudentPrefOrder", "top1AdmittedRatio",
                    "top3AdmittedRatio", "top10AdmittedRatio", "admittedPrefTrendRatio", "admittedGovPref",
                    "admittedPrivPref", "admittedTotalPref", "admittedTotalDepartmentPref", "currentStudentCount"]

    # Creates the csv file, writes the header for all the features it will hold.
    # It will utilize writer.writerow() function for entering new rows to the csv file

    # Site link and path for utilizing the webdriver are introduced to the code. Then it opens the site on chrome by driver.get(site)
    def __init__(self):
        while True:
            self.type = input(
                "Please enter the program type you wanna scrape (only available inputs are 'ea', 'söz', 'dil', 'say')('- 1' to exit)")
            if self.type == "-1":
                self.type = ""
                break
            elif self.type == 'say' or self.type == 'söz' or self.type == 'dil' or self.type == 'ea':
                break
        while True:
            self.uniType = input(
                "Please enter the university type you wanna scrape (only available inputs are 'Devlet', 'Vakıf')('- 1' to exit)")
            if self.uniType == "-1":
                self.uniType = ""
                break
            elif self.uniType == 'Devlet' or self.uniType == 'Vakıf':
                break
        self.startPage = 0
        while True:
            pageNum = input("Please enter the page you want your scraping to start at ('- 1' to exit)")
            if pageNum == "-1":
                pageNum = ""
                break
            elif int(pageNum) > 0:
                self.startPage = int(pageNum)
                break
        self.file = open("SehirlerBolgeler.csv", mode="r", encoding="utf8")
        self.regionFile = csv.reader(self.file, delimiter=",")
        filename = input(
            "Enter a file name either existing or a new file name (this wont truncate the file but only append to it.) (Please include the file extension '.csv')")
        self.csvfile = open(filename, mode="a", encoding="utf8")
        self.writer = csv.DictWriter(self.csvfile, fieldnames=self.featurenames)
        if self.startPage <= 1:
            self.writer.writeheader()
        self.tempDict = {}
        for i in self.featurenames:
            self.tempDict[i] = None

        site = 'https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php?p=say'
        if platform.system() == "Darwin":
            path = './resources/mac_chrome_driver/chromedriver'
        elif platform.system() == "Windows":
            path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
        self.cService = webdriver.ChromeService(executable_path=path)
        self.driver = webdriver.Chrome(service=self.cService)
        self.wait = WebDriverWait( self.driver, 30)
        self.driver.get(site)



    # This function closes the popup warning that comes to screen if it does exist.
    def closePopUp(self):
        try:
            close_button =  self.driver.find_elements(By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")
        except NoSuchElementException:
            pass
        else:
            if len(close_button) == 1:
                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
                self.driver.execute_script('arguments[0].click()', close_button[0])
            elif len(close_button) > 1:
                self.driver.execute_script('arguments[0].click()', close_button[1])
                try:
                    close_button =  self.driver.find_elements(By.XPATH,
                                                        """//span[@class="featherlight-close-icon featherlight-close"]""")
                except NoSuchElementException:
                    pass
                else:
                    close_button2 =  self.driver.find_element(By.XPATH,
                                                        """//span[@class="featherlight-close-icon featherlight-close"]""")
                    self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
                    self.driver.execute_script('arguments[0].click()', close_button2)
            else:
                pass


    # This function finds and clicks the "Hepsini Aç"(open all) button then waits 0.2 seconds to ensure clickable is open by the time we start scraping.
    def openAll(self):
        self.wait.until(EC.presence_of_element_located((By.XPATH, """//a[@class="label label-success openall"]""")))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, """//a[@class="label label-success openall"]""")))
        open_all_button = self.driver.find_element(By.XPATH, """//a[@class="label label-success openall"]""")
        self.driver.execute_script('arguments[0].click()', open_all_button)


    # This function selects the option with the given value
    def selectOption(self, value):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//option[@value=\"" + str(value) + "\"]")))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//option[@value=\"" + str(value) + "\"]")))
        selection = self.driver.find_element(By.XPATH, "//option[@value=\"" + str(value) + "\"]")
        selection.click()


    # Clicks the academic year sections in the department page
    def clickYear(self,year):
        self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@class="panel panel-default"]""")))
        temp = self.driver.find_element(By.XPATH, """//div[@class="panel panel-default"]""")
        try:
            yearButton = temp.find_element(By.XPATH, ".//font[text()=\"" + str(year) + " Yılı\"]")
        except NoSuchElementException:
            return 1
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//font[text()=\"" + str(year) + " Yılı\"]")))
            yearButton = yearButton.find_element(By.XPATH, "./..")
            self.driver.execute_script('arguments[0].click()', yearButton)
        return 0


    # Returns the tables of the given section name. Also scrapes the language, department name and scholarship information from the header
    def searchInSection(self, sectionName):
        if sectionName == "genelBilgiler":
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, """//div[@style="margin:0px;background-color:#646464;"]""")))
            title = self.driver.find_element(By.XPATH, """//div[@style="margin:0px;background-color:#646464;"]""")
            titleAll = title.find_element(By.XPATH, """.//h3[@class="panel-title pull-left"]""").text
            titleAll = titleAll[titleAll.index("(") + len("("):]
            titleAll = titleAll.strip(")")
            region = self.determineRegion(titleAll)
            self.tempDict["universityRegion"] = region
            self.tempDict["universityLocation"] = titleAll

            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1000_1"]""")))
            genelBilgiler = self.driver.find_element(By.XPATH, """//div[@id="icerik_1000_1"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1000_1 > table""")))
            tables = genelBilgiler.find_elements(By.XPATH, ".//table")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1000_1 big""")))
            tableHeader = genelBilgiler.find_element(By.XPATH, """.//big""").text
            index = tableHeader.find("(")
            if index != -1:
                if tableHeader.find("(Burslu)") != -1:
                    self.tempDict["scholarshipRate"] = 100
                    tableHeader = tableHeader.replace(" (Burslu)", "")
                elif tableHeader.find("(%50 İndirimli)") != -1:
                    self.tempDict["scholarshipRate"] = 50
                    tableHeader = tableHeader.replace(" (%50 İndirimli)", "")
                elif tableHeader.find("(Ücretli)") != -1:
                    self.tempDict["scholarshipRate"] = 0
                    tableHeader = tableHeader.replace(" (Ücretli)", "")
                elif tableHeader.find("(%25 İndirimli)") != -1:
                    self.tempDict["scholarshipRate"] = 25
                    tableHeader = tableHeader.replace(" (%25 İndirimli)", "")
                elif tableHeader.find("(%75 İndirimli)") != -1:
                    self.tempDict["scholarshipRate"] = 75
                    tableHeader = tableHeader.replace(" (%75 İndirimli)", "")

            index = tableHeader.find("(")
            if index != -1:
                index_end = tableHeader.find(")")
                language = tableHeader[index + 1:index_end]
                self.tempDict["language"] = language
                tableHeader = tableHeader.replace(" (" + language + ")", "")
                pass

            self.tempDict["departmentName"] = tableHeader
            return tables
        elif sectionName == "region":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1020ab"]""")))
            regions = self.driver.find_element(By.XPATH, """//div[@id="icerik_1020ab"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1020ab table""")))
            tables = regions.find_elements(By.XPATH, """.//table[@class="table table-bordered"]""")
            return tables
        elif sectionName == "preference":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1080"]""")))
            preference = self.driver.find_element(By.XPATH, """//div[@id="icerik_1080"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1080 table""")))
            table = preference.find_element(By.XPATH, """.//table""")
            return table
        elif sectionName == "admittedOrder":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1040"]""")))
            admitted = self.driver.find_element(By.XPATH, """//div[@id="icerik_1040"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1040 table""")))
            table = admitted.find_element(By.XPATH, ".//table")
            return table
        elif sectionName == "prefTrend":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1310"]""")))
            prefTrend = self.driver.find_element(By.XPATH, """//div[@id="icerik_1310"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1310 table""")))
            table = prefTrend.find_element(By.XPATH, ".//table")
            return table
        elif sectionName == "average":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1230"]""")))
            average = self.driver.find_element(By.XPATH, """//div[@id="icerik_1230"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1230 table""")))
            tables = average.find_elements(By.XPATH, ".//table")
            return tables
        elif sectionName == "admittedPref":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1300"]""")))
            average = self.driver.find_element(By.XPATH, """//div[@id="icerik_1300"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1300 table""")))
            table = average.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
            return table
        elif sectionName == "admittedSameDepartmentPref":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1340a"]""")))
            average = self.driver.find_element(By.XPATH, """//div[@id="icerik_1340a"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1340a table""")))
            table = average.find_element(By.XPATH, ".//table")
            return table
        elif sectionName == "academics":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_2050"]""")))
            average = self.driver.find_element(By.XPATH, """//div[@id="icerik_2050"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_2050 table""")))
            table = average.find_element(By.XPATH, ".//table")
            return table
        elif sectionName == "totalStudent":
            self.wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_2010"]""")))
            average = self.driver.find_element(By.XPATH, """//div[@id="icerik_2010"]""")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_2010 table""")))
            table = average.find_element(By.XPATH, ".//table")
            return table


    def searchInTable(self, table, tabletype, tableCount):
        body = table.find_element(By.XPATH, ".//tbody")
        rows = body.find_elements(By.XPATH, ".//tr")
        if tabletype == "genelBilgiler":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
                if leftCell == "ÖSYM Program Kodu":
                    self.tempDict["idOSYM"] = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
                elif leftCell == "Üniversite":
                    self.tempDict["universityName"] = row.find_element(By.XPATH,
                                                                  """.//td[@class="text-center vert-align"]""").text
                elif leftCell == "Fakülte / Yüksekokul":
                    temp = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
                    if temp.find("(İngilizce)") != -1:
                        temp = temp.replace(" (İngilizce) ", "")
                    if temp.find("(Burslu)") != -1:
                        temp = temp.replace("(Burslu)", "")
                    if temp.find("(%50 İndirimli)") != -1:
                        temp = temp.replace("(%50 İndirimli)", "")
                    if temp.find("(Ücretli)") != -1:
                        temp = temp.replace("(Ücretli)", "")
                    if temp.find("(%25 İndirimli)") != -1:
                        temp = temp.replace("(%25 İndirimli)", "")
                    if temp.find("(%75 İndirimli)") != -1:
                        temp = temp.replace("(%75 İndirimli)", "")
                    self.tempDict["faculty"] = temp
                elif leftCell == "Puan Türü":
                    self.tempDict["programType"] = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
                elif leftCell == "Genel Kontenjan":
                    self.tempDict["quota"] = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
                elif leftCell == "Genel Kontenjana Yerleşen":
                    self.tempDict["occupiedSlots"] = int(
                        row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text) if row.find_element(
                        By.XPATH, """.//td[@class="text-center vert-align"]""").text != "---" else 0 / int(
                        self.tempDict["quota"]) * 100
                elif leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası *" or leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası*":
                    self.tempDict["baseRanking"] = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
                elif leftCell.find("Tavan Başarı Sırası(0,12) *") != -1 or leftCell.find(
                        "Tavan Başarı Sırası(0,12)*") != -1:
                    self.tempDict["topRanking"] = row.find_element(By.XPATH, """.//td[@class="text-center vert-align"]""").text
        elif tabletype == "region":
            for row in rows:
                cols = row.find_elements(By.XPATH, """.//td""")
                leftCell = cols[0].text
                if leftCell == "Farklı Şehir":
                    col = cols[2].text
                    self.tempDict["outOfCityStudentRate"] = col
                elif leftCell == self.tempDict["universityRegion"]:
                    col = cols[2].text
                    self.tempDict["sameRegionStudentRate"] = col
        elif tabletype == "preference":
            for row in rows:
                try:
                    totalPref = row.find_element(By.XPATH, """.//td[@class="thr text-left"]""")
                except NoSuchElementException:
                    leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
                    if leftCell == "Ortalama Tercih Edilme Sırası":
                        self.tempDict["avgOrderofPreference"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
                    elif leftCell == "Birinci Sırada Tercih Eden Sayısı":
                        cols = row.find_elements(By.XPATH, ".//td")
                        col = cols[2].text
                        self.tempDict["top1PreferenceRatio"] = col
                    elif leftCell == "İlk Üç Sırada Tercih Eden Sayısı":
                        cols = row.find_elements(By.XPATH, ".//td")
                        col = cols[2].text
                        self.tempDict["top3PreferenceRatio"] = col
                    elif leftCell == "İlk Dokuz Sırada Tercih Eden Sayısı":
                        cols = row.find_elements(By.XPATH, ".//td")
                        col = cols[2].text
                        self.tempDict["top9PreferenceRatio"] = col
                else:
                    totalPrefCount = row.find_element(By.XPATH, """.//td[@align="center"]""").text
                    self.tempDict["totalPreference"] = totalPrefCount
        elif tabletype == "admittedOrder":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
                if leftCell == "Birinci Tercih Olarak Yerleşen Sayısı":
                    cols = row.find_elements(By.XPATH, """.//td""")
                    col = cols[2].text
                    self.tempDict["top1AdmittedRatio"] = col
                elif leftCell == "İlk Üç Tercih Olarak Yerleşen Sayısı":
                    cols = row.find_elements(By.XPATH, """.//td""")
                    col = cols[2].text
                    self.tempDict["top3AdmittedRatio"] = col
                elif leftCell == "İlk On Tercih Olarak Yerleşen Sayısı":
                    cols = row.find_elements(By.XPATH, """.//td""")
                    col = cols[2].text
                    self.tempDict["top10AdmittedRatio"] = col
                elif leftCell == "Yerleşenler Ortalama Kaçıncı Tercihinde Yerleşti":
                    self.tempDict["avgAdmittedStudentPrefOrder"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
        elif tabletype == "prefTrend":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb"]""").text
                if leftCell == "Devlet":
                    self.tempDict["admittedGovPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
                elif leftCell == "Vakıf":
                    self.tempDict["admittedPrivPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
        elif tabletype == "average":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb text-left"]""").text
                if leftCell == "TYT" and tableCount == 0:
                    self.tempDict["avgAdmissionRanking(TYT)"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
                elif leftCell == "TYT" and tableCount == 1:
                    self.tempDict["baseAdmissionRanking(TYT)"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text
        elif tabletype == "admittedPref":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@class="thb"]""").text
                if leftCell == "Kullanılan Tercih":
                    self.tempDict["admittedTotalPref"] = row.find_element(By.XPATH, """.//td[@align="center"]""").text

        elif tabletype == "admittedSameDepartmentPref":
            for row in rows:
                leftCell = row.find_element(By.XPATH, """.//td[@width="60%"]""").text
                self.tempDict["admittedTotalDepartmentPref"] = row.find_element(By.XPATH, """.//td[@class="text-center"]""").text
                break
        elif tabletype == "academics":
            for row in rows:
                cols = row.find_elements(By.XPATH, """.//td""")
                if cols[0].text == "Profesör":
                    self.tempDict["profCount"] = cols[1].text
                elif cols[0].text == "Doçent":
                    self.tempDict["assoCount"] = cols[1].text
                elif cols[0].text == "Doktor Öğretim Üyesi":
                    self.tempDict["docCount"] = cols[1].text
        elif tabletype == "totalStudent":
            for row in rows:
                # leftCell = row.find_element(By.XPATH, """.//td[@class="thr"]""").text
                cols = row.find_elements(By.XPATH, """.//td""")
                col = cols[1].text
                self.tempDict["currentStudentCount"] = col
                break

        return


    # This function is for after entering the page of one Department. Scrapes the data of all academic years existing for that Department to the csv file.
    def scrapeDepartment(self):
        if self.driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or self.driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or self.driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
            return
        self.closePopUp()
        year = 2023
        for i in range(0, 3):
            if self.driver.current_url == "https://yokatlas.yok.gov.tr/lisans-anasayfa.php" or self.driver.current_url == "https://yokatlas.yok.gov.tr/2022/lisans-anasayfa.php" or self.driver.current_url == "https://yokatlas.yok.gov.tr/2021/lisans-anasayfa.php":
                break

            self.closePopUp()
            self.openAll()

            self.tempDict["academicYear"] = year - i
            tableCount = 0

            tableType = "genelBilgiler"
            tables = self.searchInSection(tableType)
            for table in tables:
                self.searchInTable(table, tableType,  tableCount)

            tableType = "region"
            tables = self.searchInSection(tableType)
            for table in tables:
                self.searchInTable(table, tableType,  tableCount)

            tableType = "preference"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "admittedOrder"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "prefTrend"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "average"
            tables = self.searchInSection(tableType )
            for table in tables:
                self.searchInTable(table, tableType,  tableCount)
                tableCount += 1

            tableType = "admittedPref"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "admittedSameDepartmentPref"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "academics"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            tableType = "totalStudent"
            table = self.searchInSection(tableType )
            self.searchInTable(table, tableType,  tableCount)

            self.writer.writerow(self.tempDict)
            for a in self.featurenames:
                self.tempDict[a] = None

            if self.clickYear(year - i - 1) == 1:
                break
        return


    # This function clicks the Department with the given index on the list and enters the Departments page tab(that opens when you click it).
    def enterDepartment(self,row):
        original_window = self.driver.current_window_handle
        assert len(self.driver.window_handles) == 1
        link = row.find_element(By.XPATH, """.//a[@target="_blank"]""")
        link.click()
        self.wait.until(EC.number_of_windows_to_be(2))
        for window_handle in self.driver.window_handles:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                break
        time.sleep(1)
        return original_window


    # Closes the tab of recently scraped department.
    def exitDepartment(self,original_window):
        self.driver.close()
        self.driver.switch_to.window(original_window)
        return


    def clickPageButton(self,buttonName):
        buttonTab = self.driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, ".//a[text()=\"" + buttonName + "\"]")))
            button = buttonTab.find_element(By.XPATH, ".//a[text()=\"" + buttonName + "\"]")
        except NoSuchElementException:
            raise ValueError(buttonName + " Button doesn't exist!!")
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, ".//a[text()=\"" + buttonName + "\"]")))
            button.click()
            time.sleep(5)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(3)


    def clickNextPageButton(self):
        buttonTab = self.driver.find_element(By.XPATH, """//div[@id="mydata_paginate"]""")
        try:
            buttonTab.find_element(By.XPATH, """.//li[@class="paginate_button next disabled"]""")
        except NoSuchElementException:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, """.//a[text()="Sonraki"]""")))
            buttonTab.find_element(By.XPATH, """.//a[text()="Sonraki"]""").click()
            time.sleep(5)
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(3)
            return 0
        else:
            return 1


    def determineRegion(self,cityName):
        self.file.seek(0)
        region = ""
        for row in self.regionFile:
            if cityName == row[1]:
                return row[2]
        return region
