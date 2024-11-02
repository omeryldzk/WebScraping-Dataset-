from selenium import webdriver
from scrapeFunctions import *


#MAIN FUNCTION
def main():
    #First we will select our program type option
    type = ""
    while True:
        type = input("Please enter the program type you wanna scrape (only available inputs are 'ea', 'söz', 'dil', 'say')('- 1' to exit)")
        if type == "-1":
            return
        elif type == 'say' or type == 'söz' or type == 'dil' or type == 'ea':
            break
    selectOption(type)
    #We then decide numbers of elements in the table
    selectOption("100")
    #Then we decide the university type (private/government)
    uniType = ""
    while True:
        uniType = input("Please enter the university type you wanna scrape (only available inputs are 'Devlet', 'Vakıf')('- 1' to exit)")
        if uniType == "-1":
            return
        elif uniType == 'Devlet' or uniType == 'Vakıf':
            break
    selectOption(uniType)
    time.sleep(3)

    #This function can be applied to use the navigator bar at the bottom and start from a certain page
    # clickPageButton("4")
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




