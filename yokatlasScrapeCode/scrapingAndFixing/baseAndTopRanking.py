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

fixedFileName = fileToFix.replace(".csv", "") + "(fixed3)" + ".csv"
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
        for i in range (0,4): 
            tempRanking = department[19 + i]
            r1 = tempRanking.rfind(".")
            if r1 != -1:
                a = len(tempRanking) - 1 - r1
                if a < 3:
                    tempRanking += "0" * (3-a)  
                    department[19 + i] = tempRanking
    csvwriter.writerow(department)
