from scrapeFunctions import *


#MAIN FUNCTION
def main():
    scrapeFunctions = ScrapeFunctions()
    if scrapeFunctions.type == "" or scrapeFunctions.uniType == "" or scrapeFunctions.startPage == "":
        return
    #First we will select our program type option
    scrapeFunctions.selectOption(scrapeFunctions.type)
    #We then decide numbers of elements in the table
    scrapeFunctions.selectOption("100")
    #Then we decide the university type (private/government)
    scrapeFunctions.selectOption(scrapeFunctions.uniType)
    time.sleep(3)

    #This function can be applied to use the navigator bar at the bottom and start from a certain page
    for i in range(0,scrapeFunctions.startPage-1):
        scrapeFunctions.clickNextPageButton()
    while True:
        temp = scrapeFunctions.driver.find_element(By.XPATH,"""//table[@id="mydata"]""")
        body = temp.find_element(By.XPATH,".//tbody")
        rows = body.find_elements(By.XPATH,".//tr")
        for row in rows:
            original_window = scrapeFunctions.enterDepartment(row)
            scrapeFunctions.scrapeDepartment()
            scrapeFunctions.csvfile.flush()
            scrapeFunctions.exitDepartment(original_window)
    
        if scrapeFunctions.clickNextPageButton() == 1:
            break
    return
     


main()


    






# temp = driver.find_element(By.XPATH,"""//div[@id="icerik_1000_1"]""")
# rows = temp.find_elements(By.XPATH,".//tr")
# for row in rows:
    
#     cols = row.find_elements(By.XPATH,".//td")
    
#     for col in cols:
#         print(col.text)




