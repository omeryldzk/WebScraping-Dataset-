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

regionFile = open("SehirlerBolgeler.csv", mode="r", encoding="utf8")
regionCsv = csv.reader(regionFile, delimiter=",")

if platform.system() == "Darwin":
    path = '../resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
cService = webdriver.ChromeService(executable_path=path)
driver = webdriver.Chrome(service=cService)
wait = WebDriverWait(driver, 30)

count = 0
for department in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(department)
        count += 1
        continue
    else:
        if department[26] == "":
            osymId = department[5]
            link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + osymId
            driver.get(link)
            closePopUp(driver, wait)
            openAll(driver, wait)
            wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1020ab"]""")))
            regions = driver.find_element(By.XPATH, """//div[@id="icerik_1020ab"]""")
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1020ab table""")))
            tables = regions.find_elements(By.XPATH, """.//table[@class="table table-bordered"]""")
            for table in tables:
                body = table.find_element(By.XPATH, ".//tbody")
                rows = body.find_elements(By.XPATH, ".//tr")
                for row in rows:
                    cols = row.find_elements(By.XPATH, """.//td""")
                    leftCell = cols[0].text
                    if leftCell == department[15]:
                        col = cols[2].text
                        department[26] = col
                
    csvwriter.writerow(department)
