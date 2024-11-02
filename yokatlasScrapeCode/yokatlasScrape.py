from selenium import webdriver
from scrapeFunctions import *


#MAIN FUNCTION
def main():
    #First we will select our program type option
    selectOption("ea")
    #We then decide numbers of elements in the table
    selectOption("100")
    #Then we decide the university type (private/government)
    selectOption("Vakıf")
    time.sleep(3)

    #This function can be applied to use the navigator bar at the bottom and start from a certain page
    # clickPageButton("4")
    while True:
        temp = driver.find_element(By.XPATH,"""//table[@id="mydata"]""")
        body = temp.find_element(By.XPATH,".//tbody")
        rows = body.find_elements(By.XPATH,".//tr")
        for row in rows:
            original_window = enterDepartment(row)
            scrapeDepartment(tempDict,writer)
            csvfile.flush()
            exitDepartment(original_window)
    
        if clickNextPageButton() == 1:
            break
    return
     

#Creates the csv file, writes the header for all the features it will hold. 
#It will utilize writer.writerow() function for entering new rows to the csv file
csvfile = open("departments(test).csv", mode="a")
writer = csv.DictWriter(csvfile, fieldnames=featurenames)
writer.writeheader()
tempDict = {}
for i in featurenames:
    tempDict[i] = None
#Site link and path for utilizing the webdriver are introduced to the code. Then it opens the site on chrome by driver.get(site)
driver.get(site)
main()


    






# temp = driver.find_element(By.XPATH,"""//div[@id="icerik_1000_1"]""")
# rows = temp.find_elements(By.XPATH,".//tr")
# for row in rows:
    
#     cols = row.find_elements(By.XPATH,".//td")
    
#     for col in cols:
#         print(col.text)




