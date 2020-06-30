"""https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip



3,Region,,1,,,6,
3,"Episode week",,2,,,7;21,
3,"Episode year",,3,,,7,
3,Gender,,4,,,8,
3,"Age group",,5,,,9,
3,Occupation,,6,,,10,
3,Asymptomatic,,7,,,11,
3,"Onset week of symptoms",,8,,,12;21,
3,"Onset year of symptoms",,9,,,13,
3,"Symptom, cough",,10,,,14,
3,"Symptom, fever",,11,,,14,
3,"Symptom, chills",,12,,,14,
3,"Symptom, sore throat",,13,,,14,
3,"Symptom, runny nose",,14,,,14,
3,"Symptom, shortness of breath",,15,,,14,
3,"Symptom, nausea",,16,,,14,
3,"Symptom, headache",,17,,,14,
3,"Symptom, weakness",,18,,,14,
3,"Symptom, pain",,19,,,14,
3,"Symptom, irritability",,20,,,14,
3,"Symptom, diarrhea",,21,,,14,
3,"Symptom, other",,22,,,14,
3,"Hospital status",,23,,,15,
3,Recovered,,24,,,16,
3,"Recovery week",,25,,,17;21,
3,"Recovery year",,26,,,18,
3,Death,,27,,,19,
3,Transmission,,28,,,20,

Symbol Legend
Description,Symbol
"not available for a specific reference period",..
"less than the limit of detection",<LOD
"value rounded to 0 (zero) where there is a meaningful distinction between true zero and the value that was rounded",0s
"data quality: excellent",A
"data quality: very good",B
"data quality: good",C
"data quality: acceptable",D
"use with caution",E
"too unreliable to be published",F
"not applicable",...
preliminary,p
revised,r
"suppressed to meet the confidentiality requirements of the Statistics Act",x
terminated,t

"Survey Code","Survey Name"
5319,"COVID-19 epidemiological reports"

"Subject Code","Subject Name"
13,Health

"Note ID",Note
1,"Source: Public Health Agency of Canada (PHAC), COVID-19 epidemiological reports, with contribution from Provincial/Territorial Ministries of Health. For more information about this table please see the website: <a href=""https://www150.statcan.gc.ca/n1/en/catalogue/13260002"" rel=""external noopener noreferrer"" target=""_blank"">User Guide and Data Dictionary for Preliminary COVID-19 Data (opens new window)</a>."
2,"Given that the COVID-19 pandemic is rapidly evolving, these data are considered preliminary. The data published by Statistics Canada only account for those where a detailed case report was provided by the provincial or territorial jurisdiction to the Public Health Agency of Canada (PHAC). Statistics Canada’s detailed preliminary confirmed cases will not match the total case reporting done at the provincial and territorial levels which are reported daily by each jurisdiction and compiled by the PHAC.  The discrepancy is due to delays associated with the submission of the detailed information, its capture and coding. Hence, Statistics Canada’s file on detailed case reporting is a subset of the total counts reported by the health authorities across Canada."
3,"Confirmed cases are laboratory confirmed cases for which a case report form has been received by the Public Health Agency of Canada (PHAC) from provincial or territorial partners."
4,"On May 22nd, 2020, this data file of detailed confirmed cases from the Public Health Agency of Canada (PHAC) replaced data published in table 13-10-0766-01. This covers all of the detailed confirmed cases up to May 26th, but with new Statistics Canada Case identifier numbers."
5,"Statistics Canada generated case identifier number."
6,"Region: 1 = Atlantic (New Brunswick, Nova Scotia, Prince Edward Island, Newfoundland and Labrador), 2 = Quebec, 3 = Ontario and Nunavut, 4 = Prairies (Alberta, Saskatchewan, and Manitoba) and the Northwest Territories, 5 = British Columbia and Yukon."
7,"The episode week and episode year are derived from the episode date. The episode date is created from the earliest date available from the following series: Symptom Onset Date, Specimen Collection Date and Laboratory Testing Date. When no date is available, this field is considered ""Not stated"" and given the value 99. These values are corrected as Public Health Agency of Canada (PHAC) receives new information."
8,"Gender codes: 1 = Male, 2 = Female, 9 = Not stated. These values are corrected as the Public Health Agency of Canada (PHAC) receives new information. It should be noted that the French form uses the term 'sex' contrary to the English form that uses the term 'gender'. In the context of this table, the term gender is also used in French. The cases that have reported 'other' for sex or 'non-binary' for gender have been reclassified as 'not stated' gender."
9,"Age group codes: 1 = 0 to 19 years, 2 = 20 to 29 years, 3 = 30 to 39 years, 4 = 40 to 49 years, 5 = 50 to 59 years, 6 = 60 to 69 years, 7 = 70 to 79 years, 8 = 80 years or older, 99 = Not stated. These values are corrected as the Public Health Agency of Canada (PHAC) receives new information."
10,"Occupation: 1 = Health care worker, 2 = School or daycare worker/attendee, 3 = Long term care resident, 4 = Other, 9 = Not stated."
11,"Asymptomatic: 1=  Yes, 2  = No, 9 = Not Stated."
12,"Week of symptom(s) onset."
13,"Year of symptom(s) onset. 20 = the year 2020, 99 = Not stated."
14,"Symptom: 1 = Yes, 2 = No, 9 = Not Stated/Unknown."
15,"Hospitalization status: 1 = Hospitalized and in Intensive care unit 2 = Hospitalized, but not in intensive care unit, 3= Not hospitalized, 9 = Not Stated/Unknown."
16,"Indicates if the case has recovered. 1 = Yes, 2 = No, 9 = Not Stated/Unknown."
17,"Week of recovery date."
18,"Year of recovery date. 20 = the year 2020, 99 = Not stated."
19,"Death: 1 = Yes, 2 = No, 9 = Not stated."
20,"Transmission: 1 = Domestic acquisition - Contact of COVID case, contact with traveller, or unknown source, 2 = International travel, 9 = Not stated."
21,"0" represents the first days of the year leading up to, but not including the first Sunday. ""1"" represents the first full week of the year, beginning on the first Sunday, and so on."
22,"On June 4th, 2020, a large update was made to this table: cases from Quebec were added."

"Correction ID","Correction Date","Correction Note"
"""
import csv
from datetime import datetime, timedelta
from io import TextIOWrapper
import logging
from zipfile import ZipFile

