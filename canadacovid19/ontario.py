"""
parse data from https://www.publichealthontario.ca/en/data-and-analysis/infectious-disease/covid-19-data-surveillance/covid-19-data-tool

"""

import logging
from urllib.parse import urlparse

from requests_html import AsyncHTMLSession
from requests import Response
import pandas

logger = logging.getLogger(__name__)


async def _download_xlsx(url: str, session):
    # url = f"https://ws1.publichealthontario.ca/appdata/COVID/PROD/staticFilesDoNotTouch/{filename}"
    # https://ws1.publichealthontario.ca/appdata/COVID/PROD/graphs.xlsx
    parsed_url = urlparse(url)
    filename = parsed_url.path.split("/")[-1]
    logger.info("filename %s", filename)
    # return filename
    # resp = await session.get(url)
    # resp: Response = await session.get(url, stream=True)
    # with open(filename, "wb") as f:
    #     for chunk in resp.iter_content(1024):
    #         f.write(chunk)
    return filename


async def _get_xlsx(url: str, session: AsyncHTMLSession):
    filename = await _download_xlsx(url, session)
    # url = "https://ws1.publichealthontario.ca/appdata/COVID/PROD/staticFilesDoNotTouch/master.xlsx"
    # resp = await session.get(url)
    # resp: Response = await session.get(url, stream=True)

    # with open(filename, "wb") as f:
    #     for chunk in resp.iter_content(1024):
    #         f.write(chunk)
    # xlsx = pandas.read_excel(filename)

    return filename


def _get_phus(filename: str):
    """get public health units"""
    df = pandas.read_excel(filename, "PHUs")
    phus = {}
    for index, row in df.iterrows():
        phus[row["PHU_ID"]] = row["PHU_Name"]
        # logger.info("%s", row["PHU_ID"])
    logger.info("phus = %s", phus)
    return phus


def _get_age_sex(filename: str, phus: dict):
    df = pandas.read_excel(filename, "ageSex")

    data: dict = {}
    for index, row in df.iterrows():
        if row["ageID"] != 11:
            # not all ages
            continue
        if row["areaID"] == 35:
            # total Ontario
            continue
        area_id = int(row["areaID"])
        phu = phus[area_id]
        # logger.info("phu %s", phu)
        data.setdefault(phu, {})
        # if row["ageID"] == 11:
        data[phu]["count"] = int(row["countAllCases"])
        data[phu]["rate"] = row["rateAllCases"]
        data[phu]["population"] = int(
            int(row["countAllCases"]) * (100000 / row["rateAllCases"])
        )

        # rate = (count / population)
        # population = rate * (1 / count)
        # rate / 100000 = count / population
        #
        # (rate / 100000) * (1 / count )= population
        #
        # logger.info(row)
    return data


async def get_data():
    """get the data"""
    session = AsyncHTMLSession()
    url = "https://ws1.publichealthontario.ca/appdata/COVID/PROD/staticFilesDoNotTouch/master.xlsx"

    master = await _get_xlsx(url, session)
    phus = _get_phus(master)

    url = "https://ws1.publichealthontario.ca/appdata/COVID/PROD/graphs.xlsx"
    graphs = await _get_xlsx(url, session)
    data = _get_age_sex(graphs, phus)
    # xlsx = pandas.ExcelFil
    # e()
    return {"Ontario": data}
