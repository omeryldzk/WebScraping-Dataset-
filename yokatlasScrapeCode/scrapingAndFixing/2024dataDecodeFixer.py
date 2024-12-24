from fixFunctions import *
import csv
import platform
from selenium.common import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fixFunctions import *


fileToFix = "2024departments(allfixed).csv"
file = open(fileToFix, "r", encoding="utf-8")
csvreaderFileToFix = csv.reader(file)

fixerFile = "2024departments(rightencoding).csv"
file2 = open(fixerFile, "r", encoding="utf-8")
csvreaderFixerFile = csv.reader(file2)

fixedFileName = fileToFix.replace(".csv", "") + "(FIXED)" + ".csv"
newFile = open(fixedFileName, "w", newline="", encoding="utf-8")
csvwriter = csv.writer(newFile)


for index,row in enumerate(csvreaderFileToFix):
    if index == 0:
        csvwriter.writerow(row)
        continue
    corresponding_row = []
    for row2 in csvreaderFixerFile:
        if row2[5] == row[5]:
            corresponding_row = row2
            break
    columns_to_fix = [1,2,3,4,6,7,14,15]
    for column in columns_to_fix:
        row[column] = corresponding_row[column]
    csvwriter.writerow(row)
    

