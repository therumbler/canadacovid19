"""https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip
"""
import csv
from zipfile import ZipFile

from requests_html import AsyncHTMLSession
from requests import Response


async def _download_file():
    session = AsyncHTMLSession()
    url = "https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip"
    resp: Response = await session.get(url, stream=True)
    filename = "tmp.zip"
    with open(filename, "wb") as f:
        for chunk in resp.iter_content(1024):
            f.write(chunk)

    with ZipFile(filename) as zipfile:
        with zipfile.open("13100781-eng/13100781.csv") as csvdata:
            datareader = csv.reader(csvdata)
            for row in datareader:
                logger.info(", ".join(row))
                break


async def get_data():
    await _download_file()
    return {}
