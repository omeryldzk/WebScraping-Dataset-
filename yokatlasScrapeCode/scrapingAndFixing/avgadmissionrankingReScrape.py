import csv
from selenium import webdriver
import platform

from selenium.common import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def closePopUp(driver,wait):
    try:
        close_button = driver.find_elements(By.XPATH,
                                                 """//span[@class="featherlight-close-icon featherlight-close"]""")
    except NoSuchElementException:
        pass
    else:
        if len(close_button) == 1:
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
            driver.execute_script('arguments[0].click()', close_button[0])
        elif len(close_button) > 1:
            driver.execute_script('arguments[0].click()', close_button[1])
            try:
                close_button = driver.find_elements(By.XPATH,
                                                         """//span[@class="featherlight-close-icon featherlight-close"]""")
            except NoSuchElementException:
                pass
            else:
                close_button2 = driver.find_element(By.XPATH,
                                                         """//span[@class="featherlight-close-icon featherlight-close"]""")
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, """//span[@class="featherlight-close-icon featherlight-close"]""")))
                driver.execute_script('arguments[0].click()', close_button2)
        else:
            pass
    return
def openAll(driver,wait):
    wait.until(EC.presence_of_element_located((By.XPATH, """//a[@class="label label-success openall"]""")))
    wait.until(EC.element_to_be_clickable((By.XPATH, """//a[@class="label label-success openall"]""")))
    open_all_button = driver.find_element(By.XPATH, """//a[@class="label label-success openall"]""")
    driver.execute_script('arguments[0].click()', open_all_button)
    return 

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

count = 0
for department in csvreaderFileToFix:
    if count == 0:
        csvwriter.writerow(department)
        count += 1
        continue
    else:
        if department[10] != 0:
            if department[0] != "2021":
                if department[21] == "":
                    osymId = department[5]
                    year = department[0]
                    site = "https://yokatlas.yok.gov.tr/" + year + "/lisans.php?y=" + osymId
                    driver.get(site)
                    closePopUp(driver, wait)
                    openAll(driver, wait)
                    wait.until(EC.presence_of_element_located((By.XPATH, """//div[@id="icerik_1230"]""")))
                    rankings = driver.find_element(By.XPATH, """//div[@id="icerik_1230"]""")
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, """div#icerik_1230 table""")))
                    table = rankings.find_element(By.XPATH, """.//table[@class="table table-bordered"]""")
                    body = table.find_element(By.XPATH, ".//tbody")
                    rows = body.find_elements(By.XPATH, ".//tr")
                    for row in rows:
                        cols = row.find_elements(By.XPATH, ".//td")
                        leftCell = cols[0]
                        if leftCell.text == "TYT":
                            temp = cols[1].text
                            department[21] = temp
                                

    csvwriter.writerow(department)
