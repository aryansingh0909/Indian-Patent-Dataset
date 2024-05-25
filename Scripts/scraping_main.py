from tqdm import tqdm
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from chromedriver_py import binary_path  # this will get you the path variable

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime as dt
import time
import pandas as pd

import argparse


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", type=int, default=1)
    parser.add_argument("--year", type=int, default=2024)
    parser.add_argument("--skip-status", action="store_true")

    args = parser.parse_args()
    return args


def _parse_dates(args):
    from_date = dt.date(args.year, args.month, 1)
    # get last day of month
    to_date = (from_date.replace(day=1) + dt.timedelta(days=32)).replace(
        day=1
    ) - dt.timedelta(days=1)
    return from_date, to_date


def _get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("log-level=3")
    options.add_argument("--ignore-certificate-errors-spki-list")
    options.add_argument("--ignore-ssl-errors")
    # options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    service_object = Service(binary_path)
    driver = webdriver.Chrome(service=service_object, options=options)
    driver.maximize_window()
    return driver


def _fill_search_page(driver, from_date, to_date):
    print(f"Fetching data from {from_date} to {to_date}")
    print("Fill captcha and click submit")

    url = "https://iprsearch.ipindia.gov.in/publicsearch"
    driver.get(url)
    print(driver.title)

    driver.find_element(By.ID, "FromDate").send_keys(f"{from_date:%m-%d-%Y}")
    driver.find_element(By.ID, "ToDate").send_keys(f"{to_date:%m-%d-%Y}")

    captcha = driver.find_element(By.XPATH, '//*[@id="CaptchaText"]')
    driver.execute_script("arguments[0].scrollIntoView();", captcha)
    captcha.click()

    time.sleep(9)


def _get_result_count(driver):
    last_page_button = driver.find_element(
        By.CSS_SELECTOR,
        'button.last[name="page"]',
    )
    page_count = int(last_page_button.get_attribute("value"))

    total_count_el = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Total Document(s):')]"
    )
    row_count = int(
        total_count_el.text.strip().removeprefix("Total Document(s): ").strip()
    )
    return page_count, row_count


def _get_master_df():
    return pd.DataFrame(
        columns=[
            "Application Number",
            "Title",
            "Application Date",
            "Status",
            "Publication Number",
            "Publication Date(U/S 11A)",
            "Publication Type",
            "Application Filing Date",
            "Priority Number",
            "Priority Country",
            "Priority Date",
            "Field Of Invention",
            "Classification (IPC)",
            "Inventor Name",
            "Inventor Address",
            "Inventor Country",
            "Inventor Nationality",
            "Applicant Name",
            "Applicant Address",
            "Applicant Country",
            "Applicant Nationality",
            "Abstract",
            "Application Type",
            "E-MAIL (As Per Record)",
            "ADDITIONAL-EMAIL (As Per Record)",
            "E-MAIL (UPDATED Online)",
            "PARENT APPLICATION NUMBER",
            "PARENT APPLICATION FILING DATE",
            "REQUEST FOR EXAMINATION DATE",
            "FIRST EXAMINATION REPORT DATE",
            "Date Of Certificate Issue",
            "POST GRANT JOURNAL DATE",
            "REPLY TO FER DATE",
            "PCT INTERNATIONAL APPLICATION NUMBER",
            "PCT INTERNATIONAL FILING DATE",
            "Application Status",
        ]
    )


def _get_from_main_page(driver, row):
    (
        application_number_cell,
        title_cell,
        application_date_cell,
        status_cell,
        status_link_cell,
    ) = row.find_elements(By.CSS_SELECTOR, "td")
    application_link = application_number_cell.find_element(By.CSS_SELECTOR, "button")
    status_link = status_link_cell.find_element(By.CSS_SELECTOR, "button")
    return (
        {
            "Application Number": application_link.text,
            "Title": title_cell.text,
            "Application Date": application_date_cell.text,
            "Status": status_cell.text,
        },
        application_link,
        status_link,
    )


def _get_from_application_number_link(driver, application_link):
    application_link.click()
    driver.switch_to.window(driver.window_handles[1])

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tab-content")))

    (
        title_row,
        publication_number_row,
        publication_date_row,
        publication_type_row,
        application_number_row,
        application_filing_date_row,
        priority_number_row,
        priority_country_row,
        priority_date_row,
        field_of_invention_row,
        classification_row,
        _inventor,
        inventors_row,
        _applicant,
        applicants_row,
        abstract_row,
        specification_row,
        application_status_link_row,
    ) = driver.find_elements(
        By.CSS_SELECTOR,
        "#home > table > tbody > tr",
    )

    def _get_row_table_cols(row):
        table = row.find_element(By.CSS_SELECTOR, "table")
        rows = table.find_elements(By.CSS_SELECTOR, "tr")
        # convert table to list of each row
        values = [
            [cell.text.strip() for cell in row.find_elements(By.CSS_SELECTOR, "td")]
            for row in rows[1:]
        ]
        # convert list to column wise dictionary
        headings = [cell.text for cell in rows[0].find_elements(By.CSS_SELECTOR, "th")]
        data = {
            heading: "\n".join([row[idx] for row in values])
            for idx, heading in enumerate(headings)
        }
        return data

    def _get_row_value(row):
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        assert len(cells) == 2
        return cells[1].text.strip()

    inventors = _get_row_table_cols(inventors_row)
    applicants = _get_row_table_cols(applicants_row)
    data = {
        "Publication Number": _get_row_value(publication_number_row),
        "Publication Date(U/S 11A)": _get_row_value(publication_date_row),
        "Publication Type": _get_row_value(publication_type_row),
        "Application Filing Date": _get_row_value(application_filing_date_row),
        "Priority Number": _get_row_value(priority_number_row),
        "Priority Country": _get_row_value(priority_country_row),
        "Priority Date": _get_row_value(priority_date_row),
        "Field Of Invention": _get_row_value(field_of_invention_row),
        "Classification (IPC)": _get_row_value(classification_row),
        "Inventor Name": inventors["Name"],
        "Inventor Address": inventors["Address"],
        "Inventor Country": inventors["Country"],
        "Inventor Nationality": inventors["Nationality"],
        "Applicant Name": applicants["Name"],
        "Applicant Address": applicants["Address"],
        "Applicant Country": applicants["Country"],
        "Applicant Nationality": applicants["Nationality"],
        "Abstract": abstract_row.text.strip(),
    }
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return data


