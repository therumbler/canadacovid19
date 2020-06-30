"""gather data from each province"""
import asyncio
import json
import logging
import os
import sys
from canadacovid19 import quebec, ontario, canada


logger = logging.getLogger(__name__)

PUBLIC_ALL_DATA_PATH = os.environ['PUBLIC_ALL_DATA_PATH']

def setup_logging(level):
    logging.basicConfig(stream=sys.stderr, level=level)


async def main():
    coros = [
        quebec.get_data(),
        ontario.get_data(),
        canada.get_data(),
    ]
    responses = await asyncio.gather(*coros)

    data = []
    for response in responses:
        if len(response.keys()) > 1:
            # Canada
            # data.append({key: val for key, val in response.items()})
            data.extend([{k: response[k]} for k in response.keys()])
        else:
            data.append(response)

    for d in data:
        logger.debug(d)

    with open("public/alldata.json", "w") as f:
        f.write(json.dumps(data))

    with open(f"{PUBLIC_ALL_DATA_PATH}/alldata.json", "w") as f:
        f.write(json.dumps(data))



if __name__ == "__main__":
    setup_logging(level=logging.INFO)
    asyncio.run(main())
