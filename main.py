"""gather data from each province"""
import asyncio
import json
import logging
import sys
from canadacovid19 import quebec, ontario, canada


logger = logging.getLogger(__name__)


def setup_logging(level):
    logging.basicConfig(stream=sys.stderr, level=level)


async def main():
    coros = [
        quebec.get_data(),
        ontario.get_data(),
        canada.get_data(),
    ]
    responses = await asyncio.gather(*coros)
    # logger.info(responses)

    data = []
    for response in responses:
        if len(response.keys()) > 1:
            # Canada
            # data.append({key: val for key, val in response.items()})
            data.extend([{k: response[k]} for k in response.keys()])
        else:
            data.append(response)

    for d in data:
        logger.info(d)

    with open("public/alldata.json", "w") as f:
        f.write(json.dumps(data))


if __name__ == "__main__":
    setup_logging(level=logging.DEBUG)
    asyncio.run(main())
