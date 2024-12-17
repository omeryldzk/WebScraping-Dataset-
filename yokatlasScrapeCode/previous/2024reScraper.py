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

fixedFileName = fileToFix.replace(".csv", "") + "(fixed6)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


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
            if department[10] != "0":
                osymId = department[5]
                link = "https://yokatlas.yok.gov.tr/lisans.php?y=" + osymId
                
    csvwriter.writerow(department)