def _get_from_application_status_link(driver, status_link):
    status_link.click()
    driver.switch_to.window(driver.window_handles[1])

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table-striped")))

    status_element = driver.find_element(
        By.XPATH,
        '//*[@id="Content"]/div[2]/table/tbody/tr[2]/td[1]',
    )
    if status_element.text == "APPLICATION STATUS":
        div_num = 2
    else:
        div_num = 3

    if div_num == 3:
        status_element = driver.find_element(
            By.XPATH,
            '//*[@id="Content"]/div[3]/table/tbody/tr[2]/td[2]',
        )
        table = driver.find_element(By.CSS_SELECTOR, "#Content table")
        # create dictionary of table values
        values = {"Application Status": status_element.text}
        for row in table.find_elements(By.CSS_SELECTOR, "tr"):
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if len(cells) == 2:
                values[cells[0].text.strip()] = cells[1].text.strip()
    elif div_num == 2:
        status_element = status_element = driver.find_element(
            By.XPATH,
            '//*[@id="Content"]/div[2]/table/tbody/tr[2]/td[2]',
        )
        values = {"Application Status": status_element.text}
    data = {
        "Application Type": values.get("APPLICATION TYPE", "NA"),
        "E-MAIL (As Per Record)": values.get("E-MAIL (As Per Record)", "NA"),
        "ADDITIONAL-EMAIL (As Per Record)": values.get(
            "ADDITIONAL-EMAIL (As Per Record)", "NA"
        ),
        "E-MAIL (UPDATED Online)": values.get("E-MAIL (UPDATED Online)", "NA"),
        "PARENT APPLICATION NUMBER": values.get("PARENT APPLICATION NUMBER", "NA"),
        "PARENT APPLICATION FILING DATE": values.get(
            "PARENT APPLICATION FILING DATE", "NA"
        ),
        "REQUEST FOR EXAMINATION DATE": values.get(
            "REQUEST FOR EXAMINATION DATE", "NA"
        ),
        "FIRST EXAMINATION REPORT DATE": values.get(
            "FIRST EXAMINATION REPORT DATE", "NA"
        ),
        "Date Of Certificate Issue": values.get("Date Of Certificate Issue", "NA"),
        "POST GRANT JOURNAL DATE": values.get("POST GRANT JOURNAL DATE", "NA"),
        "REPLY TO FER DATE": values.get("REPLY TO FER DATE", "NA"),
        "PCT INTERNATIONAL APPLICATION NUMBER": values.get(
            "PCT INTERNATIONAL APPLICATION NUMBER", "NA"
        ),
        "PCT INTERNATIONAL FILING DATE": values.get(
            "PCT INTERNATIONAL FILING DATE", "NA"
        ),
        "Application Status": values["Application Status"],
    }
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return data


def _get_row_data(driver, row, skip_status):
    data, application_link, status_link = _get_from_main_page(driver, row)
    data.update(_get_from_application_number_link(driver, application_link))
    if not skip_status:
        data.update(_get_from_application_status_link(driver, status_link))
    return data


def _save_df(df):
    out_path_csv = f"{from_date:%b%Y}.csv"
    out_path_xlsx = f"{from_date:%b%Y}.xlsx"
    writer = pd.ExcelWriter(out_path_xlsx, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    writer.save()
    df.to_csv(out_path_csv, index=False)


def _goto_next_page(driver):
    link = driver.find_element(
        By.XPATH, '//*[@id="header"]/div[4]/div/div[1]/form/div/button[3]'
    )
    try_count3 = 0
    max_tries3 = 10
    while try_count3 < max_tries3:
        try:
            link.click()
            wait = WebDriverWait(driver, 10)
            p = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Selected")))
            current_page = int(p.text)
            # print("Current page: ", current_page)
            break
        except Exception:
            if try_count3 == max_tries3:
                print(
                    "Max tries reached for clicking on next page button and page not loading."
                )
                break
            print("Clicked on next page but not loaded. Refreshing page.")
            driver.refresh()
            try_count3 += 1


if __name__ == "__main__":
    args = _parse_args()
    from_date, to_date = _parse_dates(args)

    driver = _get_driver()
    _fill_search_page(driver, from_date, to_date)
    page_count, row_count = _get_result_count(driver)

    df = _get_master_df()

    # show progress bar
    progress = tqdm(total=row_count)
    for page_number in range(page_count):
        rows = driver.find_elements(By.CSS_SELECTOR, "#tableData tr")
        for row in rows[1:]:
            row_data = _get_row_data(driver, row, args.skip_status)
            df.loc[len(df)] = row_data
        _save_df(df)
        _goto_next_page(driver)
        progress.update(1)

    progress.close()
    driver.quit()