from requests_html import AsyncHTMLSession
from requests import Response


logger = logging.getLogger(__name__)


CASES = {}

REGIONS = {
    "1": {
        "name": "Atlantic (New Brunswick, Nova Scotia, Prince Edward Island, Newfoundland and Labrador)",
        "count": 0,
    },
    "2": {"name": "Quebec"},
    "3": {"name": "Ontario and Nunavut"},
    "4": {
        "name": " Prairies (Alberta, Saskatchewan, and Manitoba) and the Northwest Territories"
    },
    "5": {"name": "British Columbia and Yukon."},
}


def _process_row(headers, row):
    data = {k: row[v] for k, v in [(k, v) for k, v in headers.items()]}
    case_identifcation_number = data["Case identifier number"]
    if case_identifcation_number not in CASES:
        pass
    if data["Case information"] == "Region":
        region = data["VALUE"]
        REGIONS[region].setdefault("count", 0)
        REGIONS[region]["count"] = REGIONS[region].get("count", 0) + 1
    CASES.setdefault(case_identifcation_number, {})
    if data["VALUE"] not in ("9", "99"):
        CASES[case_identifcation_number].setdefault(
            data["Case information"], data["VALUE"]
        )


async def _download_zip_file():
    global CASES
    session = AsyncHTMLSession()
    url = "https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip"
    filename = "tmp.zip"
    # resp: Response = await session.get(url, stream=True)

    # with open(filename, "wb") as f:
    #     for chunk in resp.iter_content(1024):
    #         f.write(chunk)

    return filename


def _process_zip_file(filename):
    with ZipFile(filename) as zipfile:
        with zipfile.open("13100781.csv") as csvbinary:
            csvtext = TextIOWrapper(csvbinary, encoding="utf-8-sig")
            datareader = csv.reader(csvtext)
            counter = 1
            headers = {}
            for row in datareader:
                if not headers:
                    logger.info("setting headers")
                    for index, value in enumerate(row):
                        headers[value.strip()] = index
                    logger.info("headers = %s", headers)
                    continue
                _process_row(headers, row)
                # if counter > 200:
                #     break
                counter += 1

    logger.info("processed %d records", counter)
    return REGIONS


async def _download_csv_file():
    session = AsyncHTMLSession()
    url = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"
    filename = "tmp.csv"
    resp: Response = await session.get(url, stream=True)

    with open(filename, "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

    return filename


def _process_csv_row(headers, row, regions):
    data = {k: row[v] for k, v in [(k, v) for k, v in headers.items()]}
    # only get yesterday's data
    one_day = timedelta(-1)
    yesterday = (datetime.today() + one_day).strftime("%d-%m-%Y")
    if not data["date"] == yesterday:
        # logger.error("no data for %s", yesterday)
        return
    province = data["prname"]
    if province in ("Canada", "Ontario", "Quebec"):
        logger.debug("skipping province %s", province)
        return
    regions.setdefault(province, {})
    try:
        rate = float(data.get("ratetotal", 0))
    except ValueError:
        rate = 0
    try:
        population = int(int(data["numtotal"]) * (100000 / rate))
    except ZeroDivisionError:
        logger.error("cannot calculate population for %s", data)
        if province == "Nunavut":
            population = 38780
        else:
            population = None
    try:
        regions[province]["All"] = {
            "count": int(data["numtotal"]),
            "rate": rate,
            "population": population,
        }
    except ValueError:
        pass


def _process_csv_file(filename):
    """"""
    regions = {}
    with open(filename) as csvtext:
        # csvtext = TextIOWrapper(csvbinary, encoding="utf-8-sig")
        datareader = csv.reader(csvtext)
        counter = 1
        headers = {}

        for row in datareader:
            if not headers:
                logger.info("setting headers")
                for index, value in enumerate(row):
                    headers[value.strip()] = index
                continue
            _process_csv_row(headers, row, regions)
            # if counter > 200:
            #     break
            counter += 1

    logger.info("processed %d records", counter)
    if not regions:
        logger.error("can't find any data for yesterday?")
    # logger.info("regions %s", regions)
    # logger.info(REGIONS)
    # logger.info(CASES)
    return regions


async def get_data():
    # filename = await _download_zip_file()
    # data = _process_zip_file(filename)
    filename = await _download_csv_file()
    data = _process_csv_file(filename)

    return data
