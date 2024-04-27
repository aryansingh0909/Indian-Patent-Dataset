# py -3.10 (file_name.py) to run code on specific python version
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

options = webdriver.ChromeOptions()
options.add_argument('log-level=3')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
service_object = Service(binary_path)
driver = webdriver.Chrome(service=service_object, options=options)
driver.maximize_window()
url = "https://ipindiaservices.gov.in/publicsearch"
driver.get(url)
print(driver.title)

driver.find_element(By.ID, "FromDate").send_keys("01-01-2019")
driver.find_element(By.ID, "ToDate").send_keys("01-31-2019")

captcha = driver.find_element(By.XPATH, '//*[@id="CaptchaText"]')
driver.execute_script("arguments[0].scrollIntoView();", captcha)
captcha.click()

time.sleep(9)

doc = driver.find_element(
    By.XPATH, '//*[@id="header"]/div[4]/div/div[1]/div[2]')
doc_str = doc.text
temp_list = list(doc_str.split())
pages = int(temp_list[-1])
pages_click = (math.ceil(pages / 25)) - 1
total_pages = pages_click + 1
print("Total pages = ", total_pages)
# print("pages click:", pages_click)
# print("Each page has 25 rows.")
print("Total rows:", pages)
master_df = pd.DataFrame(columns=[
    'Application Number', 'Title', 'Application Date', 'Status', 'Publication Number', 'Publication Date(U/S 11A)', 'Publication Type', 'Application Filing Date', 'Priority Number', 'Priority Country', 'Priority Date', 'Field Of Invention', 'Classification (IPC)', 'Inventor Name', 'Inventor Address', 'Inventor Country', 'Inventor Nationality', 'Applicant Name', 'Applicant Address', 'Applicant Country', 'Applicant Nationality', 'Application Type', 'E-MAIL (As Per Record)', 'ADDITIONAL-EMAIL (As Per Record)', 'E-MAIL (UPDATED Online)', 'PARENT APPLICATION NUMBER', 'PARENT APPLICATION FILING DATE', 'REQUEST FOR EXAMINATION DATE', 'FIRST EXAMINATION REPORT DATE', 'Date Of Certificate Issue', 'POST GRANT JOURNAL DATE', 'REPLY TO FER DATE', 'PCT INTERNATIONAL APPLICATION NUMBER', 'PCT INTERNATIONAL FILING DATE', 'Application Status'])
print(
    f"\nEstimated time for all pages = {round(((pages_click + 1) * 100)/ 3600, 2)} hours or {round(((pages_click + 1) * 100)/ 60, 2)} minutes.")
