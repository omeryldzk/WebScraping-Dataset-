from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import platform
import csv

site = 'https://tr.wiktionary.org/wiki/Vikis%C3%B6zl%C3%BCk:Diller_listesi'
if platform.system() == "Darwin":
    path = './resources/mac_chrome_driver/chromedriver'
elif platform.system() == "Windows":
    path = '.\\resources\\windows_chrome_driver\\chromedriver.exe'
cService = webdriver.ChromeService(executable_path = path)
driver = webdriver.Chrome(service = cService)
wait = WebDriverWait(driver, 30)
driver.get(site)
tables = driver.find_elements(By.XPATH, """//table""")
idCounter = 0
features = ["id","languageName"]
tempDictionary = {}
newFile = open("languages.csv", "w", encoding="utf-8", newline='')
csvwriter = csv.DictWriter(newFile, fieldnames=features)
csvwriter.writeheader()
for i in features:
    tempDictionary[i] = None
for table in tables:
    tableBody = table.find_element(By.XPATH, ".//tbody")
    rows = tableBody.find_elements(By.XPATH, ".//tr")
    for row in rows:
        tds = row.find_elements(By.XPATH, ".//td")
        language = tds[2].text
        tempDictionary["id"] = idCounter
        tempDictionary["languageName"] = language
        idCounter += 1
        csvwriter.writerow(tempDictionary)
