import csv
from selenium import webdriver
import platform

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fixFunctions import *


fileToFix = input("Enter the file name: ")
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixedFileName = fileToFix.replace(".csv", "") + "(fixed)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)

if platform.system() == "Darwin":
    path = '../resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
    
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService)
wait = WebDriverWait(driver, 30)
for row in csvreaderFileToFix:
    if (row[1] == "Dolmadı" and row[2] != "---") or (row[1] == "---" and row[2] == "---"):
        idOsym = row[0]
        link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + idOsym
        driver.get(link)
        closePopUp(driver, wait)
        openAll(driver, wait)
        wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1070"]""")))
        lastPersonSection = driver.find_element(By.XPATH, """//div[@id="icerik_1070"]""")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1070 table""")))
        table = lastPersonSection.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
        rows = table.find_elements(By.XPATH, """.//tr""")
        minScore = ""
        for row2 in rows:
            cols = row2.find_elements(By.XPATH, """.//td""")
            if cols[0].text == "Yerleştiği Puan*" or cols[0].text == "Yerleştiği Puan *":
                minScore = cols[1].text
        row[1] = minScore
    csvwriter.writerow(row)
    newFile.flush()
                
        
        
        