import re
def extract_last_integer(input_string):
    integers = re.findall(r'\d+', input_string)
    
    if integers:
        return int(integers[-1])
    else:
        return None
from selenium import webdriver
# (pip install selenium)
from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path # this will get you the path variable
# (pip install chromedriver-py)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import math
import calendar
from datetime import datetime
import os 
options = webdriver.ChromeOptions()
options.add_argument('log-level=3')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
# service_object = Service(binary_path)
# driver = webdriver.Chrome(service=service_object, options=options)
chromedriver_path = r'D:\web_scraping_project\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome(executable_path= chromedriver_path, options=options)
driver.maximize_window()
url = "https://www.mca.gov.in/mcafoportal/showIndexOfCharges.do"
driver.get(url)
print(driver.title)
print("Opened the website")
my_list = ['L99999GJ1987PLC009768', 'L72100MH2000PLC128949', 'L63011WB1972PLC217415', 'L25209TN1994PLC027000','U99999MH1979PTC021609']
# columns = ['SRN', 'ChargeID', 'Charge_Holder_Name', 'DateofCreation', 'DateofModification', 'DateofSatisfaction', 'Amount', 'Address']
master_df = pd.DataFrame()
for cin in my_list:
    driver.find_element(By.XPATH,'//*[@id="companyID"]').send_keys(cin)

    captcha = driver.find_element(By.XPATH, '//*[@id="captcha"]')
    driver.execute_script("arguments[0].scrollIntoView();", captcha)
    captcha.click()
    print("Waiting to enter captcha.")
    time.sleep(15)

    charges_info = driver.find_element(By.XPATH, '//*[@id="charges_info"]').text
    total_entries = extract_last_integer(charges_info)
    print("Total Entries for ",cin, ": ",total_entries)
    num_clicks = total_entries / 10
    for i in range(math.ceil(num_clicks)):
        next_button = driver.find_element(By.XPATH, '//*[@id="charges_next"]')
        next_button.click()
        time.sleep(1)
        table_element = driver.find_element(By.XPATH, '//*[@id="charges"]')
        df_temp = pd.read_html(table_element.get_attribute('outerHTML'))[0]
        master_df = pd.concat([master_df, df_temp], ignore_index=True)
        master_df['CIN'] = cin
        # master_df.to_csv(path + cin + '.csv')
        master_df.to_csv(cin + '.csv')
    

