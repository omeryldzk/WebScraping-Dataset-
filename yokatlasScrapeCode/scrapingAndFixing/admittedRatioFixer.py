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

fixedFileName = fileToFix.replace(".csv", "") + "(fixeddd)" + ".csv"
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
        if department[25] != "":
            department[25] = float(department[25]) / 10
        temp = float(department[35])
        temp2 = round(temp,3) * 100
        department[35] = "%"+str(temp2).replace(".",",")[:4]
        temp = float(department[36])
        temp2 = round(temp,3) * 100
        department[36] = "%" + str(temp2).replace(".",",")[:4]
        department[37] = "%" + str(round(float(department[37]),3) * 100).replace(".",",")[:4]
        department[29] = round(float(department[29]),3) * 10
                                

    csvwriter.writerow(department)
