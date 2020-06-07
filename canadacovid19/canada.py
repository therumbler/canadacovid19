"""https://www150.statcan.gc.ca/n1/tbl/csv/13100781-eng.zip
"""


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


async def get_data():
    await _download_file()
    return {}
