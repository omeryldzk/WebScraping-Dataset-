import csv
from selenium import webdriver
import platform

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fixFunctions import *


fileToFix = "2024+alldepartments.csv"
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

newFile = fileToFix.replace(".csv", "") + "(minMaxScore2)" + ".csv"
newFile = open(newFile, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)

if platform.system() == "Darwin":
    path = '../resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService)
wait = WebDriverWait(driver, 30)

csvwriter.writerow(["idOSYM","baseScore","topScore"])
for index,row in enumerate(csvreaderFileToFix):
    if index == 0:
        continue
    if row[0] == "2021":
        continue
    idOsym = row[5]
    baseScore = ""
    topScore = ""
    academicYear = row[0]
    if academicYear == "2024":    
        link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + idOsym
        driver.get(link)
        closePopUp(driver,wait)
        openAll(driver,wait)
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1000_1"]""")))
        div = driver.find_element(By.XPATH, """//div[@id="icerik_1000_1"]""")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1000_1 table""")))
        tables = div.find_elements(By.XPATH, """.//table[@class="table table-bordered"]""")
        for table in tables:
            body = table.find_element(By.XPATH, """.//tbody""")
            rows = body.find_elements(By.XPATH, """.//tr""")
            for row in rows:
                cols = row.find_elements(By.XPATH, """.//td""")
                leftCell = cols[0].text 
                if leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Puanı *" or leftCell == "0,12 Katsayı ile Yerleşen Son Kişinin Puanı*":
                    baseScore = cols[1].text
                if leftCell == academicYear + " Tavan Puan(0,12) *" or leftCell == academicYear + " Tavan Puan(0,12)*":
                    topScore = cols[1].text
        csvwriter.writerow([idOsym,baseScore,topScore])
        newFile.flush()
    # else:
    #     link = "https://yokatlas.yok.gov.tr/" + academicYear +"/lisans.php?y=" + idOsym
    
                
                
        
            
    
    