# print("Timer started for all pages.")
start_all = time.time()
page_number = 1
for page in range(total_pages):
    # print("Timer started for this page.")
    start = time.time()
    print(f"\nPage Number : {page + 1}")
    print("Total pages = ", total_pages)
    print("Total rows:", pages)
    # Data from the search page.
    Application_Number = []
    Title = []
    Application_Date = []
    Status = []

    # Data from Application Number link.
    publication_number2 = []
    publication_date2 = []
    publication_type2 = []
    application_filing_date2 = []
    priority_number2 = []
    priority_country2 = []
    priority_date2 = []
    field_of_invention2 = []
    classification_ipc2 = []

    inventor_name = []
    inventor_address = []
    inventor_country = []
    inventor_nationality = []

    applicant_name = []
    applicant_address = []
    applicant_country = []
    applicant_nationality = []

    # Data from Application Status link
    Application_type = []
    Email = []
    Additional_email = []
    Email_updated = []
    Parent_application_number = []
    Parent_application_filing_date = []
    Request_for_examination_date = []
    First_examaniation_report_date = []
    Date_of_certificate_issue = []
    Post_grant_journal_date = []
    Reply_to_FER_date = []
    PCT_international_application_number = []
    PCT_international_filing_date = []

    Application_Status = []

    status_dict = {'APPLICATION TYPE': Application_type, 'E-MAIL (As Per Record)': Email, 'ADDITIONAL-EMAIL (As Per Record)': Additional_email, 'E-MAIL (UPDATED Online)': Email_updated,
                   'PARENT APPLICATION NUMBER': Parent_application_number, 'PARENT APPLICATION FILING DATE': Parent_application_filing_date, 'REQUEST FOR EXAMINATION DATE': Request_for_examination_date, 'FIRST EXAMINATION REPORT DATE': First_examaniation_report_date, 'Date Of Certificate Issue': Date_of_certificate_issue, 'POST GRANT JOURNAL DATE': Post_grant_journal_date, 'REPLY TO FER DATE': Reply_to_FER_date, 'PCT INTERNATIONAL APPLICATION NUMBER': PCT_international_application_number, 'PCT INTERNATIONAL FILING DATE': PCT_international_filing_date}

    r = driver.find_elements(By.XPATH, '//*[@id="tableData"]/tbody/tr')
    c = driver.find_elements(By.XPATH, '//*[@id="tableData"]/tbody/tr[1]/td')

    rc = len(r)
    cc = len(c)

    for i in range(1, rc + 1, 1):
        for j in range(1, cc + 1, 1):
            d = driver.find_element(
                By.XPATH, "//tr["+str(i)+"]/td["+str(j)+"]")
            if (j == 1):
                print(d.text)
                Application_Number.append(d.text)

                # Clicking on Application Number link and switching to that window.
                d.click()

                if (len(driver.window_handles) < 2):
                    driver.refresh()
                    print("refreshed")
                    application_number_button = driver.find_element(
                        By.XPATH, "//tr["+str(i)+"]/td["+str(j)+"]/button")
                    application_number_button.click()
                if len(driver.window_handles) < 2:
                    print(
                        "There are not enough window handles to switch to the second window after clicking on Application Number link.")
                    publication_number2.append("NA")
                    publication_date2.append("NA")
                    publication_type2.append("NA")
                    application_filing_date2.append("NA")
                    priority_number2.append("NA")
                    priority_country2.append("NA")
                    priority_date2.append("NA")
                    field_of_invention2.append("NA")
                    classification_ipc2.append("NA")
                    inventor_name.append("NA")
                    inventor_address.append("NA")
                    inventor_country.append("NA")
                    inventor_nationality.append("NA")
                    applicant_name.append("NA")
                    applicant_address.append("NA")
                    applicant_country.append("NA")
                    applicant_nationality.append("NA")
                    Application_type.append("NA")
                    Email.append("NA")
                    Additional_email.append("NA")
                    Email_updated.append("NA")
                    Parent_application_number.append("NA")
                    Parent_application_filing_date.append("NA")
                    Request_for_examination_date.append("NA")
                    Application_Status.append("NA")
                    First_examaniation_report_date.append("NA")
                    Date_of_certificate_issue.append("NA")
                    Post_grant_journal_date.append("NA")
                    Reply_to_FER_date.append("NA")
                    PCT_international_application_number.append("NA")
                    PCT_international_filing_date.append("NA")
                else:
                    driver.switch_to.window(driver.window_handles[1])
                    try_count = 0
                    max_tries = 10
                    while (try_count < max_tries):
                        try:
                            wait = WebDriverWait(driver, 10)
                            element = wait.until(EC.presence_of_element_located(
                                (By.CLASS_NAME, 'tab-content')))
                            # print(driver.current_url)

                            row_ele = driver.find_elements(
                                By.XPATH, '//*[@id="home"]/table/tbody/tr')
                            col_ele = driver.find_elements(
                                By.XPATH, '//*[@id="home"]/table/tbody/tr[1]/td')
                            rows = len(row_ele)
                            # cols = len(col_ele)

                            for k in range(1, 12, 1):
                                ele = driver.find_element(
                                    By.XPATH, "//*[@id='home']/table/tbody/tr["+str(k)+"]/td[2]")
                                if (k == 2):
                                    publication_number2.append(ele.text)
                                if (k == 3):
                                    publication_date2.append(ele.text)
                                if (k == 4):
                                    publication_type2.append(ele.text)
                                if (k == 6):
                                    application_filing_date2.append(ele.text)
                                if (k == 7):
                                    priority_number2.append(ele.text)
                                if (k == 8):
                                    priority_country2.append(ele.text)
                                if (k == 9):
                                    priority_date2.append(ele.text)
                                if (k == 10):
                                    field_of_invention2.append(ele.text)
                                if (k == 11):
                                    classification_ipc2.append(ele.text)

                            row_ele_inventor = driver.find_elements(
                                By.XPATH, '//*[@id="home"]/table/tbody/tr[13]/td/table/tbody/tr')
                            rows_inventor = len(row_ele_inventor)
                            # print("No. of rows in inventor is: ", rows_inventor)
                            cols_inventor = 4
                            if (rows_inventor != 0):
                                col_ele_inventor = driver.find_elements(
                                    By.XPATH, '//*[@id="home"]/table/tbody/tr[13]/td/table/tbody/tr[2]/td')
                                cols_inventor = len(col_ele_inventor)
                            # print("No. of cols in inventor is: ", cols_inventor)
                            str_invname = ""
                            str_invaddress = ""
                            str_invcountry = ""
                            str_invnationality = ""

                            for m in range(2, rows_inventor + 1, 1):
                                for n in range(1, cols_inventor + 1, 1):
                                    element = driver.find_element(
                                        By.XPATH, "//*[@id='home']/table/tbody/tr[13]/td/table/tbody/tr["+str(m)+"]/td["+str(n)+"]")
                                    if (n == 1):
                                        str_invname = (
                                            str_invname + "#" + element.text)
                                    if (n == 2):
                                        str_invaddress = (
                                            str_invaddress + "#" + element.text)
                                    if (n == 3):
                                        str_invcountry = (
                                            str_invcountry + "#" + element.text)
                                    if (n == 4):
                                        str_invnationality = (
                                            str_invnationality + "#" + element.text)

                            inventor_name.append(str_invname)
                            inventor_address.append(str_invaddress)
                            inventor_country.append(str_invcountry)
                            inventor_nationality.append(str_invnationality)

                            row_ele_applicant = driver.find_elements(
                                By.XPATH, '//*[@id="home"]/table/tbody/tr[15]/td/table/tbody/tr')
                            rows_applicant = len(row_ele_applicant)
                            # print("No. of rows in applicant is: ", rows_applicant)
                            cols_applicant = 4
                            if (rows_applicant != 0):
                                col_ele_applicant = driver.find_elements(
                                    By.XPATH, '//*[@id="home"]/table/tbody/tr[15]/td/table/tbody/tr[2]/td')
                                cols_applicant = len(col_ele_applicant)
                            # print("No. of cols in applicant is: ", cols_applicant)
                            str_appname = ""
                            str_appaddress = ""
                            str_appcountry = ""
                            str_appnationality = ""

                            for m in range(2, rows_applicant + 1, 1):
                                for n in range(1, cols_applicant + 1, 1):
                                    element = driver.find_element(
                                        By.XPATH, "//*[@id='home']/table/tbody/tr[15]/td/table/tbody/tr["+str(m)+"]/td["+str(n)+"]")
                                    if (n == 1):
                                        str_appname = (
                                            str_appname + "#" + element.text)
                                    if (n == 2):
                                        str_appaddress = (
                                            str_appaddress + "#" + element.text)
                                    if (n == 3):
                                        str_appcountry = (
                                            str_appcountry + "#" + element.text)
                                    if (n == 4):
                                        str_appnationality = (
                                            str_appnationality + "#" + element.text)
                            applicant_name.append(str_appname)
                            applicant_address.append(str_appaddress)
                            applicant_country.append(str_appcountry)
                            applicant_nationality.append(str_appnationality)

                            # Clicking on Application Status link inside Application Number webpage and switching to that window.
                            l = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/table/tbody/tr[18]/td/input'))).find_element(
                                By.XPATH, '//*[@id="home"]/table/tbody/tr[18]/td/input')
                            l.click()
                            if (len(driver.window_handles) < 3):
                                driver.refresh()
                                print("refreshed second tab.")
                                application_status_button = driver.find_element(
                                    By.XPATH, '//*[@id="home"]/table/tbody/tr[18]/td/input')
                                application_status_button.click()
                            if (len(driver.window_handles) < 3):
                                print(
                                    "There are not enough window handles to switch to the third window after clicking on Application Status link.")
                                Application_type.append("NA")
                                Email.append("NA")
                                Additional_email.append("NA")
                                Email_updated.append("NA")
                                Parent_application_number.append("NA")
                                Parent_application_filing_date.append("NA")
                                Request_for_examination_date.append("NA")
                                Application_Status.append("NA")
                                First_examaniation_report_date.append("NA")
                                Date_of_certificate_issue.append("NA")
                                Post_grant_journal_date.append("NA")
                                Reply_to_FER_date.append("NA")
                                PCT_international_application_number.append(
                                    "NA")
                                PCT_international_filing_date.append("NA")

                            else:
                                driver.switch_to.window(
                                    driver.window_handles[2])
                                try_count2 = 0
                                max_tries2 = 10
                                while (try_count2 < max_tries2):
                                    try:
                                        wait = WebDriverWait(driver, 10)
                                        element = wait.until(EC.presence_of_element_located(
                                            (By.CLASS_NAME, 'table-striped')))

                                        status_element = driver.find_element(
                                            By.XPATH, '//*[@id="Content"]/div[2]/table/tbody/tr[2]/td[1]')
                                        if (status_element.text == "APPLICATION STATUS"):
                                            div_num = 2
                                        else:
                                            div_num = 3

                                        if (div_num == 3):
                                            status_element = driver.find_element(
                                                By.XPATH, '//*[@id="Content"]/div[3]/table/tbody/tr[2]/td[2]')
                                            Application_Status.append(
                                                status_element.text)
                                            row_ele = driver.find_elements(
                                                By.XPATH, '//*[@id="Content"]/div[2]/table/tbody/tr')
                                            col_ele = driver.find_elements(
                                                By.XPATH, '//*[@id="Content"]/div[2]/table/tbody/tr[2]/td')
                                            rows = len(row_ele)
                                            cols = len(col_ele)
                                            # print("No. of rows in application status is: ", rows)
                                            # print("No. of cols in application status is: ", cols)

                                            Application_type_flag = 0
                                            Email_flag = 0
                                            Additional_email_flag = 0
                                            Email_updated_flag = 0
                                            Parent_application_number_flag = 0
                                            Parent_application_filing_date_flag = 0
                                            Request_for_examination_date_flag = 0
                                            First_examaniation_report_date_flag = 0
                                            Date_of_certificate_issue_flag = 0
                                            Post_grant_journal_date_flag = 0
                                            Reply_to_FER_date_flag = 0
                                            PCT_international_application_number_flag = 0
                                            PCT_international_filing_date_flag = 0

                                            for k in range(2, rows + 1, 1):
                                                field = driver.find_element(
                                                    By.XPATH, "//tr["+str(k)+"]/td[1]")
                                                value = driver.find_element(
                                                    By.XPATH, "//tr["+str(k)+"]/td[2]")
                                                if (field.text in status_dict):
                                                    status_dict[field.text].append(
                                                        value.text)
                                                if (field.text == 'APPLICATION TYPE'):
                                                    Application_type_flag = 1
                                                elif (field.text == 'E-MAIL (As Per Record)'):
                                                    Email_flag = 1
                                                elif (field.text == 'ADDITIONAL-EMAIL (As Per Record)'):
                                                    Additional_email_flag = 1
                                                elif (field.text == 'E-MAIL (UPDATED Online)'):
                                                    Email_updated_flag = 1
                                                elif (field.text == 'PARENT APPLICATION NUMBER'):
                                                    Parent_application_number_flag = 1
                                                elif (field.text == 'PARENT APPLICATION FILING DATE'):
                                                    Parent_application_filing_date_flag = 1
                                                elif (field.text == 'REQUEST FOR EXAMINATION DATE'):
                                                    Request_for_examination_date_flag = 1
                                                elif (field.text == 'FIRST EXAMINATION REPORT DATE'):
                                                    First_examaniation_report_date_flag = 1
                                                elif (field.text == 'Date Of Certificate Issue'):
                                                    Date_of_certificate_issue_flag = 1
                                                elif (field.text == 'POST GRANT JOURNAL DATE'):
                                                    Post_grant_journal_date_flag = 1
                                                elif (field.text == 'REPLY TO FER DATE'):
                                                    Reply_to_FER_date_flag = 1
                                                elif (field.text == 'PCT INTERNATIONAL APPLICATION NUMBER'):
                                                    PCT_international_application_number_flag = 1
                                                elif (field.text == 'PCT INTERNATIONAL FILING DATE'):
                                                    PCT_international_filing_date_flag = 1

                                            if (Application_type_flag == 0):
                                                Application_type.append('NA')
                                            if (Email_flag == 0):
                                                Email.append('NA')
                                            if (Additional_email_flag == 0):
                                                Additional_email.append('NA')
                                            if (Email_updated_flag == 0):
                                                Email_updated.append('NA')
                                            if (Parent_application_number_flag == 0):
                                                Parent_application_number.append(
                                                    'NA')
                                            if (Parent_application_filing_date_flag == 0):
                                                Parent_application_filing_date.append(
                                                    'NA')
                                            if (Request_for_examination_date_flag == 0):
                                                Request_for_examination_date.append(
                                                    'NA')
                                            if (First_examaniation_report_date_flag == 0):
                                                First_examaniation_report_date.append(
                                                    'NA')
                                            if (Date_of_certificate_issue_flag == 0):
                                                Date_of_certificate_issue.append(
                                                    'NA')
                                            if (Post_grant_journal_date_flag == 0):
                                                Post_grant_journal_date.append(
                                                    'NA')
                                            if (Reply_to_FER_date_flag == 0):
                                                Reply_to_FER_date.append('NA')
                                            if (PCT_international_application_number_flag == 0):
                                                PCT_international_application_number.append(
                                                    'NA')
                                            if (PCT_international_filing_date_flag == 0):
                                                PCT_international_filing_date.append(
                                                    'NA')
                                        elif (div_num == 2):
                                            status_element = status_element = driver.find_element(
                                                By.XPATH, '//*[@id="Content"]/div[2]/table/tbody/tr[2]/td[2]')
                                            Application_Status.append(
                                                status_element.text)

                                            Application_type.append('NA')
                                            Email.append('NA')
                                            Additional_email.append('NA')
                                            Email_updated.append('NA')
                                            Parent_application_number.append(
                                                'NA')
                                            Parent_application_filing_date.append(
                                                'NA')
                                            Request_for_examination_date.append(
                                                'NA')
                                            First_examaniation_report_date.append(
                                                'NA')
                                            Date_of_certificate_issue.append(
                                                'NA')
                                            Post_grant_journal_date.append(
                                                'NA')
                                            Reply_to_FER_date.append('NA')
                                            PCT_international_application_number.append(
                                                'NA')
                                            PCT_international_filing_date.append(
                                                'NA')
                                        driver.close()
                                        driver.switch_to.window(
                                            driver.window_handles[1])
                                        driver.close()
                                        driver.switch_to.window(
                                            driver.window_handles[0])
                                        break
                                    except:
                                        if (try_count2 == max_tries2):
                                            print(
                                                f"Maximum tries {max_tries2} reached for trying to load the third tab correctly.")
                                            print(
                                                "Still no third tab was opened and loaded properly so appending NA to all the fields of third tab.")
                                            Application_type.append("NA")
                                            Email.append("NA")
                                            Additional_email.append("NA")
                                            Email_updated.append("NA")
                                            Parent_application_number.append(
                                                "NA")
                                            Parent_application_filing_date.append(
                                                "NA")
                                            Request_for_examination_date.append(
                                                "NA")
                                            Application_Status.append("NA")
                                            First_examaniation_report_date.append(
                                                "NA")
                                            Date_of_certificate_issue.append(
                                                "NA")
                                            Post_grant_journal_date.append(
                                                "NA")
                                            Reply_to_FER_date.append("NA")
                                            PCT_international_application_number.append(
                                                "NA")
                                            PCT_international_filing_date.append(
                                                "NA")
                                            print(
                                                "Appended NA due to no available tab to switch to :( ")
                                            break
                                        print("Timeout Exception for third tab.")
                                        driver.close()
                                        driver.switch_to.window(
                                            driver.window_handles[1])
                                        # print("Closing the third tab which failed to load and switching to second tab.")
                                        l.click()
                                        # print("Clicked on the Application Status button again.")
                                        if (len(driver.window_handles) < 3):
                                            driver.refresh()
                                            print("refreshed second tab.")
                                            application_status_button = driver.find_element(
                                                By.XPATH, '//*[@id="home"]/table/tbody/tr[18]/td/input')
                                            application_status_button.click()

                                        driver.switch_to.window(
                                            driver.window_handles[2])
                                        # print("Switching to the third tab again after clicking on the application number button.")
                                        try_count2 += 1
                            break
                        except:
                            if (try_count == max_tries):
                                print(f"Maximum tries {max_tries} reached.")
                                print(
                                    "Still no second tab was opened and loaded properly so appending NA to all the fields of second and third tab.")
                                publication_number2.append("NA")
                                publication_date2.append("NA")
                                publication_type2.append("NA")
                                application_filing_date2.append("NA")
                                priority_number2.append("NA")
                                priority_country2.append("NA")
                                priority_date2.append("NA")
                                field_of_invention2.append("NA")
                                classification_ipc2.append("NA")
                                inventor_name.append("NA")
                                inventor_address.append("NA")
                                inventor_country.append("NA")
                                inventor_nationality.append("NA")
                                applicant_name.append("NA")
                                applicant_address.append("NA")
                                applicant_country.append("NA")
                                applicant_nationality.append("NA")
                                Application_type.append("NA")
                                Email.append("NA")
                                Additional_email.append("NA")
                                Email_updated.append("NA")
                                Parent_application_number.append("NA")
                                Parent_application_filing_date.append("NA")
                                Request_for_examination_date.append("NA")
                                Application_Status.append("NA")
                                First_examaniation_report_date.append("NA")
                                Date_of_certificate_issue.append("NA")
                                Post_grant_journal_date.append("NA")
                                Reply_to_FER_date.append("NA")
                                PCT_international_application_number.append(
                                    "NA")
                                PCT_international_filing_date.append("NA")
                                print(
                                    "Appended NA due to no available tab to switch to :( ")
                                break

                            print("Timeout Exception")
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            # print("Closing the second tab which failed to load and switching to first tab.")
                            d.click()
                            # print("Clicked on the Application Number button again.")
                            if (len(driver.window_handles) < 2):
                                driver.refresh()
                                print("refreshed")
                                application_number_button = driver.find_element(
                                    By.XPATH, "//tr["+str(i)+"]/td["+str(j)+"]/button")
                                application_number_button.click()

                            driver.switch_to.window(driver.window_handles[1])
                            # print("Switching to the second tab again after clicking on the application number button.")
                            try_count += 1

            elif (j == 2):
                # print(d.text)
                Title.append(d.text)
            elif (j == 3):
                # print(d.text)
                Application_Date.append(d.text)
            elif (j == 4):
                # print(d.text)
                Status.append(d.text)

        # break

        if (len(Application_Number) != len(priority_number2) or len(Application_Number) != len(Application_type)):
            print(
                "Length of Application Number, Priority Number and Application Type is not equal.")
            print("Length of Application Number: ", len(Application_Number))
            print("Length of Priority Number: ", len(priority_number2))
            print("Length of Application Type: ", len(Application_type))
            break
    df_t = pd.DataFrame(list(zip(Application_Number, Title, Application_Date, Status, publication_number2, publication_date2, publication_type2, application_filing_date2, priority_number2, priority_country2, priority_date2, field_of_invention2, classification_ipc2, inventor_name, inventor_address, inventor_country, inventor_nationality, applicant_name, applicant_address, applicant_country, applicant_nationality, Application_type, Email, Additional_email, Email_updated, Parent_application_number, Parent_application_filing_date, Request_for_examination_date, First_examaniation_report_date, Date_of_certificate_issue, Post_grant_journal_date, Reply_to_FER_date, PCT_international_application_number, PCT_international_filing_date, Application_Status)), columns=[
                        'Application Number', 'Title', 'Application Date', 'Status', 'Publication Number', 'Publication Date(U/S 11A)', 'Publication Type', 'Application Filing Date', 'Priority Number', 'Priority Country', 'Priority Date', 'Field Of Invention', 'Classification (IPC)', 'Inventor Name', 'Inventor Address', 'Inventor Country', 'Inventor Nationality', 'Applicant Name', 'Applicant Address', 'Applicant Country', 'Applicant Nationality', 'Application Type', 'E-MAIL (As Per Record)', 'ADDITIONAL-EMAIL (As Per Record)', 'E-MAIL (UPDATED Online)', 'PARENT APPLICATION NUMBER', 'PARENT APPLICATION FILING DATE', 'REQUEST FOR EXAMINATION DATE', 'FIRST EXAMINATION REPORT DATE', 'Date Of Certificate Issue', 'POST GRANT JOURNAL DATE', 'REPLY TO FER DATE', 'PCT INTERNATIONAL APPLICATION NUMBER', 'PCT INTERNATIONAL FILING DATE', 'Application Status'])
    master_df = pd.concat([master_df, df_t], ignore_index=True)
    out_path = "D:\\web_scraping_project\\data_save\\2019\\jan2019\\jan2019.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    master_df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    master_df.to_csv(
        "D:\web_scraping_project\data_save\\2019\\jan2019\\jan2019.csv", index=False)
    l = driver.find_element(
        By.XPATH, '//*[@id="header"]/div[4]/div/div[1]/form/div/button[3]')
    try_count3 = 0
    max_tries3 = 10
    while (try_count3 < max_tries3):
        try:
            l.click()
            wait = WebDriverWait(driver, 10)
            p = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'Selected')))
            current_page = int(p.text)
            # print("Current page: ", current_page)
            break
        except:
            if (try_count3 == max_tries3):
                print(
                    'Max tries reached for clicking on next page button and page not loading.')
                break
            print('Clicked on next page but not loaded. Refreshing page.')
            driver.refresh()
            try_count3 += 1
    end = time.time()
    print(
        f"\nTime elapsed in previous page: {round(((end - start) / 60), 2)} minutes or {round(end - start, 2)} seconds")
    print(
        f"Estimated time left: {round((((total_pages - page_number) * 100) / 3600) , 2)} hours or {round((((total_pages - page_number) * 100) / 60) , 2)} minutes")
    print(
        f"Time elapsed from start till now is: {round(((time.time() - start_all) / 3600), 2)}  hours or {round(((time.time() - start_all) / 60), 2)} minutes")
    print(
        f"Estimated time for all pages = {round(((pages_click + 1) * 100)/ 3600, 2)} hours or {round(((pages_click + 1) * 100)/ 60, 2)} minutes.")
    page_number += 1

end_all = time.time()
print(
    f"\nEstimated time for all pages = {round(((pages_click + 1) * 100)/ 3600, 2)} hours or {round(((pages_click + 1) * 100)/ 60, 2)} minutes.")
print(
    f"Time taken for all pages: {(round(((end_all - start_all) / 3600), 2))} hours or {(round(((end_all - start_all) / 60), 1))} minutes")

driver.quit()
print(master_df)
print("Total rows shown after searching were:", pages)
print(f"Length of the dataframe is : {(master_df.shape[0])}")