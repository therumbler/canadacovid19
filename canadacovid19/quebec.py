"""
https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/
"""
import logging
import re
from requests_html import AsyncHTMLSession


logger = logging.getLogger(__name__)


def _parse_data_div(div):
    """take a quebec data div and parse the table"""
    data = {}
    table_rows = div.find("tr")
    for tr in table_rows:
        # logger.info(tr)
        table_data = tr.find("td>p")
        if not table_data:
            continue
        key = table_data[0].text
        try:
            value = re.sub(r"\s", "", table_data[1].text.strip())
            # table_data[1].text.strip().replace(" ", "")
        except IndexError:
            logger.error("cannot find value for %s", key)
            value = None
        # logger.info("key: %s value: %s", key, value)
        data[key] = value
    return data


async def get_data():
    """get quebec data"""
    session = AsyncHTMLSession()
    url = "https://www.quebec.ca/en/health/health-issues/a-z/2019-coronavirus/situation-coronavirus-in-quebec/"
    resp = await session.get(url)
    div = resp.html.find("#c50214", first=True)
    data = _parse_data_div(div)
    # logger.info(data)
    return data
