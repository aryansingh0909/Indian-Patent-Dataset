<h1 align="center">Indian Patent Dataset</h1>

<p align="center">A comprehensive dataset of all the patents filed in India for the years 2010, 2011, and 2019.</p>

## Overview

The Indian Patent Dataset provides detailed information about each patent application filed in India, including application number, title, application date, inventor and applicant information, patent status, and more. The dataset covers patents filed during the years 2010, 2011, and 2019.

## Motivation

The dataset was created to provide researchers, policymakers, businesses, legal professionals, and academics with valuable insights into the patent landscape in India. It aims to facilitate research and analysis, inform policy decisions, support business intelligence efforts, ensure legal and regulatory compliance, and enable academic research on innovation and technology transfer.

## Usage

```bash
# clone the repo
git clone path/to/git-repo
cd Indian-Patent-Dataset

# create virtual env
python3 -m venv .venv

# install requirements
pip install -r requirements.txt
source .venv/bin/activate

# run the script
python Scripts/scraping_main.py --month=1 --year=2024

# skip application status as it takes time
python Scripts/scraping_main.py --month=1 --year=2024 --skip-status

# run in headless mode
python Scripts/scraping_main.py --month=1 --year=2024 --skip-status --headless
```

## Composition

The dataset comprises individual instances representing patent applications filed in India. Each instance includes various features, such as:

- Application Number: Unique identifier for each patent application.
- Title: Title of the patent application.
- Application Date: Date when the patent application was filed.
- Status: Current status of the patent application.
- Publication Number: Number assigned to the publication of the patent application.
- Publication Date (U/S 11A): Date of publication under Section 11A.
- Publication Type: Type of publication.
- Application Filing Date: Date when the patent application was filed.
- Priority Number: Priority number of the patent application.
- Priority Country: Country of priority.
- Priority Date: Priority date of the patent application.
- Field Of Invention: Field of invention of the patent application.
- Classification (IPC): International Patent Classification of the patent application.
- Inventor Information: Information about the inventor(s) of the patent application.
- Applicant Information: Information about the applicant(s) of the patent application.
- Application Type: Type of patent application.
- E-mail (As Per Record): Email associated with the patent application record.
- Additional E-mail (As Per Record): Additional email associated with the patent application record.
- E-mail (Updated Online): Updated email associated with the patent application record.
- Request for Examination Date: Date of request for examination.
- First Examination Report Date: Date of the first examination report.
- Date Of Certificate Issue: Date of issue of the certificate.
- Post Grant Journal Date: Date of post-grant journal publication.
- Reply to FER Date: Date of reply to the first examination report.
- PCT International Application Number: International application number for PCT applications.
- PCT International Filing Date: International filing date for PCT applications.
- Application Status: Current status of the patent application.

## Collection Process

The data associated with each instance was acquired by scraping directly from the [Indian Patent Advanced Search System](https://iprsearch.ipindia.gov.in/publicsearch) using automation tools such as Selenium and Python. The scraping script scraping_main.py is provided in the repository for reference.

To run the scraping code download the scraping_main.py and chromedriver-win64.zip.

## Preprocessing

The dataset underwent some basic preprocessing, including cleaning strings and removing unnecessary symbols, to ensure data quality and consistency.

## Uses

The dataset can be used for various purposes, including:

- Research and Analysis
- Policy Making
- Business Intelligence
- Legal and Regulatory Compliance
- Academic Research

## Distribution

This dataset is distributed under the Creative Commons Attribution-ShareAlike (CC-BY-SA) license. Please refer to the LICENSE file for more information. Copyright is retained by the dataset owner.

## Maintenance

The dataset will be periodically updated to correct labeling errors, add new instances, or delete instances as necessary. Updates will be communicated through the repository.

## Contact

For questions or inquiries regarding the dataset, please contact [Aryan Singh] at [aryansinghmain09@gmail.com].
