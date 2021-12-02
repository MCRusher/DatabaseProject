#dependencies:
#./.kaggle/kaggle.json containing kaggle api key
#-obtain from: a free kaggle account
#firefox (either as default browser or in the system path)
#-obtain from: just install it, Options are browser specific so this won't work correctly with others
#./geckodriver (firefox webdriver, with windows and linux versions)
#-obtain from: https://github.com/mozilla/geckodriver/releases

import os
from os.path import exists, join
import requests as rq
#this selenium stuff took like 5 hours to get working btw
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.keys import Keys
import time

#tell kaggle where to find the kaggle api key info before importing it
os.environ["KAGGLE_CONFIG_DIR"] = ".kaggle"

import kaggle
from kaggle.api import kaggle_api_extended as kapi
#from kaggle.api.kaggle_api_extended import KaggleApi

#connect to kaggle
api = kapi.KaggleApi()
api.authenticate()

#make datasets directory if it doesn't exist
if not exists("datasets"):
    os.mkdir("datasets")
#os.chdir("datasets")

#download datasets from kaggle
api.dataset_download_file("imdevskp/corona-virus-report","country_wise_latest.csv", path="./datasets")
api.dataset_download_file("tanuprabhu/population-by-country-2020","population_by_country_2020.csv", path="./datasets")

#download datasheet from github, is the source sheet for an old dependency
#draw from new source, with same data but not downloaded as a zipped archive
req = rq.get("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv")
with open("./datasets/vaccinations.csv", "wb") as file:
    file.write(req.content)

#remember to change USA to United States for consistency with other tables for the tables from selenium

#os.chdir("..")

#set up absolute path to use as firefox download directory
datasets_dir = join(os.getcwd(), "datasets")

#configure firefox to download csv files automatically without a prompt
op = webdriver.FirefoxOptions()
op.set_preference("browser.download.folderList", 2)
op.set_preference("browser.download.manager.showWhenStarting", False)
op.set_preference("browser.download.dir", datasets_dir)
op.set_preference("browser.helperApps.neverAsk.saveToDisk","text/csv")

#list of variants on the website to downloaded datasheets for
variants = ["omicron", "gh490r", "delta", "alpha", "beta", "gamma", "lambda", "mu"]

#open a firefox session
with webdriver.Firefox(options=op) as driver:
    #load page that contains the datasheets
    driver.get("https://mendel3.bii.a-star.edu.sg/METHODS/corona/gamma/MUTATIONS/hcov19-variants/")
    #unique feature to locate download button with (does not have an id or name)
    xpath = """
            //a[@download='countrySubmissionCount.csv']
            """.strip()#trim newlines (using multiline to make it easier to read)
    #the absolute path to each file once they've just been downloaded
    file_path = join(datasets_dir, "countrySubmissionCount.csv")
    #download datasheet for each variant
    for variant in variants:
        #wait for page to load in download button
        elem = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((
                By.XPATH,
                xpath
            ))
        )

        #give the blob time to load into memory (otherwise may only get a partial download)
        time.sleep(5)
        
        #click the download button
        elem.click()
        
        #the final absolute path of the current dataset file that it will be renamed to
        renamed_file_path = join(datasets_dir, variant+".csv")
        
        #if a previous version of the final dataset file exists, delete it
        if exists(renamed_file_path):
            os.remove(renamed_file_path)
        #rename the datasheet to its final filename
        os.rename(file_path, renamed_file_path)
        
        #select drop down menu and choose next option down from current (this tooks 2 hours to get to this point btw)
        #drop menu has no unique features, have to walk to it
        elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div")
        #click to open drop menu, hit down, and press enter to select next element (on last element it will wrap but this doesn't matter)
        AC(driver).context_click(elem).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
