from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import pwinput
import pandas as pd

def login(driver = webdriver.Chrome()):
    #navigating to the myAshoka login page
    driver.get("https://my.ashoka.edu.in/SIS/Login.aspx")

    #selecting the Google login method
    driver.find_element(By.XPATH, "//*[@id='divLogin']/div[1]/div/a").click()

    #logging in with Google
    inpEmail = input("Enter your email: ")
    email = driver.find_element(By.XPATH, "//*[@id='identifierId']")
    email.send_keys(inpEmail)
    driver.find_element(By.XPATH, "//*[@id='identifierNext']/div/button").click()
    if (driver.page_source.find("Enter your password")):
        inpPassword = pwinput.pwinput("Enter your password: ")
        password = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
        WebDriverWait(driver, 10).until(lambda p: password.is_displayed())
        password.send_keys(inpPassword)
        driver.find_element(By.CSS_SELECTOR, "#passwordNext > div > button").click()
    
    print("Logging in! Please wait...")
    return driver

def selectDateRange(driver):
    #user input for date range
    inpFromDate = input("Enter the start date (dd/mm/yyyy): ")
    inpToDate = input("Enter the end date (dd/mm/yyyy): ")


    #selecting the to date
    toDateField = driver.find_element(By.ID, "ContentPlaceHolder1_txttodate")
    toDateField.click()
    toDateField.send_keys(Keys.CONTROL + "A", Keys.DELETE)
    toDateField.send_keys(inpToDate)
    toDateField.send_keys(Keys.ENTER)

    #selecting the from date
    fromDateField = driver.find_element(By.ID, "ContentPlaceHolder1_txtfromdate")
    fromDateField.click()
    fromDateField.send_keys(Keys.CONTROL + "A", Keys.DELETE)
    fromDateField.send_keys(inpFromDate)
    fromDateField.send_keys(Keys.ENTER)

    #clicking the submit button
    driver.find_element(By.ID, "ContentPlaceHolder1_btnGet").click()

    #selecting all dining transactions
    selectDropdown = Select(driver.find_element(By.XPATH, "//*[@id='ContentPlaceHolder1_divView']/div/div[2]/div[3]/div/div/table/tfoot/tr/th/select[1]"))
    selectDropdown.select_by_visible_text("All")

def getMessBill(driver):
    table = pd.read_html(driver.find_element(By.TAG_NAME, "table").get_attribute("outerHTML"))[0]
    
    #dropping the last row and the rows with NaN amount values
    table = table.loc[table["Amount"].notna()].iloc[:-1, :]
    
    #converting the amount column to numeric from object
    table["Amount"] = table["Amount"].apply(pd.to_numeric)

    #calculating the total amount and printing it
    print("The bill is: ", table["Amount"].sum())

def main():
    #logging in
    driver = login()
    time.sleep(5)

    #navigating to the dining transactions page
    driver.get("https://my.ashoka.edu.in/SIS/Contents/Reports/my_dining_transactions.aspx")

    #selecting the date range
    selectDateRange(driver)
    getMessBill(driver)
    driver.quit()

if __name__ == "__main__":
    main()