from selenium import webdriver
from scrapeFunctions import *


#MAIN FUNCTION
def main():
    if type == "" or uniType == "" or startPage == "":
        return
    #First we will select our program type option
    selectOption(type)
    #We then decide numbers of elements in the table
    selectOption("100")
    #Then we decide the university type (private/government)
    selectOption(uniType)
    time.sleep(3)

    #This function can be applied to use the navigator bar at the bottom and start from a certain page
    for i in range(0,startPage-1):
        clickNextPageButton()
    while True:
        temp = driver.find_element(By.XPATH,"""//table[@id="mydata"]""")
        body = temp.find_element(By.XPATH,".//tbody")
        rows = body.find_elements(By.XPATH,".//tr")
        for row in rows:
            original_window = enterDepartment(row)
            scrapeDepartment(tempDict,writer,regionFile)
            csvfile.flush()
            exitDepartment(original_window)
    
        if clickNextPageButton() == 1:
            break
    return
     


main()


    






# temp = driver.find_element(By.XPATH,"""//div[@id="icerik_1000_1"]""")
# rows = temp.find_elements(By.XPATH,".//tr")
# for row in rows:
    
#     cols = row.find_elements(By.XPATH,".//td")
    
#     for col in cols:
#         print(col.text)




