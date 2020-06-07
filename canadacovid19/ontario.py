"""
parse data from https://www.publichealthontario.ca/en/data-and-analysis/infectious-disease/covid-19-data-surveillance/covid-19-data-tool

"""
from requests_html import AsyncHTMLSession
import pandas


async def _get_master(session: AsyncHTMLSession):
    url = "https://ws1.publichealthontario.ca/appdata/COVID/PROD/staticFilesDoNotTouch/master.xlsx"
    resp = await session.get(url)
    xlsx = pandas.read_excel(resp.raw)

    return xlsx


async def get_data():
    """get the data"""
    session = AsyncHTMLSession()
    master = await _get_master(session)
    # xlsx = pandas.ExcelFile()
    return {}
