"""https://kustom.radio-canada.ca/coronavirus/canada_quebec"""


from requests_html import AsyncHTMLSession


async def get_province(province: str):
    session = AsyncHTMLSession()
    url = f"https://kustom.radio-canada.ca/coronavirus/canada_{province.lower()}"
    resp = await session.get(url)

    return resp.json()
